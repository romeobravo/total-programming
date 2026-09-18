import { readPrinciples } from '../lib/principles.js';

export default function totalProgramming(pi) {
  pi.on('before_agent_start', (event) => {
    const principles = readPrinciples();
    return {
      systemPrompt: event.systemPrompt.includes(principles)
        ? event.systemPrompt
        : `${event.systemPrompt}\n\n${principles}`,
    };
  });
}
