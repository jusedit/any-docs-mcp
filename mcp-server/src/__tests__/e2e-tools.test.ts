import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { MarkdownParser } from '../markdown-parser';
import { join } from 'path';

describe('get_overview and get_file_toc E2E', () => {
  const fixturesPath = join(__dirname, '../../../tests/fixtures/search/test-docs');
  let parser: MarkdownParser;

  beforeAll(() => {
    parser = new MarkdownParser(fixturesPath, 'test-docs');
    parser.buildIndex();
  });

  it('getOverview returns file list with top-level sections', () => {
    const overview = parser.getOverview();
    
    expect(overview).toContain('#');
    expect(overview).toContain('Documentation Overview');
    // Should contain fixture file names
    expect(overview.length).toBeGreaterThan(0);
  });

  it('getFileToc returns heading hierarchy for known file', () => {
    const toc = parser.getFileToc('getting-started');
    
    expect(toc).toBeDefined();
    expect(toc).toContain('- ');  // List format
    expect(toc).toContain('Getting Started');
  });

  it('getFileToc returns undefined for non-existent file', () => {
    const toc = parser.getFileToc('non-existent-file');
    
    expect(toc).toBeUndefined();
  });

  it('getFileList returns all files', () => {
    const files = parser.getFileList();
    
    expect(files.length).toBeGreaterThan(0);
    expect(files).toContain('getting-started');
    expect(files).toContain('api-reference');
  });
});
