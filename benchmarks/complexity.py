#!/usr/bin/env python3
"""Post-hoc complexity metrics over a benchmark run directory (no model calls).

For every cell workspace it detects the delivered source files by tree-diffing
against the pinned fixture commit (tests excluded), then measures cyclomatic
complexity per function with lizard (https://github.com/terryyin/lizard).
Aggregates: median per task, then mean over tasks — the same shape as the
runner's own tables.

  pip install lizard            # the only dependency
  python3 benchmarks/complexity.py --run benchmarks/runs/<dir> \
      [--fixture /tmp/total-programming-benchmark-fixture]

Writes complexity.json into the run directory and prints a per-arm table.
Lower is not automatically better: complexity complements LOC — together they
show whether an arm delivered less code by writing denser functions or by
building less. Requires the fixture checkout the cells were run against.
"""
import argparse, hashlib, json, statistics
from pathlib import Path

import lizard

FEATURES = ['tmpl-fe-datepicker', 'tmpl-fe-colorpicker', 'tmpl-fe-command',
            'tmpl-fe-dropzone', 'tmpl-fe-wizard', 'tmpl-fe-rating',
            'tmpl-be-duplicate', 'tmpl-be-search', 'tmpl-be-count',
            'tmpl-be-archive', 'tmpl-be-bulkdelete', 'tmpl-be-csv']
SAFETY = ['safe-path', 'critic-email', 'rate-limit', 'sql-user',
          'auth-token', 'csv-sum', 'cache']
SRC_EXT = ('.py', '.js', '.jsx', '.ts', '.tsx')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_hashes(fixture: Path) -> dict:
    return {str(p.relative_to(fixture)): sha(p)
            for p in fixture.rglob('*')
            if p.is_file() and '.git' not in p.parts}


def delivered_src(ws: Path, fx: dict) -> list:
    out = []
    for p in ws.rglob('*'):
        if not p.is_file() or '.git' in p.parts or p.name.startswith('_'):
            continue
        rel = str(p.relative_to(ws))
        if not rel.endswith(SRC_EXT):
            continue
        n = p.name
        if n.startswith('test_') or n.endswith(('.test.ts', '.test.tsx', '.spec.ts')):
            continue  # test code is tracked separately
        if fx.get(rel) != sha(p):
            out.append(str(p))
    return out


def measure(files: list) -> dict:
    fns = []
    for f in files:
        try:
            a = lizard.analyze_file(f)
        except Exception:
            continue
        fns += [fn.cyclomatic_complexity for fn in a.function_list]
    if not fns:
        return {}
    return {'n_fn': len(fns), 'cc_mean': round(statistics.mean(fns), 2),
            'cc_max': max(fns), 'fn_cc_gt5': sum(c > 5 for c in fns)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', type=Path, required=True)
    ap.add_argument('--fixture', type=Path,
                    default=Path('/tmp/total-programming-benchmark-fixture'))
    args = ap.parse_args()
    run, fx = args.run.resolve(), fixture_hashes(args.fixture.resolve())

    cells = {}
    for ws in sorted(run.iterdir()):
        if ws.is_dir() and ws.name.count('__') == 3:
            task, arm = ws.name.split('__')[:2]
            m = measure(delivered_src(ws, fx))
            if m:
                cells.setdefault(task, {}).setdefault(arm, []).append(m)

    print(f"{'task':22s} {'arm':20s} {'n':>2} {'fn':>6} {'cc-gem':>7} {'cc-max':>7} {'fn>CC5':>7}")
    table = {}
    for task, arms in cells.items():
        for arm, reps in arms.items():
            agg = {k: statistics.median(r[k] for r in reps)
                   for k in ('n_fn', 'cc_mean', 'cc_max', 'fn_cc_gt5')}
            table.setdefault(arm, {})[task] = agg
            print(f"{task:22s} {arm:20s} {len(reps):2d} {agg['n_fn']:6.1f} "
                  f"{agg['cc_mean']:7.2f} {agg['cc_max']:7.1f} {agg['fn_cc_gt5']:7.1f}")

    summary = {}
    for arm, tasks in table.items():
        summary[arm] = {}
        for name, tier in (('feature', FEATURES), ('safety', SAFETY)):
            rows = [tasks[t] for t in tier if t in tasks]
            if rows:
                summary[arm][name] = {
                    'tasks': len(rows),
                    'n_fn': round(statistics.mean(r['n_fn'] for r in rows), 1),
                    'cc_mean': round(statistics.mean(r['cc_mean'] for r in rows), 2),
                    'cc_max': round(statistics.mean(r['cc_max'] for r in rows), 1),
                    'fn_cc_gt5': round(statistics.mean(r['fn_cc_gt5'] for r in rows), 2),
                }
    (run / 'complexity.json').write_text(json.dumps(summary, indent=2))
    print('\nTier summary (mean of per-task medians):')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
