#!/usr/bin/env python3
"""CPO-style product judge: head-to-head tussen twee armen uit benchmark-run-dirs.

Anders dan judge_readability.py (alleen leesbaarheid) oordeelt deze judge als
een product-verantwoordelijke: eerst intent afleiden, dan huidige waarde
(correctheid/robuustheid van de gedeelde kern + verantwoorde extras), dan
toekomstwaarde (leesbaarheid, verandercosten tegen 3 neutrale scenario's,
testability, over-engineering), risico's, en pas daarna een verdict.
Slaat de volledige rationale ongekort op.

Gebruik:
  python3 judge_cpo.py --run-a <rundir> --arm-a total-programming \
      --run-b <rundir> --arm-b ponytail --out <rundir>/judge_cpo_x.json

Zelfde conventies als judge_readability.py: blinde A/B (volgorde wisselt per
rep), alleen geleverde gewijzigde bronbestanden (tree-diff vs fixture),
geen armenamen in het zicht van de judge, 3 retries bij ongeldige JSON.
"""
import argparse, json, statistics, subprocess, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

FEATURES = ['tmpl-fe-datepicker', 'tmpl-fe-colorpicker', 'tmpl-fe-command',
            'tmpl-fe-dropzone', 'tmpl-fe-wizard', 'tmpl-fe-rating']
SRC_EXT = ('.py', '.js', '.jsx', '.ts', '.tsx')

PROMPT = """You are a Chief Product Officer with a deep engineering background, comparing two solutions to the same problem. No formal requirements exist, so you must infer intent carefully. Judge on evidence, not stylistic preference. Both solutions are anonymous: do not guess which agent or style produced them.

Optional context: {domain}

<solution_a>
{a}
</solution_a>

<solution_b>
{b}
</solution_b>

## Step 1: Establish intent (before judging)
- Describe the core problem both solutions appear to solve, in 2-3 sentences.
- List the capabilities they share (common core).
- List the capabilities unique to A and unique to B.
- Generate 3 realistic future changes for this domain. Make them neutral: do not pick changes that favour one solution's existing structure.

## Step 2: Current value (score each solution 1-5)
- Core quality: how correct and robust is the common core, including edge cases and error paths?
- Extras: for each unique capability, explain who benefits and why. An extra counts as positive only if you can name a plausible user need. Unjustified extras are neutral or negative, because they add maintenance surface.

## Step 3: Future value (score each solution 1-5)
- Readability: could a new developer understand this in 15 minutes?
- Change cost: for each of the 3 scenarios, estimate files/places touched and regression risk.
- Testability: can the logic be tested in isolation?
- Over-engineering: penalize abstractions that solve no current or listed future problem.

## Step 4: Risks
Name the single biggest risk per solution: what breaks or hurts first?

## Step 5: Verdict
- Weigh current vs future value by expected lifespan. If no lifespan is given, assume production code.
- Choose A, B, or tie (only if the difference is genuinely negligible).
- State the deciding factor in one sentence.

Cite concrete code locations (file and symbol) for every substantive claim.

Respond with ONLY a JSON object, no markdown fences, with exactly these keys:
{{"intent": "<2-3 sentences>", "common_core": "<shared capabilities>", "unique_a": "<capabilities only A has>", "unique_b": "<capabilities only B has>", "future_changes": ["<change 1>", "<change 2>", "<change 3>"], "a_current": <1-5 int>, "b_current": <1-5 int>, "extras_note_a": "<who benefits from A's extras, or why they are unjustified>", "extras_note_b": "<same for B>", "a_future": <1-5 int>, "b_future": <1-5 int>, "change_cost_note": "<per scenario: files touched and regression risk for A and B>", "testability_note": "<can each solution's logic be tested in isolation>", "over_engineering_note": "<abstractions that solve no current or listed future problem>", "risk_a": "<single biggest risk of A>", "risk_b": "<single biggest risk of B>", "verdict": "<a|b|tie>", "deciding_factor": "<one sentence>", "citations": "<file/symbol references backing the claims>"}}"""


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fixture_hashes(fixture: Path):
    return {str(p.relative_to(fixture)): sha(p)
            for p in fixture.rglob('*')
            if p.is_file() and '.git' not in p.parts}


def delivered_src(ws: Path, fx: dict):
    out = []
    for p in ws.rglob('*'):
        if not p.is_file() or '.git' in p.parts or p.name.startswith('_'):
            continue
        rel = str(p.relative_to(ws))
        if not rel.endswith(SRC_EXT):
            continue
        n = p.name
        if n.startswith('test_') or n.endswith(('.test.ts', '.test.tsx', '.spec.ts')):
            continue
        if fx.get(rel) != sha(p):
            out.append((rel, p.read_text(errors='replace')))
    return sorted(out)


def render(files, tag):
    if not files:
        return f'({tag}: no source files delivered)'
    return '\n\n'.join(f'### {tag} — {rel}\n```{rel.rsplit(".", 1)[-1]}\n{text}\n```'
                       for rel, text in files)


