// total-programming — OpenCode plugin.
//
// Appends the Total Programming principles to every chat's system prompt and
// registers the /total-programming command and the skills directory, so the
// plugin works when installed from npm or referenced as a local file. Reuses
// the shared principles builder so Claude Code, Codex, OpenCode, Cursor, Pi,
// and Hermes all read one source of truth.
//
// OpenCode loads this as a plugin — add it to your opencode.json:
//   { "plugin": ["total-programming"] }
// or point at this file directly after cloning the repository:
//   { "plugin": ["/absolute/path/to/total-programming/.opencode/plugins/total-programming.mjs"] }

import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import { readPrinciples } from '../../lib/principles.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// The command-file parser is CommonJS; bridge to it from this ES module.
const require = createRequire(import.meta.url);
const { parseCommandFile } = require('./tp-frontmatter.cjs');

export default async () => {
  const commandDir = path.join(__dirname, '..', 'command');
  const skillsDir = path.resolve(__dirname, '..', '..', 'skills');

  return {
    // Register the /total-programming command and the skills directory.
    config: async (config) => {
      if (!config.command) config.command = {};
      try {
        for (const file of fs.readdirSync(commandDir).filter((f) => f.endsWith('.md'))) {
          const parsed = parseCommandFile(path.join(commandDir, file));
          if (parsed) config.command[path.basename(file, '.md')] = parsed;
        }
      } catch (e) {}

      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) {
        config.skills.paths.push(skillsDir);
      }
    },

    // Append the principles to the system prompt every turn, without
    // duplicating them when the transform runs again.
    'experimental.chat.system.transform': async (_input, output) => {
      const principles = readPrinciples();
      if (output.system.length > 0) {
        const last = output.system[output.system.length - 1];
        if (typeof last === 'string' && last.includes(principles)) return;
        output.system[output.system.length - 1] = `${last}\n\n${principles}`;
      } else {
        output.system.push(principles);
      }
    },
  };
};
