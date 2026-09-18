import { readPrinciples } from '../lib/principles.js';

console.log(JSON.stringify({
  hookSpecificOutput: {
    hookEventName: 'SessionStart',
    additionalContext: readPrinciples(),
  },
}));
