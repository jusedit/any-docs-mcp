/**
 * Real-World MCP Evaluation Script
 *
 * Called by the Python quality benchmark via subprocess.
 * Reads JSON from stdin: { docsPath, docName, queries }
 * Outputs JSON to stdout with index, search, and overview metrics.
 */
import { MarkdownParser } from '../markdown-parser.js';
import { readFileSync, readdirSync } from 'fs';

interface Query {
  doc_name: string;
  query: string;
  expected_top_title: string;
  expected_file: string;
  query_type: string;
}

interface EvalInput {
  docsPath: string;
  docName: string;
  queries: Query[];
}

async function main() {
  // Read input from stdin
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const input: EvalInput = JSON.parse(Buffer.concat(chunks).toString('utf-8'));

  const { docsPath, docName, queries } = input;

  // Verify path has .md files
  let mdFiles: string[];
  try {
    mdFiles = readdirSync(docsPath).filter(f => f.endsWith('.md'));
  } catch {
    console.log(JSON.stringify({ error: `Cannot read ${docsPath}` }));
    process.exit(0);
  }

  if (mdFiles.length === 0) {
    console.log(JSON.stringify({ error: `No .md files in ${docsPath}` }));
    process.exit(0);
  }

  // Build index
  const parser = new MarkdownParser(docsPath, docName);
  const index = parser.buildIndex();
  const buildTimeMs = parser.getLastBuildTimeMs();

  // Index metrics
  const sectionsWithCode = index.allSections.filter(s => s.codeBlocks.length > 0).length;
  const sectionsWithSourceUrl = index.allSections.filter(s => s.sourceUrl).length;
  const totalContentLength = index.allSections.reduce((sum, s) => sum + s.content.length, 0);
  const avgContentLength = index.allSections.length > 0
    ? totalContentLength / index.allSections.length
    : 0;

  // Search evaluation
  let precisionAt1Hits = 0;
  let precisionAt3Hits = 0;
  let reciprocalRankSum = 0;
  let zeroResultQueries = 0;
  const queriesTested = queries.length;

  for (const q of queries) {
    const results = parser.search(q.query, { maxResults: 10 });

    if (results.length === 0) {
      zeroResultQueries++;
      continue;
    }

    // Check precision@1: is the top result's title a match?
    const topTitle = results[0].title.toLowerCase();
    const expectedTitle = q.expected_top_title.toLowerCase();

    if (topTitle.includes(expectedTitle) || expectedTitle.includes(topTitle)) {
      precisionAt1Hits++;
    }

    // Check precision@3: is the expected title in top 3?
    const top3Titles = results.slice(0, 3).map(r => r.title.toLowerCase());
    if (top3Titles.some(t => t.includes(expectedTitle) || expectedTitle.includes(t))) {
      precisionAt3Hits++;
    }

    // MRR: find rank of first relevant result
    for (let i = 0; i < results.length; i++) {
      const title = results[i].title.toLowerCase();
      if (title.includes(expectedTitle) || expectedTitle.includes(title)) {
        reciprocalRankSum += 1 / (i + 1);
        break;
      }
    }
  }

  const precisionAt1 = queriesTested > 0 ? precisionAt1Hits / queriesTested : 0;
  const precisionAt3 = queriesTested > 0 ? precisionAt3Hits / queriesTested : 0;
  const mrr = queriesTested > 0 ? reciprocalRankSum / queriesTested : 0;

  // Overview metrics
  const overview = parser.getOverview();
  const fileList = parser.getFileList();
  let tocFilesWithEntries = 0;
  let tocTotalEntries = 0;

  for (const file of fileList) {
    const toc = parser.getFileToc(file);
    if (toc && toc.trim().length > 0) {
      tocFilesWithEntries++;
      tocTotalEntries += toc.split('\n').filter(l => l.trim().startsWith('-')).length;
    }
  }

  // Output results
  const result = {
    index: {
      totalSections: index.allSections.length,
      totalFiles: index.files.size,
      buildTimeMs: Math.round(buildTimeMs),
      sectionsWithCode,
      sectionsWithSourceUrl,
      avgContentLength: Math.round(avgContentLength),
    },
    search: {
      queriesTested,
      precisionAt1: Math.round(precisionAt1 * 1000) / 1000,
      precisionAt3: Math.round(precisionAt3 * 1000) / 1000,
      mrr: Math.round(mrr * 1000) / 1000,
      zeroResultQueries,
    },
    overview: {
      overviewLength: overview.length,
      tocFilesWithEntries,
      tocTotalEntries,
    },
  };

  console.log(JSON.stringify(result));
}

main().catch(err => {
  console.log(JSON.stringify({ error: String(err) }));
  process.exit(0);
});
