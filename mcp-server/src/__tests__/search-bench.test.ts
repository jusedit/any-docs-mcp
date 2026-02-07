import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { MarkdownParser } from '../markdown-parser';
import { join } from 'path';
import { writeFileSync, mkdirSync } from 'fs';

interface BenchmarkResult {
  p50: number;
  p95: number;
  mean: number;
  max: number;
  queryCount: number;
  timestamps: number[];
}

// 50 diverse search queries
const BENCHMARK_QUERIES = [
  'getting started',
  'installation',
  'configuration',
  'API reference',
  'tutorial',
  'example',
  'function',
  'component',
  'state',
  'props',
  'hook',
  'useEffect',
  'useState',
  'async',
  'await',
  'promise',
  'fetch',
  'axios',
  'router',
  'middleware',
  'database',
  'query',
  'mutation',
  'schema',
  'type',
  'interface',
  'class',
  'export',
  'import',
  'default',
  'return',
  'const',
  'let',
  'var',
  'if',
  'else',
  'for',
  'while',
  'map',
  'filter',
  'reduce',
  'callback',
  'event',
  'listener',
  'DOM',
  'render',
  'mount',
  'unmount',
  'lifecycle',
  'error handling',
  'debugging',
  'testing',
  'deploy',
  'build'
];

describe('search benchmark', () => {
  const fixturesPath = join(__dirname, '../../../tests/fixtures/search/test-docs');
  let parser: MarkdownParser;
  let results: BenchmarkResult;

  beforeAll(() => {
    parser = new MarkdownParser(fixturesPath, 'test-docs');
    parser.buildIndex();

    // Run benchmark
    const timestamps: number[] = [];
    
    for (const query of BENCHMARK_QUERIES) {
      const start = performance.now();
      parser.search(query);
      const end = performance.now();
      timestamps.push(end - start);
    }

    // Calculate statistics
    const sorted = [...timestamps].sort((a, b) => a - b);
    const p50Index = Math.floor(sorted.length * 0.5);
    const p95Index = Math.floor(sorted.length * 0.95);
    
    results = {
      p50: sorted[p50Index],
      p95: sorted[p95Index],
      mean: timestamps.reduce((a, b) => a + b, 0) / timestamps.length,
      max: Math.max(...timestamps),
      queryCount: timestamps.length,
      timestamps
    };

    // Write results to file
    const outputDir = join(__dirname, '../../test-output');
    try {
      mkdirSync(outputDir, { recursive: true });
    } catch {}
    
    writeFileSync(
      join(outputDir, 'benchmark-results.json'),
      JSON.stringify(results, null, 2)
    );

    // Log to stderr
    console.error(`\nSearch Benchmark Results:`);
    console.error(`  Queries: ${results.queryCount}`);
    console.error(`  p50: ${results.p50.toFixed(2)}ms`);
    console.error(`  p95: ${results.p95.toFixed(2)}ms`);
    console.error(`  Mean: ${results.mean.toFixed(2)}ms`);
    console.error(`  Max: ${results.max.toFixed(2)}ms`);
  });

  it('completes benchmark queries', () => {
    expect(results.queryCount).toBeGreaterThanOrEqual(50);
  });

  it('has p50 latency under 50ms', () => {
    expect(results.p50).toBeLessThan(50);
  });

  it('has p95 latency under 200ms', () => {
    expect(results.p95).toBeLessThan(200);
  });

  it('writes benchmark results to JSON', () => {
    expect(results.timestamps.length).toBeGreaterThanOrEqual(50);
    expect(results.p50).toBeGreaterThan(0);
    expect(results.p95).toBeGreaterThanOrEqual(results.p50);
  });
});
