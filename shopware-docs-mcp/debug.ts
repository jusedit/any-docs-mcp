import { readFileSync } from 'fs';

const filePath = 'C:/Users/jonas/Documents/Python/Karl & Engel/Shopware/guides-plugins-plugins.md';
const content = readFileSync(filePath, 'utf-8');
const lines = content.split('\n');

console.log('First 20 lines:');
for (let i = 0; i < 20; i++) {
  const line = lines[i];
  const headingMatch = line.match(/^(#{1,6})\s+(.+)$/);
  console.log(`Line ${i}: "${line.substring(0, 60)}" -> Match: ${headingMatch ? headingMatch[2] : 'NO'}`);
}
