import { describe, it, expect, beforeAll } from 'vitest';
import { MarkdownParser } from '../markdown-parser';
import { join } from 'path';

describe('find_code_examples E2E', () => {
  const fixturesPath = join(__dirname, '../../../tests/fixtures/search/test-docs');
  let parser: MarkdownParser;

  beforeAll(() => {
    parser = new MarkdownParser(fixturesPath, 'test-docs');
    parser.buildIndex();
  });

  it('finds code examples by language', () => {
    const index = parser.getIndex();
    let foundCodeBlocks: { language: string; code: string }[] = [];

    // Search for code blocks in all sections
    for (const section of index.allSections) {
      for (const block of section.codeBlocks) {
        if (block.language === 'bash' || block.language === 'javascript') {
          foundCodeBlocks.push(block);
        }
      }
    }

    expect(foundCodeBlocks.length).toBeGreaterThan(0);
  });

  it('finds code examples matching query terms', () => {
    const index = parser.getIndex();
    const results = parser.search('npm install');

    expect(results.length).toBeGreaterThan(0);
  });

  it('returns empty results for non-matching query', () => {
    const results = parser.search('xyznonexistent12345');

    expect(results.length).toBe(0);
  });
});
