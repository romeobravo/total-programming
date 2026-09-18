# Agentic benchmark

Compare a clean Claude Code baseline with the eleven Total Programming principles.
The harness reuses Ponytail's tasks and scorers, pinned at
`e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156`, against the FastAPI template at
`cd83fc1` (the same fixture revision used by the published benchmark).

## Run

Requires Python 3, Git, and an authenticated Claude Code CLI that supports `--safe-mode`.
No Python packages are required. These are real model calls and consume subscription
usage or API credit. Dollar amounts in CLI output are list-price estimates, not a
statement of charges against a subscription.

```bash
git clone https://github.com/DietrichGebert/ponytail /tmp/total-programming-benchmark-upstream
git -C /tmp/total-programming-benchmark-upstream checkout e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156
git clone https://github.com/fastapi/full-stack-fastapi-template /tmp/total-programming-benchmark-fixture
git -C /tmp/total-programming-benchmark-fixture checkout cd83fc1

# First validate a single safety task in both arms.
python3 benchmarks/run.py \
  --upstream /tmp/total-programming-benchmark-upstream \
  --fixture /tmp/total-programming-benchmark-fixture \
  --output /tmp/total-programming-pilot --pilot --workers 2

# Then run all 152 cells: 19 tasks × 2 arms × 4 repetitions.
python3 benchmarks/run.py \
  --upstream /tmp/total-programming-benchmark-upstream \
  --fixture /tmp/total-programming-benchmark-fixture \
  --output benchmarks/runs/full --workers 3
```

Choose a new output directory for each run. Existing evidence is never overwritten.

## Results

See [`results/2026-09-18-haiku.md`](results/2026-09-18-haiku.md): on Haiku 4.5,
the principles cut delivered code 43%, cost 32%, and time 36% on the feature tier
while passing every safety gate.

The upstream scorer selftests run before any cells. The runner stops scheduling new
cells after a CLI error, missing result, permission denial, or isolation failure;
already-running cells finish. Each cell retains upstream's five-minute timeout and
has a $0.75 list-price budget cap. A stopped or budget-limited run is not a successful
benchmark result.

## Isolation and adaptations

Both arms use Claude Code's stock system prompt with the original benchmark's shared
write-code-only instruction. `--safe-mode` disables personal customizations and
CLAUDE.md discovery; empty setting sources, disabled skills, strict MCP configuration,
and an explicit file-tool allowlist add further isolation. The wrapper verifies that
the actual session init contains no plugins, skills, or MCP servers. Only Read, Write,
Edit, Glob, and Grep are exposed. Bash and other execution tools are unavailable.

The treatment appends the canonical principles (without YAML metadata) directly to
the system prompt. This deliberately tests the **principles**, not the plugin's
SessionStart activation mechanism. The baseline receives no added philosophy.
Authentication is retained; no personal Claude configuration is changed.

The original task prompts, seeds, scoring functions, source/test LOC classification,
and model ID (`claude-haiku-4-5-20251001`) are unchanged. Cell order is deterministically
shuffled to reduce arm/order confounding. Three cells run concurrently. The runner
imports upstream code from the pinned checkout instead of maintaining a fork.

## Evidence

The output directory includes:

- `manifest.json`: commits, model, CLI version, adaptations, task order, and skill hash.
- `principles.md`: the exact treatment text.
- `status.json`, `results.json`, `summary.json`: progress, raw scores, and aggregates.
- A separate workspace per cell, retaining generated code and its fixture git baseline.
- Per-cell `_invocation.json`, `_init.json`, `_events.jsonl`, `_claude.json`, and stderr.

Raw workspaces and traces are gitignored. They may contain sensitive session metadata;
inspect and redact before sharing. Results should separate pilot cells from the full run.

## Interpretation

The feature tier measures **added source lines**, not proven functionality. Upstream's
`correct=1` for a feature only means that code was added; its `safe=1` is a placeholder,
not a security test. Do not present those feature fields as correctness or safety rates.
Feature completeness requires a separate review or the upstream completeness judge.

Only the seven safety tasks execute deterministic checks against generated functions.
Even those checks are narrow floors, not a guarantee of security. Test code is tracked
separately using upstream's classifier, including its limitations.

Compare the two fresh arms, not these numbers directly against Ponytail's historical
headline: CLI behavior, platform, caching, and service performance may differ. Lower
LOC alone is not a win. This benchmark measures generation cost/time and delivered
code size—not long-term maintainability or sustained development pace.