INT_KEYS = ('a_current', 'b_current', 'a_future', 'b_future')


def judge_pair(judge, pair, a_text, b_text, a_arm, b_arm, domain):
    prompt = PROMPT.format(a=a_text, b=b_text, domain=domain)
    for attempt in range(3):
        try:
            r = subprocess.run(['claude', '-p', prompt, '--model', judge,
                                '--output-format', 'json'],
                               capture_output=True, text=True, timeout=600)
        except subprocess.TimeoutExpired:
            continue  # judge stalled — retry
        try:
            outer = json.loads(r.stdout)
            raw = outer.get('result', r.stdout)
            data = json.loads(raw[raw.index('{'):raw.rindex('}') + 1])
            if data.get('verdict') in ('a', 'b', 'tie') and all(
                    isinstance(data.get(k), int) for k in INT_KEYS):
                data['pair'] = pair
                data['a_arm'] = a_arm
                data['b_arm'] = b_arm
                return data
        except Exception:
            pass
    return {'pair': pair, 'a_arm': a_arm, 'b_arm': b_arm,
            'error': 'judge did not return valid JSON'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-a', type=Path, required=True, help='Run dir holding arm A cells')
    ap.add_argument('--arm-a', default='total-programming')
    ap.add_argument('--run-b', type=Path, required=True, help='Run dir holding arm B cells')
    ap.add_argument('--arm-b', default='baseline')
    ap.add_argument('--out', type=Path, help='Result JSON (default: <run-a>/judge_cpo.json)')
    ap.add_argument('--fixture', type=Path, default=Path('/tmp/total-programming-benchmark-fixture'))
    ap.add_argument('--judge', default='sonnet')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--domain', default='FastAPI + React full-stack template (expected lifespan: production code)')
    args = ap.parse_args()
    run_a, run_b = args.run_a.resolve(), args.run_b.resolve()
    arm_a, arm_b = args.arm_a, args.arm_b
    fx = fixture_hashes(args.fixture.resolve())

    jobs = []
    for task in FEATURES:
        for rep in range(4):
            a = run_a / f'{task}__{arm_a}__haiku__{rep}'
            b = run_b / f'{task}__{arm_b}__haiku__{rep}'
            if not (a.is_dir() and b.is_dir()):
                continue
            # Alternate which arm is shown as A to balance position bias.
            if rep % 2 == 0:
                jobs.append((task, rep, a, b, arm_a, arm_b))
            else:
                jobs.append((task, rep, b, a, arm_b, arm_a))

    def one(job):
        task, rep, ws_a, ws_b, a_arm, b_arm = job
        a_text = render(delivered_src(ws_a, fx), 'A')
        b_text = render(delivered_src(ws_b, fx), 'B')
        if len(a_text) + len(b_text) > 120_000:
            return {'pair': [task, rep], 'error': 'pair too large'}
        return judge_pair(args.judge, [task, rep], a_text, b_text, a_arm, b_arm, args.domain)

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(one, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            try:
                r = f.result()
            except Exception as exc:
                r = {'pair': ['unknown'], 'error': str(exc)[:300]}
            results.append(r)
            if 'error' in r:
                print(f'[{i}/{len(jobs)}] {r["pair"][0]}: {r["error"]}', flush=True)
            else:
                print(f'[{i}/{len(jobs)}] {r["pair"][0]} rep{r["pair"][1]}: '
                      f'verdict={r["verdict"]} cur={r["a_current"]}/{r["b_current"]} '
                      f'fut={r["a_future"]}/{r["b_future"]}', flush=True)

    valid = [r for r in results if 'error' not in r]

    def wins(arm):
        return sum(1 for r in valid
                   if (r['verdict'] == 'a') == (r['a_arm'] == arm) and r['verdict'] != 'tie')

    def mean_for(arm, key):
        vals = [r[f'a_{key}'] if r['a_arm'] == arm else r[f'b_{key}'] for r in valid]
        return round(statistics.mean(vals), 2) if vals else None

    summary = {
        'judge_model': args.judge, 'judge_kind': 'cpo-product',
        'domain': args.domain, 'pairs': len(jobs), 'valid': len(valid),
        'blinding': 'A/B order alternates by repetition; judge sees no arm names',
        arm_a: {'wins': wins(arm_a), 'mean_current': mean_for(arm_a, 'current'),
                'mean_future': mean_for(arm_a, 'future')},
        arm_b: {'wins': wins(arm_b), 'mean_current': mean_for(arm_b, 'current'),
                'mean_future': mean_for(arm_b, 'future')},
        'ties': sum(1 for r in valid if r['verdict'] == 'tie'),
        'per_task': {t: {str(r['pair'][1]): r['verdict'] if (r['a_arm'] == arm_a)
                         else {'a': 'b', 'b': 'a', 'tie': 'tie'}[r['verdict']]
                         for r in valid if r['pair'][0] == t} for t in FEATURES},
    }
    out = args.out or (run_a / 'judge_cpo.json')
    out.write_text(json.dumps({'results': results, 'summary': summary}, indent=2))
    print(f'wrote {out}')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
