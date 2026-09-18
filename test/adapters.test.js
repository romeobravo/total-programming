import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { tmpdir } from 'node:os';
import { readPrinciples } from '../lib/principles.js';
import totalProgramming from '../pi-extension/index.js';

const root = new URL('../', import.meta.url);
const json = (path) => JSON.parse(readFileSync(new URL(path, root), 'utf8'));
const titles = [
  'Start with purpose, not implementation',
  'Choose the simplest solution that sufficiently solves the problem',
  'Try removing before adding',
  'Reduce complexity across the whole system',
  'Make understanding easy',
  'Give each part a clear responsibility',
  'Resolve consequential uncertainty early',
  'Let evidence correct the design',
  'Keep decisions reversible',
  'Limit downside while enabling upside',
  'Progress through small, complete, verifiable steps',
];

function handler() {
  const handlers = new Map();
  totalProgramming({ on: (event, callback) => handlers.set(event, callback) });
  assert.deepEqual([...handlers.keys()], ['before_agent_start']);
  return handlers.get('before_agent_start');
}

test('one skill contains the agreed eleven principles in order', () => {
  const text = readPrinciples();
  assert.deepEqual([...text.matchAll(/^## \d+\. (.+)$/gm)].map((m) => m[1]), titles);
  assert.ok(text.startsWith('# Total Programming'));
  assert.ok(text.includes('Preserve pace through agility'));
  assert.ok(text.includes('These are guides for judgment, not mechanical rules.'));
  assert.ok(!text.includes('description:'));
});

test('Claude hook emits the complete principles from another working directory', () => {
  const output = JSON.parse(execFileSync(process.execPath, [fileURLToPath(new URL('hooks/session-start.js', root))], { cwd: tmpdir(), encoding: 'utf8' }));
  assert.deepEqual(output, { hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: readPrinciples() } });
});

test('Pi appends full principles and preserves existing instructions', () => {
  const result = handler()({ systemPrompt: 'Existing system prompt\nAnother extension.' });
  assert.deepEqual(result, { systemPrompt: `Existing system prompt\nAnother extension.\n\n${readPrinciples()}` });
});

test('Pi does not duplicate principles when applied again', () => {
  const apply = handler();
  const first = apply({ systemPrompt: 'Base' });
  assert.deepEqual(apply(first), first);
});

test('Pi adds principles to each independently rebuilt turn prompt', () => {
  const apply = handler();
  for (const systemPrompt of ['First turn', 'Second turn', 'After compaction']) {
    assert.equal(apply({ systemPrompt }).systemPrompt, `${systemPrompt}\n\n${readPrinciples()}`);
  }
});

test('package and plugin metadata resolve to shipped resources', () => {
  const pkg = json('package.json');
  const plugin = json('.claude-plugin/plugin.json');
  const marketplace = json('.claude-plugin/marketplace.json');
  assert.equal(pkg.version, plugin.version);
  assert.equal(plugin.name, 'total-programming');
  assert.equal(marketplace.plugins[0].name, plugin.name);
  assert.equal(marketplace.plugins[0].source, './');
  for (const path of [...pkg.pi.extensions, ...pkg.pi.skills]) {
    assert.ok(existsSync(new URL(path, root)), path);
  }
  const hook = json('hooks/hooks.json').hooks.SessionStart[0];
  assert.equal(hook.matcher, undefined); // All SessionStart sources, including compact.
  assert.equal(hook.hooks[0].command, 'node "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.js"');
});

test('Codex plugin points at the shared hook and shipped skills', () => {
  const pkg = json('package.json');
  const codex = json('.codex-plugin/plugin.json');
  assert.equal(codex.name, 'total-programming');
  assert.equal(codex.version, pkg.version);
  assert.ok(existsSync(new URL(codex.skills, root)), codex.skills);
  assert.ok(existsSync(new URL(codex.hooks, root)), codex.hooks);
  const hooks = json(codex.hooks);
  assert.equal(hooks.hooks.SessionStart[0].hooks[0].command, 'node "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.js"');
});

test('Cursor rule ships the complete principles as an always-on instruction', () => {
  const mdc = readFileSync(new URL('.cursor/rules/total-programming.mdc', root), 'utf8');
  const match = mdc.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  assert.ok(match, 'rule carries Cursor frontmatter');
  assert.match(match[1], /alwaysApply: true/);
  assert.equal(match[2].trim(), readPrinciples());
});

test('OpenCode plugin appends the principles once and registers command and skills', async () => {
  const mod = await import(fileURLToPath(new URL('.opencode/plugins/total-programming.mjs', root)));
  assert.equal(typeof mod.default, 'function');
  assert.deepEqual(Object.keys(mod).sort(), ['default']); // One plugin-shaped export: the legacy loader treats every exported function as a plugin.
  const handlers = await mod.default();
  assert.deepEqual(Object.keys(handlers).sort(), ['config', 'experimental.chat.system.transform']);

  const config = {};
  await handlers.config(config);
  assert.ok(config.command['total-programming'].template.includes('Total Programming'));
  assert.ok(config.command['total-programming'].description.length > 0);
  assert.ok(config.skills.paths.some((p) => p === path.resolve(fileURLToPath(root), 'skills')), 'skills directory registered');

  const output = { system: ['Base prompt'] };
  await handlers['experimental.chat.system.transform']({}, output);
  const expected = `Base prompt\n\n${readPrinciples()}`;
  assert.equal(output.system[0], expected);
  await handlers['experimental.chat.system.transform']({}, output);
  assert.equal(output.system[0], expected); // No duplication on a repeated transform.

  const empty = { system: [] };
  await handlers['experimental.chat.system.transform']({}, empty);
  assert.deepEqual(empty.system, [readPrinciples()]);
});

test('Hermes manifest and adapter reference the shipped skill and hook', () => {
  const pkg = json('package.json');
  const manifest = readFileSync(new URL('plugin.yaml', root), 'utf8');
  assert.match(manifest, /^name: total-programming$/m);
  assert.match(manifest, new RegExp(`^version: ${pkg.version}$`, 'm'));
  assert.match(manifest, /^  - pre_llm_call$/m);
  const adapter = readFileSync(new URL('__init__.py', root), 'utf8');
  assert.ok(adapter.includes('def register('));
  assert.ok(adapter.includes('skills" / "total-programming"') || adapter.includes('SKILL_PATH'), 'adapter resolves the bundled skill');
  assert.ok(adapter.includes('"total-programming"'));
  assert.ok(adapter.includes('SKILL.md'));
  assert.ok(adapter.includes('pre_llm_call'));
  assert.ok(!adapter.includes('register_memory_provider')); // Keeps the manifest parser from misdetecting the plugin kind.
});
