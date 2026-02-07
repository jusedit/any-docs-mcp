import { describe, it, expect } from 'vitest';
import { MarkdownParser } from '../markdown-parser.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

interface QueryCase {
  query: string;
  expectedTopTitle: string;
  expectedFile: string;
}

const DOCS_PATH = join(__dirname, '../../../tests/fixtures/search/test-docs');
const SUITE_PATH = join(__dirname, '../../../tests/fixtures/search/query-suite.json');

describe('Search Golden Suite', () => {
  const parser = new MarkdownParser(DOCS_PATH, 'test-docs');
  parser.buildIndex();

  const suite: QueryCase[] = JSON.parse(readFileSync(SUITE_PATH, 'utf-8'));

  it(`should have at least 8/10 queries match expected top result`, () => {
    let hits = 0;

    for (const { query, expectedTopTitle, expectedFile } of suite) {
      const results = parser.search(query, { maxResults: 3 });
      
      if (results.length > 0) {
        const top = results[0];
        // Check if title matches OR file matches (flexible matching)
        if (top.title.toLowerCase().includes(expectedTopTitle.toLowerCase()) ||
            top.file === expectedFile) {
          hits++;
        }
      }
    }

    expect(hits).toBeGreaterThanOrEqual(8);
    console.log(`Search golden suite: ${hits}/${suite.length} queries matched`);
  });
});
