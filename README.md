<p align="center">
  <img src="assets/cruijff.png" width="220" alt="Total Programming logo — black-and-white line-art portrait">
</p>

<h1 align="center">Total Programming</h1>

<p align="center"><em>Preserve pace through agility.</em></p>

Build software that solves complex problems without making the next move harder than it needs to be. Like Total Football, sustained pace comes from clear responsibilities, coordinated movement, and simple passes that keep the next move available.

Eleven guiding principles for UI/UX, programming, and architecture—for humans and AI agents. Not a rigid workflow, code-golf prompt, or permission to cut essential quality.

## Contents

- [The principles](#the-principles)
- [Benchmark](#benchmark)
- [Install](#install)
- [How it works](#how-it-works)
- [Local development](#local-development)
- [Uninstall](#uninstall)
- [Background](#background)

## The principles

1. [Start with purpose, not implementation](#1-start-with-purpose-not-implementation--intent) — *Intent*
2. [Fit the problem, not its noise](#2-fit-the-problem-not-its-noise--parsimony) — *Parsimony*
3. [Try removing before adding](#3-try-removing-before-adding--subtraction) — *Subtraction*
4. [Reduce complexity across the whole system](#4-reduce-complexity-across-the-whole-system--holism) — *Holism*
5. [Make understanding easy](#5-make-understanding-easy--clarity) — *Clarity*
6. [Give each part a clear responsibility](#6-give-each-part-a-clear-responsibility--atomicity) — *Atomicity*
7. [Discover what could invalidate the approach first](#7-discover-what-could-invalidate-the-approach-first--falsification) — *Falsification*
8. [Let evidence correct the design](#8-let-evidence-correct-the-design--empiricism) — *Empiricism*
9. [Keep decisions reversible to preserve momentum](#9-keep-decisions-reversible-to-preserve-momentum--reversibility) — *Reversibility*
10. [Limit downside while enabling upside](#10-limit-downside-while-enabling-upside--asymmetry) — *Asymmetry*
11. [Progress through small, complete, verifiable steps](#11-progress-through-small-complete-verifiable-steps--progression) — *Progression*

The agent-facing text lives in [`SKILL.md`](skills/total-programming/SKILL.md), which is the single source of truth. Below, each principle is paired with a Johan Cruyff quote, where it comes from on the pitch, and why it belongs in software.

### 1. Start with purpose, not implementation — *Intent*

> "I hate someone who moves but doesn't know where to."

**On the pitch.** In Total Football, movement without the ball only helps when it serves the shared plan: every run creates space for a teammate or an option for the pass. A player running without direction pulls the team's shape apart.

**In software.** Know what someone needs to accomplish and what success looks like before choosing screens, frameworks, or functions. A shared intent lets people work independently and still converge. Without it, activity looks like progress while the system drifts apart.

### 2. Fit the problem, not its noise — *Parsimony*

> "Football is simple. Playing simple football is hard."

**On the pitch.** Cruyff's teams won through sequences of simple, well-timed passes rather than one brilliant manoeuvre. The hard part is the discipline to choose the simple option when a spectacular one is available.

**In software.** Our natural tendency is to overfit: to shape a solution around every edge case, request, and hypothetical need in front of us. A parsimonious solution captures what the problem consistently requires and ignores the noise, which is exactly why it handles the next case better. Building for needs nobody has observed is overfitting too, just to imagined data.

### 3. Try removing before adding — *Subtraction*

> "Quality isn't running a lot; it's being in the right place at the right moment."

**On the pitch.** A player who reads the game runs less, not more. Good positioning removes the need to chase; effort spent compensating for poor positioning is effort wasted.

**In software.** Many problems are symptoms of an unnecessary rule, step, dependency, or distinction. Removing the cause eliminates the whole chain of compensating solutions: the extra setting, the explanatory tooltip, the special case. Subtraction is a solution, not a cleanup chore.

### 4. Reduce complexity across the whole system — *Holism*

> "If you're not somewhere, you're either too early or too late."

**On the pitch.** In Total Football, a player's position only makes sense relative to the whole team. Being in the wrong place is never a local error: it leaves a gap that someone else has to cover.

**In software.** A shorter implementation is not simpler if users must do more work, and a quick delivery is not quick if it creates recurring operational work. Count the burden wherever it lands: users, interfaces, code, data, operations, support, and maintenance. Moving complexity somewhere else is not removing it.

### 5. Make understanding easy — *Clarity*

> "If I had wanted you to understand it, I would have explained it better."

**On the pitch.** Cruyff was famous for cryptic one-liners, known in Dutch as *Cruijffiaans*, that people still debate decades later. Charming from a football legend.

**In software.** Costly anywhere else. Read the quote as a warning. Users should understand what they can do and what happened; maintainers should understand what the code does and why it exists. The next person or agent who must change your work should not need an oracle.

### 6. Give each part a clear responsibility — *Atomicity*

> "I'm the worst if I have to defend the whole garden, but I'm the best if I have to defend this part. Everything is about space, nothing more."

**On the pitch.** Zonal defending: each player is responsible for a defined space, so the team defends as a coordinated unit instead of everyone chasing the ball.

**In software.** Like the Unix philosophy, each part should do one thing well. Small, explicit interfaces and clear responsibilities let you change, test, replace, or remove a part without coordinating every change across the whole system. Atomic does not mean tiny; it means the smallest unit that still carries a coherent responsibility.

### 7. Discover what could invalidate the approach first — *Falsification*

> "The truth is never exactly as you expect it will be."

**On the pitch.** Pressing. Cruyff's teams hunted the ball high up the pitch, because winning it back near the opponent's goal is cheap, and defending in your own box is expensive.

**In software.** Uncertainty works the same way. Confront the assumption that could invalidate your approach while being wrong still costs a spike, not a rebuild. Try to prove it wrong with the smallest credible prototype, test, or working slice, and rank uncertainty by its consequences, not by technical difficulty or interest.

### 8. Let evidence correct the design — *Empiricism*

> "Every disadvantage has its advantage."

**On the pitch.** Cruyff's most famous line. A setback reveals something you could not see before, and the team that adjusts to it gains the edge.

**In software.** Treat proposed benefits as hypotheses. Observed behavior, experiments, and working software should correct your expectations, especially when they disagree with you. A failed assumption is often the most valuable thing you learn, if you let it change the design. Neither popularity nor theory is proof.

### 9. Keep decisions reversible to preserve momentum — *Reversibility*

> "If we have the ball, they can't score."

**On the pitch.** Possession. As long as you keep the ball, you decide the next move and the opponent can only react. Lose it, and the initiative is theirs.

**In software.** A reversible decision keeps the next move yours; an irreversible one gives the ball away. Prefer choices that can be changed, replaced, or removed without rebuilding everything around them, and require stronger evidence for commitments that are hard to undo. Momentum comes from acting on what you learn, not from refusing to change course.

### 10. Limit downside while enabling upside — *Asymmetry*

> "If you can't win, make sure you don't lose."

**On the pitch.** Knowing when to secure the result. When the win is not on, protecting against the loss keeps you in the game for the next opportunity.

**In software.** Look for meaningful benefits with bounded costs and failure impact. Do not force every user or component through extra complexity to benefit a subset; make specialized capabilities independently usable without burdening the core path. Bounded downside is what makes experimentation affordable, but optional never means free.

### 11. Progress through small, complete, verifiable steps — *Progression*

> "You will understand it when you get it."

**On the pitch.** Build-up play: progressing the ball through short passes that each keep possession and open the next option, rather than gambling on one long ball.

**In software.** Build a sequence of small, complete, verifiable changes rather than one elaborate solution. Each step delivers coherent value or answers a meaningful question, and builds toward something larger. Understanding follows the step: when the next iteration is affordable, fewer decisions need to be settled upfront. Reduce scope, never essential quality.

### When principles pull in different directions

> **What is the simplest effective move we can make and validate now that preserves our freedom to make the next one?**

## Benchmark

Measured with [Ponytail](https://github.com/DietrichGebert/ponytail)'s pinned agentic benchmark: real headless Claude Code sessions (Haiku 4.5, 19 tasks × 2 arms × 4 runs) editing a real FastAPI + React repo, scored on the delivered `git diff` and adversarial safety checks. Same tasks, fixture, and scorers as Ponytail's published run.

| vs clean no-skill baseline | LOC | tokens | cost | time | safe |
|---|---:|---:|---:|---:|---:|
| ponytail (their run) | **−54%** | −22% | −20% | −27% | 100% |
| total-programming (this run) | −43% | **−26%** | **−32%** | **−36%** | **100%** |

The principles cut code most where an over-build trap exists (color picker −68%, star rating −64%) and are a wash on irreducible code. They never forced the one-liner: the date picker still legitimately used Radix. All 28/28 adversarial safety checks passed — including the path-traversal guard a bare "prefer one-liners" prompt drops.

Rows are from separate runs on different days; each is valid against its own baseline. Full method, per-task tables, and limits: [benchmarks/results/2026-09-18-haiku.md](benchmarks/results/2026-09-18-haiku.md).

Results were measured on the v0.2.0 wording. Principles 2, 6, 7, 9 and 11 have since been refined and the descriptors added; these changes have not yet been re-measured.

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

## How it works

- `skills/total-programming/SKILL.md` is the single source of truth.
- `hooks/session-start.js` supplies the same text to Claude Code as session context, and `.codex-plugin/plugin.json` points Codex at the same hook and skills.
- `pi-extension/index.js` appends it to Pi's existing system prompt.
- `.opencode/plugins/total-programming.mjs` appends it to OpenCode's system prompt every turn and registers `/total-programming`.
- `.cursor/rules/total-programming.mdc` is the instruction-only Cursor rule.
- `plugin.yaml` and `__init__.py` inject it into Hermes Agent before each LLM call and register the skill and `/total-programming`.
- All adapters strip the skill's YAML metadata; none modifies project instruction files, changes tool permissions, or calls a network service.

The principles guide judgment rather than enforce behavior. Installing them does not guarantee model compliance or prove an improvement in development speed.

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

Claude Code:

```text
/plugin uninstall total-programming@total-programming
```

Pi, when installed from GitHub:

```bash
pi remove git:github.com/romeobravo/total-programming
```

For a local Pi installation, run `pi remove /absolute/path/to/total-programming` with your checkout's path. For a skill-only installation, remove only the symlink you created.

## Background

By Ruben Buitelaar, building on [What if Johan Cruyff Was a Software Engineer?](https://medium.com/@rubenbuitelaar/what-if-johan-cruyff-was-a-software-engineer-237d22da5bb?sk=527a69571726edc74f1dd263a1509f63) and his work on tackling complexity.

Packaging inspired by [Ponytail](https://github.com/DietrichGebert/ponytail); implementation and principles are independent.

Cruyff quotes are translated from Dutch, some loosely to convey their intent. Like most *Cruijffiaans*, they circulate in several versions.
