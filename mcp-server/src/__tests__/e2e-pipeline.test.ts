/**
 * End-to-End Pipeline Test — Phase B (TypeScript)
 *
 * Reads .md files produced by the Python scraper (Phase A),
 * builds a MarkdownParser index, and verifies:
 *   - Index contains sections with content
 *   - Search returns relevant results
 *   - Overview, TOC, and code examples work correctly
 *
 * Env: E2E_DOCS_PATH — absolute path to scraped .md output directory
 */
import { describe, it, expect, beforeAll } from 'vitest';
import { MarkdownParser, Section, DocumentIndex } from '../markdown-parser.js';
import { existsSync, readdirSync } from 'fs';
import { join } from 'path';

const docsPath = process.env.E2E_DOCS_PATH || join(__dirname, '..', '..', '..', 'tests', 'e2e', 'scraper_output', 'e2e-testdocs', 'v1');

describe('E2E Pipeline — MCP MarkdownParser on scraped output', () => {
  let parser: MarkdownParser;
  let index: DocumentIndex;

  beforeAll(() => {
    if (!existsSync(docsPath)) {
      throw new Error(`E2E docs path does not exist: ${docsPath}. Run Phase A (Python) first.`);
    }

    const mdFiles = readdirSync(docsPath).filter(f => f.endsWith('.md'));
    if (mdFiles.length === 0) {
      throw new Error(`No .md files found in ${docsPath}. Run Phase A (Python) first.`);
    }

    console.log(`\n  📂 Loading ${mdFiles.length} .md file(s) from: ${docsPath}`);
    mdFiles.forEach(f => console.log(`     - ${f}`));

    parser = new MarkdownParser(docsPath, 'e2e-testdocs');
    index = parser.buildIndex();

    console.log(`  📊 Index: ${index.allSections.length} sections, ${index.files.size} files`);
    console.log(`  ⏱  Build time: ${parser.getLastBuildTimeMs().toFixed(0)}ms`);
  });

  // ─── Index Structure ──────────────────────────────────────────

  it('builds index with sections from scraped files', () => {
    expect(index.allSections.length).toBeGreaterThan(0);
    expect(index.files.size).toBeGreaterThan(0);
  });

  it('sections have required fields', () => {
    for (const section of index.allSections.slice(0, 10)) {
      expect(section.id).toBeTruthy();
      expect(section.file).toBeTruthy();
      expect(section.title).toBeTruthy();
      expect(typeof section.level).toBe('number');
      expect(Array.isArray(section.path)).toBe(true);
      expect(typeof section.content).toBe('string');
      expect(Array.isArray(section.codeBlocks)).toBe(true);
    }
  });

  it('index contains code blocks from the documentation', () => {
    const sectionsWithCode = index.allSections.filter(s => s.codeBlocks.length > 0);
    expect(sectionsWithCode.length).toBeGreaterThan(0);

    // Verify code blocks have language tags
    const allCodeBlocks = sectionsWithCode.flatMap(s => s.codeBlocks);
    console.log(`  📝 Found ${allCodeBlocks.length} code block(s) across ${sectionsWithCode.length} section(s)`);
    
    const languages = [...new Set(allCodeBlocks.map(cb => cb.language))];
    console.log(`  🔤 Languages: ${languages.join(', ')}`);
    expect(languages.length).toBeGreaterThan(0);
  });

  // ─── Search ───────────────────────────────────────────────────

  it('search returns results for "authentication"', () => {
    const results = parser.search('authentication');
    expect(results.length).toBeGreaterThan(0);

    // Top result should be related to authentication
    const topTitle = results[0].title.toLowerCase();
    const topContent = results[0].content.toLowerCase();
    const isRelevant = topTitle.includes('auth') || topContent.includes('auth');
    expect(isRelevant).toBe(true);
    console.log(`  🔍 "authentication" → top result: "${results[0].title}" (file: ${results[0].file})`);
  });

  it('search returns results for "Docker deployment"', () => {
    const results = parser.search('Docker deployment');
    expect(results.length).toBeGreaterThan(0);
    console.log(`  🔍 "Docker deployment" → ${results.length} result(s), top: "${results[0].title}"`);
  });

  it('search returns results for "API key"', () => {
    const results = parser.search('API key');
    expect(results.length).toBeGreaterThan(0);
    console.log(`  🔍 "API key" → ${results.length} result(s), top: "${results[0].title}"`);
  });

  it('search returns results for "npm install"', () => {
    const results = parser.search('npm install');
    expect(results.length).toBeGreaterThan(0);
    console.log(`  🔍 "npm install" → ${results.length} result(s), top: "${results[0].title}"`);
  });

  it('search returns empty for nonsense query', () => {
    const results = parser.search('xyzzy_nonexistent_term_12345');
    expect(results.length).toBe(0);
  });

  // ─── Overview ─────────────────────────────────────────────────

  it('getOverview returns structured documentation overview', () => {
    const overview = parser.getOverview();
    expect(overview.length).toBeGreaterThan(0);
    expect(overview).toContain('Documentation Overview');
    console.log(`  📋 Overview length: ${overview.length} chars`);
  });

  // ─── File List & TOC ──────────────────────────────────────────

  it('getFileList returns scraped file names', () => {
    const files = parser.getFileList();
    expect(files.length).toBeGreaterThan(0);
    console.log(`  📁 Files: ${files.join(', ')}`);
  });

  it('getFileToc returns table of contents for each file', () => {
    const files = parser.getFileList();
    for (const file of files) {
      const toc = parser.getFileToc(file);
      expect(toc).toBeTruthy();
      expect(toc!.length).toBeGreaterThan(0);
    }
    console.log(`  📑 TOC available for all ${files.length} file(s)`);
  });

  // ─── Section Retrieval ────────────────────────────────────────

  it('getSection retrieves individual sections by ID', () => {
    const sectionId = index.allSections[0].id;
    const section = parser.getSection(sectionId);
    expect(section).toBeTruthy();
    expect(section!.id).toBe(sectionId);
  });

  it('getSectionByTitle finds sections by title substring', () => {
    // Search for a title we know exists from our fixtures
    const results = parser.getSectionByTitle('Started');
    expect(results.length).toBeGreaterThan(0);
    console.log(`  🎯 getSectionByTitle("Started") → ${results.length} match(es)`);
  });

  // ─── Code Examples ────────────────────────────────────────────

  it('code blocks contain expected programming languages', () => {
    const allBlocks = index.allSections.flatMap(s => s.codeBlocks);
    const languages = new Set(allBlocks.map(b => b.language.toLowerCase()));

    // markdownify may remap language tags; check we have at least 2 distinct languages
    console.log(`  Languages found: ${[...languages].join(', ')}`);
    expect(languages.size).toBeGreaterThanOrEqual(2);
  });

  // ─── Source URLs ──────────────────────────────────────────────

  it('sections preserve source URLs from scraper output', () => {
    const withSource = index.allSections.filter(s => s.sourceUrl);
    // The scraper adds **Source:** annotations which the parser extracts
    console.log(`  🔗 ${withSource.length}/${index.allSections.length} sections have source URLs`);
    // At least some sections should have source URLs
    expect(withSource.length).toBeGreaterThan(0);
  });

  // ─── Performance ──────────────────────────────────────────────

  it('index build completes in under 1 second', () => {
    expect(parser.getLastBuildTimeMs()).toBeLessThan(1000);
  });

  it('search completes in under 50ms', () => {
    const start = performance.now();
    parser.search('authentication OAuth2 API');
    const elapsed = performance.now() - start;
    expect(elapsed).toBeLessThan(50);
    console.log(`  ⚡ Search latency: ${elapsed.toFixed(1)}ms`);
  });
});
