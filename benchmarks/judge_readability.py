#!/usr/bin/env python3
"""Blind pairwise readability judge for the agentic benchmark.

Pairs each repetition of arm A with the same repetition of arm B and asks a
judge model (via the Claude Code CLI, so it uses the same subscription auth as
the cells) which anonymous solution it would rather maintain. The judge never
learns which arm produced which solution; the A/B order alternates per
repetition to balance position bias. Arms may live in different run
directories (e.g. comparing arms from separate runs).

  python3 benchmarks/judge_readability.py \
      --run-a benchmarks/runs/<dir-a> --arm-a total-programming \
      --run-b benchmarks/runs/<dir-b> --arm-b ponytail \
      [--judge sonnet] [--workers 4] [--out PATH]

Reads delivered source files via tree-diff against the fixture commit the cells
were run with (tests excluded). Writes the result JSON via --out (default:
<run-a>/judge_readability.json) and prints aggregates. A judgment is
directional evidence, not a deterministic measurement.
"""
import argparse, json, hashlib, statistics, subprocess, sys, tempfile, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ['tmpl-fe-datepicker', 'tmpl-fe-colorpicker', 'tmpl-fe-command',
            'tmpl-fe-dropzone', 'tmpl-fe-wizard', 'tmpl-fe-rating']
SRC_EXT = ('.py', '.js', '.jsx', '.ts', '.tsx')
PROMPT = """You are a senior engineer reviewing two ANONYMOUS implementations (A and B) of the same small feature task in an existing FastAPI + React codebase.

Judge READABILITY AND COMPREHENSIBILITY ONLY, as the next maintainer would experience it:
- naming and vocabulary,
- structure and obviousness of intent,
- how quickly you could safely change this code,
- penalize both unnecessary cleverness/abstraction AND unexplained density.

Do NOT judge feature completeness, framework choice, or line count by itself.

Solution A:
{a}

Solution B:
{b}

Respond with ONLY this JSON:
{{"a_score": <1-5 int>, "b_score": <1-5 int>, "prefer": "<a|b|tie>", "why": "<one line>"}}"""

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def fixture_hashes(fixture: Path):
    return {str(p.relative_to(fixture)): sha(p)
            for p in fixture.rglob('*')
            if p.is_file() and '.git' not in p.parts}

def delivered_src(ws: Path, fx: dict):
    out = []
    for p in ws.rglob('*'):
        if not p.is_file() or '.git' in p.parts or p.name.startswith('_'): continue
        rel = str(p.relative_to(ws))
        if not rel.endswith(SRC_EXT): continue
        n = p.name
        if n.startswith('test_') or n.endswith(('.test.ts', '.test.tsx', '.spec.ts')): continue
        if fx.get(rel) != sha(p): out.append((rel, p.read_text(errors='replace')))
    return sorted(out)

def render(files, tag):
    if not files: return f'({tag}: no source files delivered)'
    return '\n\n'.join(f'### {tag} — {rel}\n```{rel.rsplit(".",1)[-1]}\n{text}\n```'
                       for rel, text in files)

def judge_pair(judge, pair, a_text, b_text, a_arm, b_arm):
    prompt = PROMPT.format(a=a_text, b=b_text)
    for attempt in range(3):
        try:
            r = subprocess.run(['claude', '-p', prompt, '--model', judge,
                                '--output-format', 'json'],
                               capture_output=True, text=True, timeout=600)
        except subprocess.TimeoutExpired:
            continue  # judge stalled (large pair or busy API) — retry
        try:
            outer = json.loads(r.stdout)
            raw = outer.get('result', r.stdout)
            data = json.loads(raw[raw.index('{'):raw.rindex('}') + 1])
            if data.get('prefer') in ('a', 'b', 'tie'):
                return {'pair': pair, 'a_arm': a_arm, 'b_arm': b_arm,
                        'a_score': data['a_score'], 'b_score': data['b_score'],
                        'prefer': data['prefer'], 'why': data.get('why', '')[:200]}
        except Exception:
            pass
    return {'pair': pair, 'a_arm': a_arm, 'b_arm': b_arm, 'error': 'judge did not return valid JSON'}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-a', type=Path, required=True, help='Run dir holding arm A cells')
    ap.add_argument('--arm-a', default='total-programming')
    ap.add_argument('--run-b', type=Path, required=True, help='Run dir holding arm B cells')
    ap.add_argument('--arm-b', default='baseline')
    ap.add_argument('--out', type=Path, help='Result JSON (default: <run-a>/judge_readability.json)')
    ap.add_argument('--fixture', type=Path, default=Path('/tmp/total-programming-benchmark-fixture'))
    ap.add_argument('--judge', default='sonnet')
    ap.add_argument('--workers', type=int, default=4)
    args = ap.parse_args()
    run_a, run_b = args.run_a.resolve(), args.run_b.resolve()
    arm_a, arm_b = args.arm_a, args.arm_b
    fx = fixture_hashes(args.fixture.resolve())

    jobs = []
    for task in FEATURES:
        for rep in range(4):
            a = run_a / f'{task}__{arm_a}__haiku__{rep}'
            b = run_b / f'{task}__{arm_b}__haiku__{rep}'
            if not (a.is_dir() and b.is_dir()): continue
            # Alternate which arm is shown as A to balance position bias.
            if rep % 2 == 0: jobs.append((task, rep, a, b, arm_a, arm_b))
            else:            jobs.append((task, rep, b, a, arm_b, arm_a))

    def one(job):
        task, rep, ws_a, ws_b, a_arm, b_arm = job
        a_text = render(delivered_src(ws_a, fx), 'A')
        b_text = render(delivered_src(ws_b, fx), 'B')
        if len(a_text) + len(b_text) > 120_000:
            return {'pair': [task, rep], 'error': 'pair too large'}
        return judge_pair(args.judge, [task, rep], a_text, b_text, a_arm, b_arm)

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(one, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            try:
                r = f.result()
            except Exception as exc:
                r = {'pair': ['unknown'], 'error': str(exc)[:200]}
            results.append(r)
            print(f'[{i}/{len(jobs)}] {r["pair"][0]} rep{r["pair"][1]}: '
                  + (r.get('error') or f'prefer={r["prefer"]} a={r["a_score"]} b={r["b_score"]}'), flush=True)

    valid = [r for r in results if 'error' not in r]
    def arm_stats(arm):
        scored = [(r['a_score'] if r['a_arm'] == arm else r['b_score']) for r in valid]
        wins = sum(1 for r in valid if (r['prefer'] == 'a') == (r['a_arm'] == arm) and r['prefer'] != 'tie')
        return {'mean_score': round(statistics.mean(scored), 2), 'wins': wins}
    summary = {
        'judge_model': args.judge, 'pairs': len(jobs), 'valid': len(valid),
        'blinding': 'A/B order alternates by repetition; judge sees no arm names',
        arm_a: arm_stats(arm_a),
        arm_b: arm_stats(arm_b),
        'ties': sum(1 for r in valid if r['prefer'] == 'tie'),
        'per_task': {t: {str(r['pair'][1]): r['prefer'] if (r['a_arm'] == arm_a) else
                         {'a': 'b', 'b': 'a', 'tie': 'tie'}[r['prefer']]
                         for r in valid if r['pair'][0] == t} for t in FEATURES},
    }
    out = args.out or (run_a / 'judge_readability.json')
    out.write_text(json.dumps({'results': results, 'summary': summary}, indent=2))
    print(f'wrote {out}')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
