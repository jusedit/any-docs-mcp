import { MarkdownParser } from './src/markdown-parser.js';

const DOCS_PATH = 'C:/Users/jonas/Documents/Python/Karl & Engel/Shopware';

console.log('=== Shopware Docs MCP Server Test ===\n');

const parser = new MarkdownParser(DOCS_PATH);
const index = parser.buildIndex();

console.log(`✓ Files indexed: ${index.files.size}`);
console.log(`✓ Total sections: ${index.allSections.length}`);

// Test 1: Search for "plugin base guide"
console.log('\n--- Test 1: Search "plugin base guide" ---');
const results1 = parser.search('plugin base guide', { maxResults: 3 });
console.log(`Found ${results1.length} results:`);
for (const r of results1) {
  console.log(`  - [${r.file}] ${r.path.join(' > ')} > ${r.title}`);
}

// Test 2: Search for "create plugin"
console.log('\n--- Test 2: Search "create plugin" ---');
const results2 = parser.search('create plugin', { maxResults: 3 });
console.log(`Found ${results2.length} results:`);
for (const r of results2) {
  console.log(`  - [${r.file}] ${r.title}`);
}

// Test 3: Get file TOC
console.log('\n--- Test 3: File TOC for guides-plugins-plugins ---');
const toc = parser.getFileToc('guides-plugins-plugins');
if (toc) {
  const lines = toc.split('\n').slice(0, 10);
  console.log(lines.join('\n'));
  console.log('  ...');
}

// Test 4: Get section by title
console.log('\n--- Test 4: Get section "Create your first plugin" ---');
const sections = parser.getSectionByTitle('Create your first plugin');
if (sections.length > 0) {
  const s = sections[0];
  console.log(`Title: ${s.title}`);
  console.log(`File: ${s.file}`);
  console.log(`Path: ${s.path.join(' > ')}`);
  console.log(`Code blocks: ${s.codeBlocks.length}`);
  console.log(`Content preview: ${s.content.substring(0, 200)}...`);
}

// Test 5: Find code examples
console.log('\n--- Test 5: Find code examples for "Plugin" ---');
const codeMatches: { title: string; lang: string }[] = [];
for (const section of index.allSections) {
  for (const block of section.codeBlocks) {
    if (block.code.toLowerCase().includes('plugin')) {
      codeMatches.push({ title: section.title, lang: block.language });
      if (codeMatches.length >= 5) break;
    }
  }
  if (codeMatches.length >= 5) break;
}
console.log(`Found ${codeMatches.length} code examples:`);
for (const m of codeMatches) {
  console.log(`  - [${m.lang}] ${m.title}`);
}

console.log('\n=== All tests completed ===');
