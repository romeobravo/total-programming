'use strict';

// total-programming command-file frontmatter parser.
//
// Pulled out of total-programming.mjs so the plugin module's only export is
// the plugin function itself. OpenCode's legacy plugin loader treats every
// function exported from a plugin module as a plugin; keeping the parser in
// its own module leaves exactly one plugin-shaped export on the .mjs.

function parseCommandFile(filePath) {
  const fs = require('fs');
  const content = fs.readFileSync(filePath, 'utf8');
  // Tolerate CRLF: a Windows checkout (autocrlf) delivers \r\n, git ships \n.
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) return null;
  const description = match[1].match(/description:\s*(.+)/)?.[1]?.trim();
  return { description, template: match[2].trim() };
}

module.exports = { parseCommandFile };
