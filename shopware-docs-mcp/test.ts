import { MarkdownParser } from './src/markdown-parser.js';

const DOCS_PATH = process.env.SHOPWARE_DOCS_PATH || 'C:/Users/jonas/Documents/Python/Karl & Engel/Shopware';

console.log('Testing MarkdownParser with path:', DOCS_PATH);

const parser = new MarkdownParser(DOCS_PATH);
const index = parser.buildIndex();

console.log('Files indexed:', index.files.size);
console.log('Total sections:', index.allSections.length);
console.log('Files:', Array.from(index.files.keys()).slice(0, 5));

// Test search
const results = parser.search('plugin base guide', { maxResults: 3 });
console.log('Search results for "plugin base guide":', results.length);
if (results.length > 0) {
  console.log('First result:', results[0].title);
}

// Test get_file_toc
const toc = parser.getFileToc('guides-plugins-plugins');
console.log('TOC for guides-plugins-plugins:', toc ? 'Found' : 'Not found');
