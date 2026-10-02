# GLM 5.3 Flash — pi harness, complete dataset (2026-10-02)

Final report for the 2026-09-26 GLM 5.3 Flash run (pi coding agent harness,
`--runner pi --provider zai-coding`): 228 cells = 19 tasks × 3 arms
(baseline, total-programming, ponytail) × 4 repetitions, every cell now
delivered. This supersedes `2026-09-30-glm-flash.md`, which was computed
while 14 cells (7 baseline, 7 Total Programming) still had no deliverable
after the timeout-rerun ladder (300 s → 600 s → 1200 s).

Those cells were regenerated on 2026-10-02 after fixing the harness: pi's
json mode streams a full message snapshot (incl. thinking-so-far) with every
streaming delta, so on a reasoning model the event trace grew quadratically
with thinking length (250–620 MB cells; all 19 stuck cells turned out to be
events-cap guard kills, not wall-time timeouts). The runner now routes
`message_update` snapshots to a one-slot sidecar and appends everything else
to the trace (commit `b7371ef`); traces stay kilobyte-sized and no rerun cell
was killed or timed out. Timeout caps no longer influence any number below.

## Delivery

| arm | delivered | correct | safe |
|---|---|---|---|
| baseline | 76/76 | 75/76 | 76/76 |
| total-programming | 76/76 | 76/76 | 76/76 |
| ponytail | 76/76 | 76/76 | 76/76 |

The single correctness miss is a scorer artifact, not a real failure:
`sql-user` baseline rep 2 delivers a correctly parameterized query but sets
`cursor.row_factory = sqlite3.Row`, and the scorer's `"alice" in str(row)`
check cannot see through a `sqlite3.Row` repr.

## Delivered LOC (paired per task, median per repetition set, all 19 tasks)

| arm | geometric mean vs baseline |
|---|---|
| total-programming | 78% |
| ponytail | 40% |

## Cost and time (median per valid run)

| arm | tokens in+out | wall time |
|---|---|---|
| baseline | 23.2 k | 192 s |
| total-programming | 24.0 k | 179 s |
| ponytail | 12.5 k | 92 s |

On the complete dataset Total Programming spends ~3% more tokens than
baseline and finishes slightly faster; the +20% token overhead in the
partial report was an artifact of the missing big-task cells.

## Cyclomatic complexity (lizard, all 12 feature + 7 safety tasks, full cohort)

Mean of per-task medians per function:

| arm | feature: n_fn | feature: cc mean / max | safety: cc mean / max |
|---|---|---|---|
| baseline | 16.3 | 2.76 / 6.5 | 5.11 / 5.9 |
| total-programming | 14.6 | 2.60 / 5.3 | 3.52 / 4.1 |
| ponytail | 7.5 | 2.23 / 3.5 | 2.25 / 2.6 |

Total Programming's signature safety-task simplification (−31% CC vs
baseline) stands; ponytail is structurally simplest everywhere (no function
above CC 3.5).

## Blind readability judge (Sonnet, anonymous A/B, position-balanced)

All 24 pairs per matchup now have source on both sides — no walkovers, no
exclusions. Pairs score both solutions 1–5 and pick a preference.

- **Total Programming vs baseline: 14–8 for Total Programming** (2 ties).
  Mean scores 3.75 vs 3.46. Per task: rating 3–0 (1 tie), datepicker 3–0
  (1 tie), command 3–1, colorpicker 2–2, dropzone 2–2, wizard 1–3.
- **Ponytail vs Total Programming: 15–7 for ponytail** (2 ties). Mean
  scores 3.92 vs 3.33. Per task: datepicker 4–0, command 3–1, rating 2–1
  (1 tie), wizard 2–1 (1 tie), colorpicker 2–2, dropzone 2–2.

For reference, the partial-dataset report said 11–7 and 19–3, but those
tallies counted walkover wins where one side had delivered nothing (9 of
ponytail's 19 wins); code-only counting on the half dataset gave 7–4 and
10–3. The complete dataset makes every pair a fair comparison and lands
between those readings: Total Programming's edge over baseline grows to
14–8, ponytail's lead is real but moderate at 15–7.

## Reading

With every cell delivered, the story sharpens rather than changes. On a
much stronger model the baseline already builds fairly lean (TP −22% LOC),
and Total Programming's judgment overhead all but disappears in tokens
(+3%) and wall time (slightly faster than baseline) while keeping its
safety-task simplification (−31% CC) and a real blind-readability edge
(14–8). Ponytail's mechanical minimalism remains the strongest single
profile at this tier — complete delivery, −60% LOC, lowest complexity,
fastest and cheapest, and a 15–7 blind win driven by tasks where a native
wrapper is simply the better answer (datepicker 4–0) — but it is a 2:1
margin on honest pairs, not the 6:1 the walkover tallies suggested.

Caveats: single run, single model, one judge model (Sonnet); the Haiku runs
used the Claude Code harness, so Haiku-vs-GLM differences conflate model
tier with harness; ponytail's skill text was appended raw including its
YAML frontmatter (same method across arms, so arms are comparable within
the run); timeout caps are arbitrary but no longer affect any result.
