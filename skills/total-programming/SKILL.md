---
name: total-programming
description: Use when designing, building, refactoring, or reviewing software, UI/UX, or architecture. Apply Total Programming principles to preserve pace through agility and deliberate complexity management.
---

# Total Programming

## Preserve pace through agility

**Build software that solves complex problems without making the next move harder than it needs to be.**

Sustained pace comes from the ability to understand, change, and validate software with little friction. Keep necessary complexity manageable and remove unnecessary complexity so that each addition does not progressively limit your freedom to act.

Like Total Football, agility is not everyone moving faster independently. It comes from clear responsibilities, coordinated movement, and simple passes that keep the next move available.

**We pursue simplicity not to build less capable software, but to preserve our ability to keep improving it.** These principles apply to interfaces, interactions, code, and architecture—for humans and AI agents alike.

## 1. Start with the goal and why it matters (Intent)

Understand what someone needs to accomplish, why it matters to them, and what success looks like before choosing screens, frameworks, or functions. Communicate decisions through that goal and its reason rather than technical detail alone.

A shared goal, understood with its why, creates freedom to find the right solution: people can adapt the how without losing the what. Clarify consequential ambiguities, challenge work that does not serve the goal, and avoid confusing a proposed implementation with the underlying need.

## 2. Make understanding easy (Clarity)

Prefer clear language, familiar interactions, explicit state, and readable code over cleverness. Users should understand what they can do and what happened; maintainers should understand what the code does and why it exists.

Understanding makes confident action possible. Optimize for the next person or agent who must use, inspect, or change what you build. Brevity helps only when it preserves clarity.

## 3. Give each part a clear responsibility (Atomicity)

Organize the system into cohesive parts with small, explicit interfaces. Keep related behavior together and unnecessary dependencies apart. Like the Unix philosophy, each part should do one thing well: the smallest unit that still carries a coherent responsibility.

Clear responsibilities create freedom to act without coordinating every change across the whole system. Good boundaries make parts easier to reason about, test, replace, and remove—not merely smaller.

## 4. Prefer reversible decisions to preserve momentum (Reversibility)

Prefer choices that can be changed, replaced, or removed without rebuilding everything around them. A reversible decision keeps the next move yours.

Most decisions are two-way doors: make them quickly and let the result guide the next one. Treat one-way doors—commitments that are difficult to undo—with care, and require stronger evidence before going through. Momentum comes from acting on what you learn, not from refusing to change course. Preserve options through focused solutions and good boundaries, not speculative flexibility.

## 5. Enable upside while limiting downside (Asymmetry)

Avoid forcing every user or component through extra complexity to benefit a subset. Where appropriate, make specialized capabilities independently usable without burdening the core path.

Look for meaningful benefits with bounded costs and failure impact. This creates room to experiment, but optional does not mean free: controls, configuration, dependencies, and code still consume attention and require maintenance.

## 6. Fit the problem, not its noise (Parsimony)

Prefer the simplest solution that captures what the problem consistently requires. Details that are one-off, speculative, or specific to today’s example are noise: fitting them makes a solution brittle, not complete. When in doubt, bias toward the simpler fit—it handles the next case more gracefully than one shaped around every case you have seen.

A solution that generalizes well is not a generic one. Abstractions, settings, and frameworks for needs you have not observed are overfitting too, just to imagined data. Additional complexity must earn its place through meaningful benefits relative to its delivery and ongoing costs. Never simplify away essential security, privacy, accessibility, reliability, or data integrity—those are signal, not noise.

## 7. Tackle consequential uncertainty first (Falsification)

Identify the assumption that could invalidate the approach, and try to prove it wrong before investing heavily in work that depends on it.

Use the smallest credible prototype, usability test, technical spike, or working slice that answers the question. Prioritize uncertainty by its consequences, not by technical difficulty or interest. Learning early preserves room to change direction.

## 8. Try removing before adding (Subtraction)

When a problem appears, ask whether an unnecessary rule, step, dependency, or distinction creates it. Removing the cause can eliminate a whole chain of compensating solutions.

Consider subtraction as a real solution, not merely a cleanup activity. A simpler flow or domain model may solve more than another explanation, setting, condition, or abstraction. Less unnecessary structure means less to work around when things change.

## 9. Let evidence shape the design (Empiricism)

Treat proposed benefits as hypotheses until supported by relevant evidence. Use observed behavior, experiments, and working software to challenge expectations—not merely confirm them.

Neither popularity nor theory is sufficient proof. Compare existing and proposed approaches against the same goal, and distinguish what is observed from what is assumed. The ability to learn and adjust quickly reduces the need to be right upfront.

## 10. Reduce complexity across the whole system (Holism)

A shorter implementation is not simpler if users must do more work. A clean screen is not simpler if it hides necessary information. A quick delivery is not quick overall if it creates recurring operational work.

Count the burden wherever it lands: users, interfaces, code, data, operations, support, and maintenance. Preserve the agility of the whole rather than making one part faster at another’s expense.

## 11. Progress in small, verifiable steps (Progression)

Build toward something larger through small, complete changes rather than one elaborate solution. Each step should deliver coherent value or answer a meaningful question.

Reduce scope, not essential quality. Verify each step, let feedback choose the next, and remove scaffolding that no longer serves a purpose. When the next step is affordable, fewer decisions need settling upfront.

## Using these principles

These are guides for judgment, not mechanical rules. Their purpose is to help us make trade-offs that solve today’s problem while preserving our ability to respond to tomorrow’s.

Each principle has a one-word descriptor—Intent, Clarity, Atomicity, Reversibility, Asymmetry, Parsimony, Falsification, Subtraction, Empiricism, Holism, Progression—as shorthand for invoking it in design discussions and reviews.

When they pull in different directions, ask:

> **What is the simplest effective move we can make and validate now that preserves our freedom to make the next one?**
