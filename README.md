<p align="center">
  <img src="assets/cruijff.png" width="220" alt="Total Programming logo — black-and-white line-art portrait">
</p>

<h1 align="center">Total Programming</h1>

<p align="center"><em>Preserve pace through agility.</em></p>

Build software that solves complex problems without making the next move harder than it needs to be. Like Total Football, sustained pace comes from clear responsibilities, coordinated movement, and simple passes that keep the next move available.

Eleven guiding principles for UI/UX, programming, and architecture—for humans and AI agents. Not a rigid workflow, code-golf prompt, or permission to cut essential quality.

**[Read the complete principles →](skills/total-programming/SKILL.md)**

## Install

Requires Node.js 20+ on your PATH and Claude Code or Pi. No runtime dependencies, build step, or API keys of its own.

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

### Pi

```bash
pi install git:github.com/romeobravo/total-programming
```

Restart Pi, or use `/reload` in an existing session. The extension appends the full principles to the system prompt before each agent run, without replacing existing instructions. You can also invoke the skill explicitly:

```text
/skill:total-programming
```

## How it works

- `skills/total-programming/SKILL.md` is the single source of truth.
- `hooks/session-start.js` supplies the same text to Claude Code as session context.
- `pi-extension/index.js` appends it to Pi's existing system prompt.
- Both adapters strip the skill's YAML metadata; neither modifies project instruction files, changes tool permissions, or calls a network service.

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
