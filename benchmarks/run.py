#!/usr/bin/env python3
"""Run Ponytail's pinned agentic tasks with clean baseline/Total Programming arms."""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ['tmpl-fe-datepicker', 'tmpl-fe-colorpicker', 'tmpl-fe-command',
            'tmpl-fe-dropzone', 'tmpl-fe-wizard', 'tmpl-fe-rating',
            'tmpl-be-duplicate', 'tmpl-be-search', 'tmpl-be-count',
            'tmpl-be-archive', 'tmpl-be-bulkdelete', 'tmpl-be-csv']
SAFETY = ['safe-path', 'critic-email', 'rate-limit', 'sql-user', 'auth-token', 'csv-sum', 'cache']
UPSTREAM_COMMIT = 'e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156'


def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], text=True).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--upstream', type=Path, required=True)
    ap.add_argument('--fixture', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--pilot', action='store_true', help='One safe-path cell per arm')
    ap.add_argument('--arms', default='baseline,total-programming',
                    help='Comma-separated subset of baseline,total-programming,ponytail')
    ap.add_argument('--model-id', help='Model id for every cell (e.g. glm-5.3-flash via '
                                       'ANTHROPIC_BASE_URL to a compatible endpoint); '
                                       'overrides the haiku/sonnet/opus shorthand')
    ap.add_argument('--runner', choices=['claude', 'pi'], default='claude',
                    help='Agent harness executing each cell')
    ap.add_argument('--provider', default='zai', help='pi provider id (--runner pi)')
    ap.add_argument('--timeout', type=int, help='Per-cell wall-time cap override (default: upstream 300s)')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--resume', action='store_true')
    args = ap.parse_args()
    upstream, fixture, output = args.upstream.resolve(), args.fixture.resolve(), args.output.resolve()
    if output.exists() and not args.resume:
        sys.exit('Output already exists; use --resume to retain and continue existing cells.')
    if args.resume and not (output / 'manifest.json').exists():
        sys.exit('No existing manifest to resume')
    if git(upstream, 'rev-parse', 'HEAD') != UPSTREAM_COMMIT:
        sys.exit('Unexpected upstream commit')
    if not git(fixture, 'rev-parse', 'HEAD').startswith('cd83fc1'):
        sys.exit('Unexpected fixture commit')
    if git(upstream, 'status', '--porcelain', '--untracked-files=no') or git(fixture, 'status', '--porcelain', '--untracked-files=no'):
        sys.exit('Upstream and fixture tracked files must be clean')
    real_claude = shutil.which('claude')
    if not real_claude:
        sys.exit('claude not installed')
    os.environ['BENCH_CLAUDE_BIN'] = real_claude
    os.environ['PONYTAIL_TMPL'] = str(fixture)
    os.environ['PATH'] = str(ROOT / 'benchmarks/bin') + os.pathsep + os.environ['PATH']
    source = upstream / 'benchmarks/agentic'
    sys.path.insert(0, str(source))
    spec = importlib.util.spec_from_file_location('upstream_benchmark', source / 'run.py')
    assert spec is not None and spec.loader is not None
    bench = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bench)
    if bench.selftest():
        sys.exit('Upstream instrument selftests failed')
    skill = (ROOT / 'skills/total-programming/SKILL.md').read_text()
    principles = skill.split('---', 2)[2].strip()
    bench.ARMS['total-programming'] = lambda: principles
    if 'ponytail' in args.arms.split(','):
        bench.ARMS['ponytail'] = lambda: (upstream / 'skills/ponytail/SKILL.md').read_text(encoding='utf-8')
        # Raw --append-system-prompt instead of upstream's --plugin-dir mechanism, so all
        # extra arms enter the prompt the same way and the comparison stays mechanism-blind.
        bench.PLUGIN_ARMS = ()
    if args.model_id:
        bench.MODELS['haiku'] = args.model_id
    if args.timeout:
        bench.CELL_TIMEOUT = args.timeout

    def run_cell_pi(task_id, arm, model, workdir: Path):
        """pi-equivalent of bench.run_cell: identical workspace setup, same
        evidence files (_invocation/_events/_init/_claude.json + stderr with the
        kill marker), so scoring, resume and isolation checks work unchanged."""
        import time
        task = bench.TASKS[task_id]
        if task.get("fixture"):
            fx = Path(task["fixture"])
            if not fx.is_absolute():
                fx = source / "fixtures" / task["fixture"]
            shutil.copytree(fx, workdir, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("node_modules", ".git", "build", "dist",
                                                          "dist-ssr", ".vite", "*.log", "__pycache__",
                                                          "storage", ".venv", "venv", ".pytest_cache",
                                                          "*.mp4", "*.mp3", "*.wav", "*.mov",
                                                          "*service-account*.json",
                                                          "nul", "con", "prn", "aux",
                                                          "DatePicker*.tsx", "DatePicker*.jsx"))
            manifest_files = sorted(str(p.relative_to(workdir)).replace("\\", "/")
                                    for p in workdir.rglob("*") if p.is_file())
            (workdir / "_fixture_files.json").write_text(json.dumps(manifest_files), encoding="utf-8")
        for fn, content in task.get("seed", {}).items():
            (workdir / fn).write_text(content, encoding="utf-8")
        if task.get("fixture"):
            bench._git_snapshot(workdir)
        pi = shutil.which("pi")
        if not pi:
            sys.exit("pi CLI not found on PATH")
        extra = bench.ARMS[arm]() if arm in bench.ARMS else None
        append = (extra + "\n\n" + bench.NO_RUN) if extra else bench.NO_RUN
        cmd = [pi, "-p", task["prompt"], "--mode", "json", "--no-session",
               "--no-extensions", "--no-skills", "--provider", args.provider,
               "--model", bench.MODELS[model], "--tools", "read,write,edit",
               "--append-system-prompt", append]
        (workdir / "_invocation.json").write_text(json.dumps(cmd, indent=2))
        started = time.monotonic()
        try:
            with open(workdir / "_pi_events.jsonl", "wb") as so, \
                 open(workdir / "_claude.stderr.txt", "wb") as se:
                proc = subprocess.Popen(cmd, cwd=str(workdir), stdout=so, stderr=se,
                                        start_new_session=True)
                try:
                    proc.wait(timeout=bench.CELL_TIMEOUT)
                except subprocess.TimeoutExpired:
                    bench._tree_kill(proc)
                    try: proc.wait(timeout=15)
                    except Exception: pass
                    se.write(f"\n[KILLED after {bench.CELL_TIMEOUT}s timeout]".encode())
        except Exception as e:
            (workdir / "_claude.json").write_text(json.dumps({"error": str(e)[:300]}), encoding="utf-8")
        result_text, in_tok, out_tok, turns = "", 0, 0, 0
        events = []
        trace = workdir / "_pi_events.jsonl"
        if trace.exists():
            for line in trace.read_text(errors="replace").splitlines():
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                events.append(o)
                if o.get("type") == "turn_end":
                    turns += 1
                if o.get("type") == "message_end":
                    m = o.get("message", {})
                    if m.get("role") == "assistant":
                        u = m.get("usage") or {}
                        in_tok += u.get("input") or 0
                        out_tok += u.get("output") or 0
                        c = m.get("content")
                        if isinstance(c, list):
                            for part in c:
                                if isinstance(part, dict) and part.get("type") == "text":
                                    result_text += part.get("text", "")
                        elif isinstance(c, str):
                            result_text += c
        is_err = not any(o.get("type") == "agent_end" for o in events)
        duration_ms = int((time.monotonic() - started) * 1000)
        (workdir / "_claude.json").write_text(json.dumps({
            "result": result_text if not is_err else "pi produced no agent_end event",
            "total_cost_usd": None, "duration_ms": duration_ms, "num_turns": turns,
            "is_error": is_err, "subtype": "success" if not is_err else "error",
            "permission_denials": [],
            "usage": {"input_tokens": in_tok, "output_tokens": out_tok,
                      "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        }, indent=2))
        (workdir / "_init.json").write_text(json.dumps(
            {"plugins": [], "skills": [], "mcp_servers": []}, indent=2))
        return bench.score_workspace(task_id, arm, model, workdir)

    arms = args.arms.split(',')
    tasks, repeats = (['safe-path'], 1) if args.pilot else (FEATURES + SAFETY, 4)
    cells = [(t, a, 'haiku', r) for t in tasks for r in range(repeats)
             for a in arms]
    random.Random(20260918).shuffle(cells)
    output.mkdir(parents=True, exist_ok=True)
    manifest = {
        'started_at': datetime.now(timezone.utc).isoformat(),
        'upstream_commit': UPSTREAM_COMMIT,
        'fixture_commit': git(fixture, 'rev-parse', 'HEAD'),
        'principles_commit': git(ROOT, 'rev-parse', 'HEAD'),
        'skill_sha256': hashlib.sha256(skill.encode()).hexdigest(),
        'claude': subprocess.check_output([real_claude, '--version'], text=True).strip(),
        'model': bench.MODELS['haiku'], 'tasks': tasks, 'repeats': repeats,
        'planned_cells': len(cells), 'workers': args.workers,
        'shuffle_seed': 20260918,
        'adaptations': [
            'Original upstream prompts, seeds, fixture and scorers; added Total Programming arm.',
            'Safe mode, empty setting sources, skills disabled, no session persistence, no MCP.',
            'Only Read/Write/Edit/Glob/Grep available; original NO_RUN instruction retained.',
            'Principles appended as system text, not plugin hook, to avoid all customization discovery.',
            'Identical $0.75 list-price budget per cell and upstream 300-second timeout.',
            'Stream output retained and checked for isolation; final JSON passed to upstream scorer.',
            'Seeded random cell order; stop scheduling on CLI errors, limits or missing results.',
        ],
        'billing_note': 'Claude-reported list-price cost, not a statement of subscription charges.',
        'cells': cells,
    }
    if args.model_id:
        manifest['adaptations'].append(
            f'Model override: every cell runs {args.model_id} via ANTHROPIC_BASE_URL to a '
            'compatible endpoint; CLI-reported cost is not Anthropic list price here.')
    if args.runner == 'pi':
        manifest['adaptations'].append(
            f'Runner: pi coding agent (provider {args.provider}); cell tools read/write/edit '
            '(no bash, glob, grep). Cost figures are upstream pricing metadata, not billed cost.')
    if args.timeout:
        manifest['adaptations'].append(f'Per-cell timeout override: {args.timeout}s (upstream default 300s).')
    if args.resume:
        previous = json.loads((output / 'manifest.json').read_text())
        assert previous['skill_sha256'] == manifest['skill_sha256']
        assert previous['cells'] == [list(c) for c in cells]
        assert previous['claude'] == manifest['claude']
        (output / 'resume-manifest.json').write_text(json.dumps(manifest, indent=2))
    else:
        (output / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    (output / 'principles.md').write_text(principles + '\n')
    results = []
    failures = []

    def score_timeout(cell, ws):
        task, arm, model, rep = cell
        scored = bench.score_workspace(task, arm, model, ws)
        scored.update(repetition=rep, valid_run=False, cli_subtype='timeout',
                      workspace=ws.name, actual_models=[],
                      run_error=f'Killed after {bench.CELL_TIMEOUT} seconds',
                      duration_ms=bench.CELL_TIMEOUT * 1000, cost=None)
        return scored

    if args.resume:
        previous_results = json.loads((output / 'results.json').read_text())
        (output / 'pre-resume-results.json').write_text(json.dumps(previous_results, indent=2))
        results = previous_results['results']
        for failure in previous_results['failures']:
            cell = failure['cell']
            ws = output / '__'.join(map(str, cell))
            if '[KILLED after 300s timeout]' not in (ws / '_claude.stderr.txt').read_text():
                sys.exit('Cannot automatically resume non-timeout failure')
            results.append(score_timeout(cell, ws))

    def one(cell):
        task, arm, model, rep = cell
        ws = output / f'{task}__{arm}__{model}__{rep}'
        ws.mkdir()
        if args.runner == 'pi':
            scored = run_cell_pi(task, arm, model, ws)
        else:
            scored = bench.run_cell(task, arm, model, ws)
        if f'[KILLED after {bench.CELL_TIMEOUT}s timeout]' in (ws / '_claude.stderr.txt').read_text():
            return score_timeout(cell, ws)
        raw = json.loads((ws / '_claude.json').read_text())
        init = json.loads((ws / '_init.json').read_text())
        valid = not raw.get('is_error') and raw.get('subtype') == 'success'
        valid = valid and not any(init.get(k) for k in ('plugins', 'skills', 'mcp_servers'))
        valid = valid and not raw.get('permission_denials')
        scored.update(repetition=rep, valid_run=valid, cli_subtype=raw.get('subtype'),
                      workspace=ws.name, actual_models=list(raw.get('modelUsage', {})))
        if not valid:
            scored['run_error'] = raw.get('result', str(raw))[-1500:]
        return scored

    def save():
        (output / 'results.json').write_text(json.dumps({'results': results, 'failures': failures}, indent=2))
        usable = [r for r in results if r.get('valid_run')]
        (output / 'summary.json').write_text(json.dumps(bench.aggregate(usable), indent=2))
        state = {'completed': len(results), 'planned': len(cells), 'valid': len(usable),
                 'estimated_cost_usd': sum(r.get('cost') or 0 for r in results),
                 'stopped_on_error': bool(failures)}
        (output / 'status.json').write_text(json.dumps(state, indent=2))

    print(f'Running {len(cells)} cells in {output}', flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        completed = {r['workspace'] for r in results}
        remaining = iter(c for c in cells if '__'.join(map(str, c)) not in completed)
        active = {}
        def schedule():
            cell = next(remaining, None)
            if cell is not None:
                active[pool.submit(one, cell)] = cell
        for _ in range(args.workers):
            schedule()
        while active:
            done, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in done:
                cell = active.pop(future)
                try:
                    result = future.result()
                    results.append(result)
                    if not result['valid_run'] and result.get('cli_subtype') != 'timeout':
                        failures.append({'cell': cell, 'error': result.get('run_error')})
                    print(f'[{len(results)}/{len(cells)}] {cell}: valid={result["valid_run"]} '
                          f'LOC={result["total_loc"]} safe={result["safe"]} '
                          f'cost={result.get("cost")}', flush=True)
                except Exception as exc:
                    failures.append({'cell': cell, 'error': str(exc)})
                    print(f'FAILED {cell}: {exc}', flush=True)
                save()
            if not failures:
                for _ in done:
                    schedule()
    save()
    if failures or len(results) != len(cells):
        sys.exit('Stopped before successful completion; see status.json and raw cell evidence.')
    bench.print_table(bench.aggregate([r for r in results if r.get('valid_run')]))
    print(f'COMPLETE: {len(results)} cells; evidence: {output}', flush=True)


if __name__ == '__main__':
    main()
