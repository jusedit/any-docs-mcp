#!/usr/bin/env node

/**
 * AnyDocs MCP Server v2
 *
 * A lightweight MCP server that:
 *   1. Returns CLI commands to scrape documentation via scraper
 *   2. Manages scraped docs in a global AppData directory
 *   3. Copies docs + injects compact index into IDE-specific rules
 *
 * Tools:
 *   - scrape_docs:            Returns CLI command to scrape a documentation site
 *   - list_docs:              Lists all available doc sets in AppData
 *   - remove_docs:            Deletes a doc set from AppData
 *   - add_docs_to_project:    Copies docs into project + injects index into IDE rules
 *   - remove_docs_from_project: Removes docs + index from project
 *   - list_project_docs:      Lists docs currently added to this project
 *
 * ENV:
 *   ANYDOCS_IDE            - Target IDE: "windsurf" (default), "cursor", "claude", "antigravity"
 *   ANYDOCS_STORAGE_ROOT   - Override AppData storage path (optional)
 *   ANYDOCS_SCRAPER_PATH   - Override scraper path (optional, auto-detected from repo)
 *   OPENROUTER_API_KEY     - API key for LLM-powered scraping
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { fileURLToPath } from 'url';
import path from 'path';

import { listDocSets, getDocSetInfo, getDocRawDir, deleteDocSet, ensureStorageRoot, getStorageRoot } from './storage.js';
import { createAdapter, getIdeType } from './ide-adapter.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ideType = getIdeType();
const adapter = createAdapter(ideType);

function getScraperPath(): string {
  if (process.env.ANYDOCS_SCRAPER_PATH) {
    return process.env.ANYDOCS_SCRAPER_PATH;
  }
  // Default: relative to this repo (mcp-server is sibling of scraper)
  return path.resolve(__dirname, '..', '..', 'scraper');
}

console.error(`[anydocs-v2] IDE: ${ideType}`);
console.error(`[anydocs-v2] Storage: ${getStorageRoot()}`);
console.error(`[anydocs-v2] Scraper: ${getScraperPath()}`);

const server = new Server(
  { name: 'anydocs-v2', version: '2.0.0' },
  { capabilities: { tools: {} } }
);

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'scrape_docs',
      description: 'Get the CLI command to scrape a documentation site. The command uses the scraper and stores results in the global AnyDocs storage. After scraping completes, use `add_docs_to_project` to inject the docs into your project.',
      inputSchema: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'Start URL of the documentation site (e.g., "https://docs.example.com")' },
          name: { type: 'string', description: 'Unique identifier for this doc set (e.g., "react-docs"). Use lowercase with hyphens.' },
          max_pages: { type: 'number', description: 'Maximum pages to scrape (default: 500)', default: 500 },
        },
        required: ['url', 'name'],
      },
    },
    {
      name: 'list_docs',
      description: 'List all documentation sets available in the global AnyDocs storage. Shows name, source URL, page count, and size.',
      inputSchema: { type: 'object', properties: {} },
    },
    {
      name: 'remove_docs',
      description: 'Permanently delete a documentation set from the global AnyDocs storage. This does NOT remove it from projects — use `remove_docs_from_project` for that.',
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Name of the doc set to delete' },
        },
        required: ['name'],
      },
    },
    {
      name: 'add_docs_to_project',
      description: `Add documentation to the current project. Copies the doc files into the project and creates an always-on ${ideType} rule with the documentation index. The AI agent will then have persistent access to these docs.`,
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Name of the doc set to add (from list_docs)' },
          project_root: { type: 'string', description: 'Absolute path to the project root directory' },
        },
        required: ['name', 'project_root'],
      },
    },
    {
      name: 'remove_docs_from_project',
      description: `Remove documentation from the current project. Deletes the copied doc files and the ${ideType} rule.`,
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Name of the doc set to remove' },
          project_root: { type: 'string', description: 'Absolute path to the project root directory' },
        },
        required: ['name', 'project_root'],
      },
    },
    {
      name: 'list_project_docs',
      description: 'List documentation sets currently added to this project.',
      inputSchema: {
        type: 'object',
        properties: {
          project_root: { type: 'string', description: 'Absolute path to the project root directory' },
        },
        required: ['project_root'],
      },
    },
  ],
}));

// ---------------------------------------------------------------------------
// Tool handlers
// ---------------------------------------------------------------------------

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {

      // ---------------------------------------------------------------
      // scrape_docs — returns CLI command
      // ---------------------------------------------------------------
      case 'scrape_docs': {
        const url = args?.url as string;
        const docName = args?.name as string;
        const maxPages = (args?.max_pages as number) || 500;

        if (!url || !docName) {
          return { content: [{ type: 'text', text: '[ERROR] Both `url` and `name` are required.' }], isError: true };
        }

        // Validate URL
        try { new URL(url); } catch {
          return { content: [{ type: 'text', text: `[ERROR] Invalid URL: ${url}` }], isError: true };
        }

        // Sanitize name
        const sanitized = docName.replace(/[^a-zA-Z0-9_-]/g, '');
        if (sanitized !== docName) {
          return { content: [{ type: 'text', text: `[ERROR] Invalid name. Only alphanumeric, hyphens, underscores allowed. Got: "${docName}"` }], isError: true };
        }

        const scraperPath = getScraperPath();
        const storageRoot = ensureStorageRoot();
        const outputDir = path.join(storageRoot, sanitized);

        const cliCommand = `cd "${scraperPath}" && python cli.py scrape --url "${url}" --name "${sanitized}" --output "${outputDir}" --max-pages ${maxPages}`;

        return {
          content: [{
            type: 'text',
            text: [
              `[SCRAPE] Run this command to scrape the documentation:`,
              '',
              '```bash',
              cliCommand,
              '```',
              '',
              `**Name:** ${sanitized}`,
              `**URL:** ${url}`,
              `**Max pages:** ${maxPages}`,
              `**Output:** ${outputDir}`,
              '',
              `Once complete, use \`add_docs_to_project\` with name "${sanitized}" to inject the docs into your project.`,
            ].join('\n'),
          }],
        };
      }

      // ---------------------------------------------------------------
      // list_docs
      // ---------------------------------------------------------------
      case 'list_docs': {
        const docs = listDocSets();

        if (docs.length === 0) {
          return {
            content: [{
              type: 'text',
              text: '# Available Documentation Sets\n\nNo documentation sets found.\n\nUse `scrape_docs` to scrape a new documentation site.',
            }],
          };
        }

        let output = `# Available Documentation Sets (${docs.length})\n\n`;
        for (const doc of docs) {
          const sizeMB = (doc.sizeBytes / 1024 / 1024).toFixed(1);
          output += `- **${doc.name}**\n`;
          if (doc.sourceUrl) output += `  - Source: ${doc.sourceUrl}\n`;
          output += `  - Pages: ${doc.totalPages}, Size: ${sizeMB} MB\n`;
          if (doc.scrapedAt) output += `  - Scraped: ${doc.scrapedAt}\n`;
          output += '\n';
        }

        return { content: [{ type: 'text', text: output }] };
      }

      // ---------------------------------------------------------------
      // remove_docs
      // ---------------------------------------------------------------
      case 'remove_docs': {
        const docName = args?.name as string;
        if (!docName) {
          return { content: [{ type: 'text', text: '[ERROR] `name` is required.' }], isError: true };
        }

        const deleted = deleteDocSet(docName);
        if (!deleted) {
          return { content: [{ type: 'text', text: `[ERROR] Documentation "${docName}" not found in storage.` }], isError: true };
        }

        return {
          content: [{ type: 'text', text: `[SUCCESS] Deleted documentation "${docName}" from storage.\n\n⚠️ Note: If this doc set was added to any projects, use \`remove_docs_from_project\` to clean those up too.` }],
        };
      }

      // ---------------------------------------------------------------
      // add_docs_to_project
      // ---------------------------------------------------------------
      case 'add_docs_to_project': {
        const docName = args?.name as string;
        const projectRoot = args?.project_root as string;

        if (!docName || !projectRoot) {
          return { content: [{ type: 'text', text: '[ERROR] Both `name` and `project_root` are required.' }], isError: true };
        }

        const info = getDocSetInfo(docName);
        if (!info) {
          return { content: [{ type: 'text', text: `[ERROR] Documentation "${docName}" not found. Use \`list_docs\` to see available sets.` }], isError: true };
        }

        const rawDir = getDocRawDir(docName);
        if (!rawDir) {
          return { content: [{ type: 'text', text: `[ERROR] No raw docs found for "${docName}". The scrape may be incomplete.` }], isError: true };
        }

        const result = adapter.addDocsToProject(projectRoot, docName, rawDir, info.agentsIndex);

        if (!result.success) {
          return { content: [{ type: 'text', text: `[ERROR] ${result.message}` }], isError: true };
        }

        return {
          content: [{
            type: 'text',
            text: [
              `[SUCCESS] ${result.message}`,
              '',
              `The documentation is now persistently available to the AI agent.`,
              `The agent can read individual doc files from \`${result.docsDir}\`.`,
              '',
              `To remove: use \`remove_docs_from_project\` with name "${docName}".`,
            ].join('\n'),
          }],
        };
      }

      // ---------------------------------------------------------------
      // remove_docs_from_project
      // ---------------------------------------------------------------
      case 'remove_docs_from_project': {
        const docName = args?.name as string;
        const projectRoot = args?.project_root as string;

        if (!docName || !projectRoot) {
          return { content: [{ type: 'text', text: '[ERROR] Both `name` and `project_root` are required.' }], isError: true };
        }

        const result = adapter.removeDocsFromProject(projectRoot, docName);

        return {
          content: [{
            type: 'text',
            text: result.success ? `[SUCCESS] ${result.message}` : `[ERROR] ${result.message}`,
          }],
          ...(result.success ? {} : { isError: true }),
        };
      }

      // ---------------------------------------------------------------
      // list_project_docs
      // ---------------------------------------------------------------
      case 'list_project_docs': {
        const projectRoot = args?.project_root as string;

        if (!projectRoot) {
          return { content: [{ type: 'text', text: '[ERROR] `project_root` is required.' }], isError: true };
        }

        const docs = adapter.listProjectDocs(projectRoot);

        if (docs.length === 0) {
          return {
            content: [{
              type: 'text',
              text: `No documentation sets added to this project.\n\nUse \`add_docs_to_project\` to add docs from the global storage.`,
            }],
          };
        }

        let output = `# Project Documentation (${ideType})\n\n`;
        for (const doc of docs) {
          output += `- **${doc}**\n`;
        }
        output += `\nTo remove: use \`remove_docs_from_project\` with the doc name.`;

        return { content: [{ type: 'text', text: output }] };
      }

      default:
        return { content: [{ type: 'text', text: `Unknown tool: ${name}` }], isError: true };
    }
  } catch (error) {
    return {
      content: [{ type: 'text', text: `[ERROR] ${error instanceof Error ? error.message : String(error)}` }],
      isError: true,
    };
  }
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`[anydocs-v2] Server running on stdio (IDE: ${ideType})`);
}

main().catch((error) => {
  console.error('[anydocs-v2] Fatal error:', error);
  process.exit(1);
});
