<p align="center">
  <img src="assets/cruijff.png" width="220" alt="Total Programming logo — black-and-white line-art portrait">
</p>

<h1 align="center">Total Programming</h1>

<p align="center"><em>A team of 11 principles for attacking hard problems at a sustained pace—for humans and AI agents.</em></p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/romeobravo/total-programming?style=flat-square&color=111111&label=release" alt="Release">
  <img src="https://img.shields.io/badge/works%20with-6%20agents-111111?style=flat-square" alt="Works with 6 agents">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

<p align="center">Product Management • Product Design • Software Architecture • Software Engineering</p>

## Contents

- [Preserve pace through agility](#preserve-pace-through-agility)
- [Using these principles](#using-these-principles)
- [Benchmark](#benchmark)
- [Install](#install)
- [Local development](#local-development)
- [Uninstall](#uninstall)
- [Background](#background)

## Preserve pace through agility

**Build software that solves complex problems without making the next move harder than it needs to be.**

Sustained pace comes from the ability to understand, change, and validate software with little friction. Keep necessary complexity manageable and remove unnecessary complexity so that each addition does not progressively limit your freedom to act.

Like Total Football, agility is not everyone moving faster independently. It comes from clear responsibilities, coordinated movement, and simple passes that keep the next move available.

**We pursue simplicity not to build less capable software, but to preserve our ability to keep improving it.** These principles apply to interfaces, interactions, code, and architecture—for humans and AI agents alike.

## 1. Start with purpose, not implementation

Understand what someone needs to accomplish and what success looks like before choosing screens, frameworks, or functions. Communicate decisions through that purpose rather than technical detail alone.

A shared direction creates freedom to find the right solution. Clarify consequential ambiguities, challenge work that does not serve the goal, and avoid confusing a proposed implementation with the underlying need.

## 2. Choose the simplest solution that sufficiently solves the problem

Simplicity is a means to effectiveness, not the outcome itself. Prefer the least complex solution that delivers the intended result without compromising essential security, privacy, accessibility, reliability, or data integrity.

Additional complexity must earn its place through meaningful benefits relative to its delivery and ongoing costs. Do not sacrifice the core need for minimalism—or sacrifice future agility for completeness, elegance, or hypothetical needs.

## 3. Try removing before adding

When a problem appears, ask whether an unnecessary rule, step, dependency, or distinction creates it. Removing the cause can eliminate a whole chain of compensating solutions.

Consider subtraction as a real solution, not merely a cleanup activity. A simpler flow or domain model may solve more than another explanation, setting, condition, or abstraction. Less unnecessary structure means less to work around when things change.

## 4. Reduce complexity across the whole system

A shorter implementation is not simpler if users must do more work. A clean screen is not simpler if it hides necessary information. A quick delivery is not quick overall if it creates recurring operational work.

Count the burden wherever it lands: users, interfaces, code, data, operations, support, and maintenance. Preserve the agility of the whole rather than making one part faster at another's expense.

## 5. Make understanding easy

Prefer clear language, familiar interactions, explicit state, and readable code over cleverness. Users should understand what they can do and what happened; maintainers should understand what the code does and why it exists.

Understanding makes confident action possible. Optimize for the next person or agent who must use, inspect, or change what you build. Brevity helps only when it preserves clarity.

## 6. Give each part a clear responsibility

Organize the system into cohesive parts with small, explicit interfaces. Keep related behavior together and unnecessary dependencies apart.

Clear responsibilities create freedom to act without coordinating every change across the whole system. Good boundaries make parts easier to reason about, test, replace, and remove—not merely smaller.

## 7. Resolve consequential uncertainty early

Identify the assumption that could invalidate the approach. Test it before investing heavily in work that depends on it.

Use the smallest credible prototype, usability test, technical spike, or working slice that answers the question. Prioritize uncertainty by its consequences, not by technical difficulty or interest. Learning early preserves room to change direction.

## 8. Let evidence correct the design

Treat proposed benefits as hypotheses until supported by relevant evidence. Use observed behavior, experiments, and working software to challenge expectations—not merely confirm them.

Neither popularity nor theory is sufficient proof. Compare existing and proposed approaches against the same goal, and distinguish what is observed from what is assumed. The ability to learn and adjust quickly reduces the need to be right upfront.

## 9. Keep decisions reversible

Prefer choices that can be changed, replaced, or removed without rebuilding everything around them. Require stronger evidence for commitments that are difficult to undo.

Preserve options through focused solutions and good boundaries, not speculative flexibility. The goal is not to anticipate every future change, but to keep the cost of responding to change manageable.

## 10. Limit downside while enabling upside

Avoid forcing every user or component through extra complexity to benefit a subset. Where appropriate, make specialized capabilities independently usable without burdening the core path.

Look for meaningful benefits with bounded costs and failure impact. This creates room to experiment, but optional does not mean free: controls, configuration, dependencies, and code still consume attention and require maintenance.

## 11. Progress through small, complete, verifiable steps

Build a sequence of understandable changes toward the goal rather than one elaborate solution. Each step should deliver coherent value or answer a meaningful question.

Reduce scope, not essential quality. Verify the intended behavior, use feedback to choose the next step, and remove experiments or scaffolding that no longer serve a purpose. When the next iteration is affordable, fewer decisions need to be settled upfront.

## Using these principles

These are guides for judgment, not mechanical rules. Their purpose is to help us make trade-offs that solve today's problem while preserving our ability to respond to tomorrow's.

When they pull in different directions, ask:

> **What is the simplest effective move we can make and validate now that preserves our freedom to make the next one?**

## Benchmark

Measured with [Ponytail](https://github.com/DietrichGebert/ponytail)'s pinned agentic benchmark on **GLM 5.3 Flash** (pi harness): 228 real headless agent sessions — 19 tasks × 3 arms (clean no-skill baseline, total-programming, ponytail) × 4 repetitions — editing a real FastAPI + React repo, scored on the delivered `git diff` and adversarial safety checks. Same tasks, fixture, and scorers as Ponytail's published run. All 228 cells delivered first-attempt, no timeouts. Full method, per-task tables, and limits: [benchmarks/results/2026-10-02-glm-flash-05.md](benchmarks/results/2026-10-02-glm-flash-05.md).

| metric | baseline | total-programming | ponytail |
|---|---:|---:|---:|
| delivered | 76/76 | 76/76 | 76/76 |
| correct | 73/76 | **76/76** | 75/76 |
| safe | 74/76 | **76/76** | 75/76 |
| LOC, geo-mean vs baseline | — | 79.1% | 39.3% |
| tokens, per-task median | 25.1k | 22.5k | 11.9k |
| wall time, median | 182.5 s | 145.0 s | 65.0 s |
| safety cc_mean (lizard) | 4.68 | 3.36 | 2.64 |
| CPO judge, current value (1–5) | 3.38 | **3.75** | 3.58 |
| CPO judge, future value (1–5) | 3.25 | **3.83** | 3.83 |

Total Programming is the only arm with a perfect correctness and safety record. It builds 21% less code than the baseline, and the reframe turned its overheads negative: ~10% fewer tokens and ~20% less wall time than following no principles at all. The cut concentrates where an over-build trap exists (color picker −66%, dropzone −62%, wizard −46%) and stays a wash on irreducible work.

Every head-to-head in the table above was decided by the CPO judge: a blind, position-balanced pairwise product judge (Sonnet, anonymous A/B) that infers each solution's intent and unique capabilities, scores **current value** (core quality — an extra counts only when a plausible user need justifies it) and **future value** (change cost against neutral future scenarios, testability, over-engineering) separately, names each side's biggest risk, and cites every claim to code before giving a verdict. Under that lens Total Programming wins **17–7 over ponytail** and **13–10 with one tie over the baseline**: terse wrappers lose points on robustness and silent regressions, while documented contracts and named validation rules count as justified extras.

Caveats: single run, model, and judge; only the within-run arm comparisons are controlled; the judge covers the six front-end tasks (24 pairs per comparison).

## Install

Requires Claude Code, Codex, OpenCode, Cursor, Pi, or Hermes Agent. No runtime dependencies, build step, or API keys of its own. The Claude Code, Codex, and Pi adapters additionally need Node.js 20+ on your PATH; the Hermes adapter needs Python 3.10+ (already required by Hermes).

### Claude Code

Send these as **two separate commands** in Claude Code:

```text
/plugin marketplace add romeobravo/total-programming
```

```text
/plugin install total-programming@total-programming
```

Restart Claude Code. The plugin adds the full principles as context on session start, including resume, clear, and compaction. You can also invoke the skill explicitly:

```text
/total-programming:total-programming
```

### Codex

Send these as **two separate commands** in Codex:

```text
codex plugin marketplace add romeobravo/total-programming
```

```text
codex plugin add total-programming@total-programming
```

Restart Codex. The plugin points at the same hook and skills as Claude Code, so the principles also arrive on resume, clear, and compaction.

### OpenCode

Clone the repository, then add the plugin file to `opencode.json`:

```json
{ "plugin": ["/absolute/path/to/total-programming/.opencode/plugins/total-programming.mjs"] }
```

Keep the clone in place. The plugin appends the full principles to the system prompt every turn, registers `/total-programming` as a command, and exposes the skills directory to OpenCode.

### Cursor

Copy the always-on rule into your project:

```bash
mkdir -p .cursor/rules
cp /absolute/path/to/total-programming/.cursor/rules/total-programming.mdc .cursor/rules/
```

Or fetch it without cloning:

```bash
mkdir -p .cursor/rules
curl -o .cursor/rules/total-programming.mdc https://raw.githubusercontent.com/romeobravo/total-programming/main/.cursor/rules/total-programming.mdc
```

Cursor picks the rule up on the next request. It is instruction-only: no commands, no hooks.

### Pi

```bash
pi install git:github.com/romeobravo/total-programming
```

Restart Pi, or use `/reload` in an existing session. The extension appends the full principles to the system prompt before each agent run, without replacing existing instructions. You can also invoke the skill explicitly:

```text
/skill:total-programming
```

### Hermes Agent

```bash
hermes plugins install romeobravo/total-programming --enable
```

Restart Hermes after installing. The plugin injects the full principles before each LLM turn, registers the skill as `total-programming:total-programming`, and adds `/total-programming [on|off]` to switch injection (default on; runtime state is process-local, so it resets on restart). Set the `TOTAL_PROGRAMMING_ENABLED` env var to `0`/`1` for a persistent default.

## Local development

Clone the repository wherever you keep your projects:

```bash
git clone https://github.com/romeobravo/total-programming.git
cd total-programming
```

Try Claude Code with the local plugin for one session, without installing it:

```bash
claude --plugin-dir .
```

Or install the checkout in Pi:

```bash
pi install "$PWD"
```

Pi references the local checkout directly; keep it in place. Edits to the principles are picked up on the next agent run. Claude Code's installed plugin may be cached: use `--plugin-dir` during development to load the working checkout directly.

Edit the skill, then run:

```bash
npm test
claude plugin validate .
```

No `npm install` is needed. Tests check all eleven headings, both adapters, prompt preservation, repeat application, and package paths. The Claude hook works independently of the current working directory.

### Skill only (no automatic injection)

If you prefer on-demand guidance, symlink the skill directory into your agent's personal skill directory instead of installing the plugin/package. Run the appropriate commands **from the repository root**. Do not overwrite an existing skill with the same name.

Claude Code:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/total-programming" "$HOME/.claude/skills/total-programming"
```

Pi:

```bash
mkdir -p ~/.pi/agent/skills
ln -s "$PWD/skills/total-programming" "$HOME/.pi/agent/skills/total-programming"
```

Invoke `/total-programming` in Claude Code or `/skill:total-programming` in Pi. Skill-only installation makes the guidance available; it does **not** guarantee the complete text is loaded automatically on every task. Keep the checkout in place while using these links.

## Uninstall

| Host | Command |
|------|---------|
| Claude Code | `/plugin uninstall total-programming@total-programming`; optionally also `/plugin marketplace remove total-programming` |
| Codex | `codex plugin remove total-programming@total-programming`; optionally also `codex plugin marketplace remove total-programming` |
| OpenCode | Remove the plugin entry from `opencode.json`; delete the clone if you no longer want it |
| Cursor | Delete the copied rule: `rm .cursor/rules/total-programming.mdc` |
| Pi | `pi remove git:github.com/romeobravo/total-programming` (a local install: `pi remove /absolute/path/to/total-programming`) |
| Hermes Agent | `hermes plugins remove romeobravo/total-programming` |
| Skill-only installs | Remove the symlink you created: `rm ~/.claude/skills/total-programming` and/or `rm ~/.pi/agent/skills/total-programming` |

These remove everything the plugin or rule added — none of the adapters write state outside their own files, so nothing else is left behind. Restart the host afterwards so the loaded copy goes away.

## Background

By Ruben Buitelaar, building on [What if Johan Cruyff Was a Software Engineer?](https://medium.com/@rubenbuitelaar/what-if-johan-cruyff-was-a-software-engineer-237d22da5bb?sk=527a69571726edc74f1dd263a1509f63) and his work on tackling complexity.

Packaging inspired by [Ponytail](https://github.com/DietrichGebert/ponytail); implementation and principles are independent.
