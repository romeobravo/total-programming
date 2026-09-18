import { readFileSync } from 'node:fs';

// The skill is the single source of truth for humans and both agent adapters.
export function readPrinciples() {
  const skill = readFileSync(new URL('../skills/total-programming/SKILL.md', import.meta.url), 'utf8');
  return skill.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();
}
