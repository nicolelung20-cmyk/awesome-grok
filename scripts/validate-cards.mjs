// Validates cards/agents.json so every agent card has the fields the gallery renders.
import { readFileSync } from 'node:fs';

const agents = JSON.parse(readFileSync(new URL('../cards/agents.json', import.meta.url), 'utf8'));
const categories = new Set(['Apps and Agents', 'CLI']);
const errors = [];
const names = new Set();

agents.forEach((a, i) => {
  const at = `#${i} (${a.name ?? 'unnamed'})`;
  for (const key of ['name', 'url', 'category', 'description']) {
    if (typeof a[key] !== 'string' || !a[key].trim()) errors.push(`${at}: missing "${key}"`);
  }
  if (a.url && !/^https:\/\//.test(a.url)) errors.push(`${at}: url must be https`);
  if (a.category && !categories.has(a.category)) errors.push(`${at}: unknown category "${a.category}"`);
  if (a.tags && !(Array.isArray(a.tags) && a.tags.every(t => typeof t === 'string'))) errors.push(`${at}: tags must be strings`);
  if (names.has(a.name)) errors.push(`${at}: duplicate name`);
  names.add(a.name);
});

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}
console.log(`${agents.length} agent cards OK`);
