#!/usr/bin/env node

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { MarkdownParser, Section } from './markdown-parser.js';
import { loadConfig, getDocsPath, listAllDocs, getDocMetadata, getDocConfig, getStorageRoot } from './config.js';
import { jobManager, ScrapeJob } from './job-manager.js';

const config = loadConfig();
const docsPath = getDocsPath(config);
const serverName = config.serverName || (config.activeDocs ? `${config.activeDocs}-mcp` : 'anydocs-mcp');

console.error(`[${serverName}] Loading documentation from: ${docsPath || '(no active docs)'}`);
console.error(`[${serverName}] Active documentation: ${config.activeDocs || '(none - all docs available)'}`);

let parser: MarkdownParser | null = null;
let currentDocName = config.activeDocs || '';

if (docsPath) {
  parser = new MarkdownParser(docsPath, config.activeDocs);
  console.error(`[${serverName}] Building index...`);
  parser.buildIndex();
  console.error(`[${serverName}] Index ready.`);
} else {
  console.error(`[${serverName}] No active documentation set. Use list_documentation_sets and switch_documentation to select one.`);
}

const server = new Server(
  {
    name: serverName,
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

function formatSection(section: Section, includeContent: boolean = true): string {
  const lines: string[] = [];
  const pathStr = section.path.length > 0 ? `${section.path.join(' > ')} > ` : '';
  lines.push(`## ${pathStr}${section.title}`);
  lines.push(`**File:** ${section.file}.md`);
  if (section.sourceUrl) {
    lines.push(`**Source:** ${section.sourceUrl}`);
  }
  
  if (includeContent && section.content) {
    lines.push('');
    lines.push(section.content.replace(/\[CODE_BLOCK\]/g, '```...```'));
  }
  
  if (section.codeBlocks.length > 0) {
    lines.push('');
    lines.push(`**Code Examples (${section.codeBlocks.length}):**`);
    for (const block of section.codeBlocks) {
      lines.push('```' + block.language);
      lines.push(block.code);
      lines.push('```');
    }
  }
  
  return lines.join('\n');
}

server.setRequestHandler(ListToolsRequestSchema, async () => {
  const docDescription = currentDocName ? `the ${currentDocName} documentation` : 'the currently active documentation';
  return {
    tools: [
      {
        name: 'search',
        description: `Search ${docDescription}. Returns relevant sections with content and code examples. Use this for finding specific topics, APIs, or code patterns.`,
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search query (e.g., "getting started", "API reference", "configuration")'
            },
            docs: {
              type: 'string',
              description: 'Optional: Name of specific documentation set to search in. If not provided, searches the currently active documentation.'
            },
            maxResults: {
              type: 'number',
              description: 'Maximum number of results (default: 10)',
              default: 10
            },
            fileFilter: {
              type: 'string',
              description: 'Filter by filename (e.g., "api" to only search API docs)'
            },
            titlesOnly: {
              type: 'boolean',
              description: 'If true, only return section titles without content (faster overview)',
              default: false
            }
          },
          required: ['query']
        }
      },
      {
        name: 'get_overview',
        description: 'Get a high-level overview of all documentation files and their main sections. Use this to understand what documentation is available.',
        inputSchema: {
          type: 'object',
          properties: {
            docs: {
              type: 'string',
              description: 'Optional: Name of specific documentation set. If not provided, uses the currently active documentation.'
            }
          }
        }
      },
      {
        name: 'get_file_toc',
        description: 'Get the table of contents (all headings) for a specific documentation file. Use this to navigate within a file.',
        inputSchema: {
          type: 'object',
          properties: {
            fileName: {
              type: 'string',
              description: 'Name of the file without .md extension'
            },
            docs: {
              type: 'string',
              description: 'Optional: Name of specific documentation set.'
            }
          },
          required: ['fileName']
        }
      },
      {
        name: 'get_section',
        description: 'Get a specific section by its title. Returns full content including code blocks.',
        inputSchema: {
          type: 'object',
          properties: {
            title: {
              type: 'string',
              description: 'Section title to find'
            },
            fileName: {
              type: 'string',
              description: 'Optional: filter by filename'
            },
            docs: {
              type: 'string',
              description: 'Optional: Name of specific documentation set.'
            }
          },
          required: ['title']
        }
      },
      {
        name: 'list_files',
        description: 'List all available documentation files in the current or specified documentation set.',
        inputSchema: {
          type: 'object',
          properties: {
            docs: {
              type: 'string',
              description: 'Optional: Name of specific documentation set.'
            }
          }
        }
      },
      {
        name: 'find_code_examples',
        description: 'Search specifically for code examples in the documentation.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search term to find in code examples'
            },
            language: {
              type: 'string',
              description: 'Filter by programming language (e.g., "python", "javascript", "bash")'
            },
            maxResults: {
              type: 'number',
              description: 'Maximum number of results',
              default: 5
            },
            docs: {
              type: 'string',
              description: 'Optional: Name of specific documentation set.'
            }
          },
          required: ['query']
        }
      },
      {
        name: 'scrape_documentation',
        description: 'Start scraping a new documentation site asynchronously. Returns a job ID to track progress. The scraping runs in the background - use get_scrape_status to check progress.',
        inputSchema: {
          type: 'object',
          properties: {
            url: {
              type: 'string',
              description: 'Start URL of the documentation site (e.g., "https://docs.example.com")'
            },
            name: {
              type: 'string',
              description: 'Unique identifier for this documentation set (e.g., "example-docs")'
            },
            displayName: {
              type: 'string',
              description: 'Human-readable name (optional, defaults to name)'
            }
          },
          required: ['url', 'name']
        }
      },
      {
        name: 'get_scrape_status',
        description: 'Get the status of a scraping job by its job ID. Shows progress including current phase, pages scraped, and any errors.',
        inputSchema: {
          type: 'object',
          properties: {
            jobId: {
              type: 'string',
              description: 'The job ID returned by scrape_documentation'
            }
          },
          required: ['jobId']
        }
      },
      {
        name: 'update_documentation',
        description: 'Re-scrape an existing documentation set to get the latest content. Runs asynchronously and returns a job ID. The old version remains available until the new scrape completes.',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: 'Name of the documentation set to update'
            },
            force: {
              type: 'boolean',
              description: 'Force update even if the refresh timeout has not been reached',
              default: false
            }
          },
          required: ['name']
        }
      },
      {
        name: 'list_documentation_sets',
        description: 'List all available documentation sets with their status, including scrape progress for active jobs, content hash, last update time, and whether refresh is needed.',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'switch_documentation',
        description: 'Switch to a different documentation set. Rebuilds the index for the selected documentation.',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: 'Name of the documentation set to switch to'
            }
          },
          required: ['name']
        }
      },
      {
        name: 'get_scrape_logs',
        description: 'Read the log output from a scraping job. Useful for debugging failed scrapes or understanding what happened during the process.',
        inputSchema: {
          type: 'object',
          properties: {
            jobId: {
              type: 'string',
              description: 'The job ID to get logs for'
            },
            lines: {
              type: 'number',
              description: 'Number of lines to return (default: 100, max: 1000)',
              default: 100
            }
          },
          required: ['jobId']
        }
      }
    ]
  };
});

// Helper function to get parser for a specific docs set
async function getParserForDocs(docsName?: string): Promise<{ parser: MarkdownParser; docName: string } | null> {
  const targetDoc = docsName || currentDocName;
  
  if (!targetDoc) {
    return null;
  }
  
  // If requesting current doc and parser exists, return it
  if (targetDoc === currentDocName && parser) {
    return { parser, docName: currentDocName };
  }
  
  // Otherwise, create a temporary parser for the requested docs
  const path = await import('path');
  const { existsSync, readdirSync, statSync } = await import('fs');
  
  const storageRoot = getStorageRoot(config);
  const docDir = path.join(storageRoot, targetDoc);
  
  if (!existsSync(docDir)) {
    return null;
  }
  
  const versions = readdirSync(docDir).filter((d: string) => 
    d.startsWith('v') && statSync(path.join(docDir, d)).isDirectory()
  );
  
  if (versions.length === 0) {
    return null;
  }
  
  const latestVersion = versions
    .map((v: string) => ({ name: v, num: parseInt(v.substring(1)) }))
    .filter((v: { name: string; num: number }) => !isNaN(v.num))
    .sort((a: { num: number }, b: { num: number }) => b.num - a.num)[0].name;
  
  const docsPath = path.join(docDir, latestVersion);
  const tempParser = new MarkdownParser(docsPath, targetDoc);
  tempParser.buildIndex();
  
  return { parser: tempParser, docName: targetDoc };
}

// Helper to run async scraping
function startAsyncScrape(jobId: string, url: string, name: string, displayName: string, isUpdate: boolean = false): void {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const scraperPath = path.join(__dirname, '..', '..', 'scraper');
  
  const command = isUpdate ? 'update' : 'add';
  const args = isUpdate 
    ? ['cli.py', command, '--name', name, '--json-progress']
    : ['cli.py', command, '--url', url, '--name', name, '--display-name', displayName, '--json-progress'];
  
  jobManager.updateJob(jobId, { status: 'analyzing' });
  
  const pythonProcess = spawn('python', args, {
    cwd: scraperPath,
    env: {
      ...process.env,
      OPENROUTER_API_KEY: process.env.OPENROUTER_API_KEY,
      ANYDOCS_REFRESH_DAYS: String(config.refreshDays || 30)
    },
    stdio: ['ignore', 'pipe', 'pipe']
  });
  
  pythonProcess.stdout.on('data', (data: Buffer) => {
    const lines = data.toString().split('\n');
    for (const line of lines) {
      if (line.trim()) {
        jobManager.addLog(jobId, `[stdout] ${line}`);
      }
      if (line.startsWith('PROGRESS:')) {
        try {
          const progress = JSON.parse(line.substring(9));
          if (progress.phase === 'completed') {
            jobManager.completeJob(jobId, {
              totalPages: progress.result?.total_pages || 0,
              totalFiles: progress.result?.total_files || 0,
              version: progress.result?.version || 'v1'
            });
          } else if (progress.phase === 'failed') {
            jobManager.failJob(jobId, progress.message || 'Unknown error');
          } else {
            jobManager.updateJob(jobId, { 
              status: progress.phase === 'scraping' ? 'scraping' : 'analyzing' 
            });
            jobManager.updateProgress(
              jobId, 
              progress.phase, 
              progress.current || 0, 
              progress.total || 0, 
              progress.current_url
            );
          }
        } catch (e) {
          console.error('[scraper] Failed to parse progress:', line);
          jobManager.addLog(jobId, `[error] Failed to parse progress: ${line}`);
        }
      }
    }
  });
  
  pythonProcess.stderr.on('data', (data: Buffer) => {
    const msg = data.toString();
    console.error('[scraper]', msg);
    const lines = msg.split('\n');
    for (const line of lines) {
      if (line.trim()) {
        jobManager.addLog(jobId, `[stderr] ${line}`);
      }
    }
  });
  
  pythonProcess.on('close', (code: number) => {
    const job = jobManager.getJob(jobId);
    if (job && job.status !== 'completed' && job.status !== 'failed') {
      if (code === 0) {
        jobManager.completeJob(jobId, { totalPages: 0, totalFiles: 0, version: 'v1' });
      } else {
        jobManager.failJob(jobId, `Process exited with code ${code}`);
      }
    }
  });
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'search': {
        const query = args?.query as string;
        const docsName = args?.docs as string | undefined;
        const maxResults = (args?.maxResults as number) || 10;
        const fileFilter = args?.fileFilter as string | undefined;
        const titlesOnly = args?.titlesOnly as boolean || false;

        const parserInfo = await getParserForDocs(docsName);
        if (!parserInfo) {
          return {
            content: [{ type: 'text', text: `No documentation set active. Use \`list_documentation_sets\` to see available sets and \`switch_documentation\` to select one.` }]
          };
        }

        const results = parserInfo.parser.search(query, { maxResults, fileFilter });
        
        if (results.length === 0) {
          return {
            content: [{ type: 'text', text: `No results found for "${query}" in ${parserInfo.docName} documentation.` }]
          };
        }

        const formatted = results.map(s => formatSection(s, !titlesOnly)).join('\n\n---\n\n');
        return {
          content: [{ 
            type: 'text', 
            text: `Found ${results.length} results for "${query}" in **${parserInfo.docName}**:\n\n${formatted}` 
          }]
        };
      }

      case 'get_overview': {
        const docsName = args?.docs as string | undefined;
        const parserInfo = await getParserForDocs(docsName);
        if (!parserInfo) {
          return {
            content: [{ type: 'text', text: `No documentation set active. Use \`list_documentation_sets\` to see available sets.` }]
          };
        }
        const overview = parserInfo.parser.getOverview();
        return {
          content: [{ type: 'text', text: overview }]
        };
      }

      case 'get_file_toc': {
        const fileName = args?.fileName as string;
        const docsName = args?.docs as string | undefined;
        const parserInfo = await getParserForDocs(docsName);
        if (!parserInfo) {
          return {
            content: [{ type: 'text', text: `No documentation set active.` }]
          };
        }
        const toc = parserInfo.parser.getFileToc(fileName);
        if (!toc) {
          return {
            content: [{ type: 'text', text: `File "${fileName}" not found in ${parserInfo.docName}. Use list_files to see available files.` }]
          };
        }
        return {
          content: [{ type: 'text', text: `# Table of Contents: ${fileName} (${parserInfo.docName})\n\n${toc}` }]
        };
      }

      case 'get_section': {
        const title = args?.title as string;
        const fileName = args?.fileName as string | undefined;
        const docsName = args?.docs as string | undefined;
        const parserInfo = await getParserForDocs(docsName);
        if (!parserInfo) {
          return {
            content: [{ type: 'text', text: `No documentation set active.` }]
          };
        }
        const sections = parserInfo.parser.getSectionByTitle(title, fileName);
        
        if (sections.length === 0) {
          return {
            content: [{ type: 'text', text: `No section found with title "${title}" in ${parserInfo.docName}.` }]
          };
        }

        const formatted = sections.map(s => formatSection(s, true)).join('\n\n---\n\n');
        return {
          content: [{ type: 'text', text: formatted }]
        };
      }

      case 'list_files': {
        const docsName = args?.docs as string | undefined;
        const parserInfo = await getParserForDocs(docsName);
        if (!parserInfo) {
          return {
            content: [{ type: 'text', text: `No documentation set active.` }]
          };
        }
        const files = parserInfo.parser.getFileList();
        const grouped: Record<string, string[]> = {};
        
        for (const file of files) {
          const prefix = file.split('-')[0];
          if (!grouped[prefix]) grouped[prefix] = [];
          grouped[prefix].push(file);
        }
        
        let output = `# Available Documentation Files (${parserInfo.docName})\n\n`;
        for (const [category, fileList] of Object.entries(grouped)) {
          output += `## ${category}\n`;
          for (const f of fileList) {
            output += `- ${f}\n`;
          }
          output += '\n';
        }
        
        return {
          content: [{ type: 'text', text: output }]
        };
      }

      case 'find_code_examples': {
        const query = args?.query as string;
        const language = args?.language as string | undefined;
        const maxResults = (args?.maxResults as number) || 5;
        const docsName = args?.docs as string | undefined;

        const parserInfo = await getParserForDocs(docsName);
        if (!parserInfo) {
          return {
            content: [{ type: 'text', text: `No documentation set active.` }]
          };
        }

        const index = parserInfo.parser.getIndex();
        const queryLower = query.toLowerCase();
        
        const matches: { section: Section; block: { language: string; code: string }; score: number }[] = [];

        for (const section of index.allSections) {
          for (const block of section.codeBlocks) {
            if (language && block.language.toLowerCase() !== language.toLowerCase()) {
              continue;
            }
            
            const codeLower = block.code.toLowerCase();
            if (codeLower.includes(queryLower)) {
              const occurrences = (codeLower.match(new RegExp(queryLower, 'g')) || []).length;
              matches.push({ section, block, score: occurrences });
            }
          }
        }

        matches.sort((a, b) => b.score - a.score);
        const topMatches = matches.slice(0, maxResults);

        if (topMatches.length === 0) {
          return {
            content: [{ type: 'text', text: `No code examples found for "${query}" in ${parserInfo.docName}.` }]
          };
        }

        let output = `Found ${topMatches.length} code examples for "${query}" in **${parserInfo.docName}**:\n\n`;
        for (const { section, block } of topMatches) {
          output += `### ${section.title}\n`;
          output += `**File:** ${section.file}.md\n`;
          if (section.sourceUrl) {
            output += `**Source:** ${section.sourceUrl}\n`;
          }
          output += `\n\`\`\`${block.language}\n${block.code}\n\`\`\`\n\n---\n\n`;
        }

        return {
          content: [{ type: 'text', text: output }]
        };
      }

      case 'scrape_documentation': {
        const url = args?.url as string;
        const docName = args?.name as string;
        const displayName = (args?.displayName as string) || docName;

        // Generate CLI command for the user to execute
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const scraperPath = path.join(__dirname, '..', '..', 'scraper');
        
        const cliCommand = `cd "${scraperPath}"; python cli.py add --url "${url}" --name "${docName}" --display-name "${displayName}" --json-progress`;

        return {
          content: [{
            type: 'text',
            text: `[READY] To scrape documentation, please execute the following command in your terminal:\n\n\`\`\`bash\n${cliCommand}\n\`\`\`\n\n**Documentation:** ${displayName}\n**URL:** ${url}\n\nOnce the scraping completes successfully, use \`switch_documentation\` with name "${docName}" to use the scraped documentation.`
          }]
        };
      }

      case 'get_scrape_status': {
        const jobId = args?.jobId as string;
        const job = jobManager.getJob(jobId);

        if (!job) {
          return {
            content: [{
              type: 'text',
              text: `[ERROR] Job not found: ${jobId}\n\nThe job may have expired or the ID is incorrect.`
            }],
            isError: true
          };
        }

        let statusEmoji = '[PENDING]';
        if (job.status === 'completed') statusEmoji = '[DONE]';
        else if (job.status === 'failed') statusEmoji = '[FAILED]';
        else if (job.status === 'scraping') statusEmoji = '[SCRAPING]';
        else if (job.status === 'analyzing') statusEmoji = '[ANALYZING]';

        let output = `${statusEmoji} **Scrape Job Status**\n\n`;
        output += `**Job ID:** ${job.id}\n`;
        output += `**Documentation:** ${job.displayName} (${job.name})\n`;
        output += `**URL:** ${job.url}\n`;
        output += `**Status:** ${job.status}\n`;
        output += `**Started:** ${job.startedAt}\n`;
        
        if (job.completedAt) {
          output += `**Completed:** ${job.completedAt}\n`;
        }

        output += `\n**Progress:**\n`;
        output += `- Phase: ${job.progress.phase}\n`;
        if (job.progress.total > 0) {
          const percent = Math.round((job.progress.current / job.progress.total) * 100);
          output += `- Progress: ${job.progress.current}/${job.progress.total} (${percent}%)\n`;
        }
        if (job.progress.currentUrl) {
          output += `- Current URL: ${job.progress.currentUrl}\n`;
        }

        if (job.error) {
          output += `\n**Error:** ${job.error}\n`;
        }

        if (job.result) {
          output += `\n**Result:**\n`;
          output += `- Total Pages: ${job.result.totalPages}\n`;
          output += `- Total Files: ${job.result.totalFiles}\n`;
          output += `- Version: ${job.result.version}\n`;
          output += `\nThe documentation is ready! Use \`switch_documentation\` to switch to "${job.name}".`;
        }

        return {
          content: [{ type: 'text', text: output }]
        };
      }

      case 'update_documentation': {
        const docName = args?.name as string;
        const force = args?.force as boolean || false;

        // Check if doc exists
        const docConfig = getDocConfig(config, docName);
        if (!docConfig) {
          return {
            content: [{
              type: 'text',
              text: `[ERROR] Documentation "${docName}" not found. Use \`list_documentation_sets\` to see available sets.`
            }],
            isError: true
          };
        }

        // Check if refresh is needed
        const metadata = getDocMetadata(config, docName);
        if (!force && metadata?.refresh_after) {
          const refreshDate = new Date(metadata.refresh_after);
          if (refreshDate > new Date()) {
            return {
              content: [{
                type: 'text',
                text: `[INFO] Documentation "${docName}" does not need refresh yet.\n\n**Last scraped:** ${metadata.last_scraped}\n**Refresh after:** ${metadata.refresh_after}\n**Content hash:** ${metadata.content_hash?.substring(0, 12)}...\n\nUse \`force: true\` to update anyway.`
              }]
            };
          }
        }

        // Generate CLI command for the user to execute
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const scraperPath = path.join(__dirname, '..', '..', 'scraper');
        
        const cliCommand = `cd "${scraperPath}"; python cli.py update --name "${docName}" --json-progress${force ? ' --force' : ''}`;

        return {
          content: [{
            type: 'text',
            text: `[READY] To update documentation, please execute the following command in your terminal:\n\n\`\`\`bash\n${cliCommand}\n\`\`\`\n\n**Documentation:** ${docConfig.display_name || docName}\n**Previous hash:** ${metadata?.content_hash?.substring(0, 12) || 'N/A'}...\n\nOnce the update completes, use \`switch_documentation\` with name "${docName}" to refresh the index.`
          }]
        };
      }

      case 'list_documentation_sets': {
        const allDocs = listAllDocs(config);
        const activeJobs = jobManager.getActiveJobs();
        
        if (allDocs.length === 0 && activeJobs.length === 0) {
          return {
            content: [{
              type: 'text',
              text: `# Available Documentation Sets\n\nNo documentation sets found.\n\nUse \`scrape_documentation\` to add a new documentation site.`
            }]
          };
        }

        let output = `# Available Documentation Sets\n\n`;
        output += `**Currently Active:** ${currentDocName || '(none)'}\n\n`;

        // Show active jobs first
        if (activeJobs.length > 0) {
          output += `## [IN PROGRESS]\n\n`;
          for (const job of activeJobs) {
            const percent = job.progress.total > 0 
              ? Math.round((job.progress.current / job.progress.total) * 100) 
              : 0;
            output += `- **${job.displayName}** (${job.name})\n`;
            output += `  - Status: ${job.status}\n`;
            output += `  - Progress: ${percent}% (${job.progress.current}/${job.progress.total})\n`;
            output += `  - Job ID: ${job.id}\n\n`;
          }
        }

        // Show existing docs
        if (allDocs.length > 0) {
          output += `## Available\n\n`;
          for (const docName of allDocs) {
            const docConfig = getDocConfig(config, docName);
            const metadata = getDocMetadata(config, docName);
            const isActive = docName === currentDocName;
            
            output += `- **${docConfig?.display_name || docName}** (${docName})${isActive ? ' [ACTIVE]' : ''}\n`;
            if (docConfig?.start_url) {
              output += `  - URL: ${docConfig.start_url}\n`;
            }
            if (metadata) {
              output += `  - Pages: ${metadata.total_pages || 'N/A'}, Files: ${metadata.total_files || 'N/A'}\n`;
              output += `  - Last scraped: ${metadata.last_scraped || 'N/A'}\n`;
              if (metadata.content_hash) {
                output += `  - Content hash: ${metadata.content_hash.substring(0, 12)}...\n`;
              }
              if (metadata.refresh_after) {
                const needsRefresh = new Date(metadata.refresh_after) < new Date();
                output += `  - Refresh: ${needsRefresh ? '[NEEDS REFRESH]' : 'OK'} (after ${metadata.refresh_after.substring(0, 10)})\n`;
              }
            }
            output += '\n';
          }
        }

        return {
          content: [{ type: 'text', text: output }]
        };
      }

      case 'switch_documentation': {
        const newDocName = args?.name as string;
        
        try {
          const path = await import('path');
          const { existsSync, readdirSync, statSync } = await import('fs');
          
          const storageRoot = getStorageRoot(config);
          const docDir = path.join(storageRoot, newDocName);
          
          if (!existsSync(docDir)) {
            return {
              content: [{
                type: 'text',
                text: `[ERROR] Documentation set "${newDocName}" not found. Use \`list_documentation_sets\` to see available sets.`
              }],
              isError: true
            };
          }

          const versions = readdirSync(docDir).filter((d: string) => 
            d.startsWith('v') && statSync(path.join(docDir, d)).isDirectory()
          );

          if (versions.length === 0) {
            return {
              content: [{
                type: 'text',
                text: `[ERROR] No versions found for "${newDocName}". The documentation may be incomplete.`
              }],
              isError: true
            };
          }

          const latestVersion = versions
            .map((v: string) => ({ name: v, num: parseInt(v.substring(1)) }))
            .filter((v: any) => !isNaN(v.num))
            .sort((a: any, b: any) => b.num - a.num)[0].name;

          const newDocsPath = path.join(docDir, latestVersion);

          console.error(`[switch] Switching to ${newDocName} (${latestVersion})...`);
          const newParser = new MarkdownParser(newDocsPath, newDocName);
          console.error(`[switch] Building index...`);
          newParser.buildIndex();
          console.error(`[switch] Index ready.`);

          // Update global state
          parser = newParser;
          currentDocName = newDocName;

          return {
            content: [{
              type: 'text',
              text: `[SUCCESS] Successfully switched to documentation set: **${newDocName}**\n\nVersion: ${latestVersion}\nPath: ${newDocsPath}\n\nYou can now search this documentation using the search tools.`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: `[ERROR] Error switching documentation: ${error instanceof Error ? error.message : String(error)}`
            }],
            isError: true
          };
        }
      }

      case 'get_scrape_logs': {
        const jobId = args?.jobId as string;
        const lines = (args?.lines as number) || 100;

        const logs = jobManager.getLogs(jobId, lines);

        if (logs.length === 0) {
          return {
            content: [{
              type: 'text',
              text: `[ERROR] No logs found for job ID: ${jobId}\n\nThe job may not exist or may have expired.`
            }],
            isError: true
          };
        }

        const job = jobManager.getJob(jobId);
        let output = `# Scrape Logs\n\n`;
        if (job) {
          output += `**Job ID:** ${job.id}\n`;
          output += `**Documentation:** ${job.displayName} (${job.name})\n`;
          output += `**Status:** ${job.status}\n`;
          output += `**Started:** ${job.startedAt}\n`;
          if (job.completedAt) {
            output += `**Completed:** ${job.completedAt}\n`;
          }
          output += `\n`;
        }

        output += `## Log Output (last ${logs.length} lines)\n\n`;
        output += '```\n';
        output += logs.join('\n');
        output += '\n```';

        return {
          content: [{ type: 'text', text: output }]
        };
      }

      default:
        return {
          content: [{ type: 'text', text: `Unknown tool: ${name}` }],
          isError: true
        };
    }
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error: ${error instanceof Error ? error.message : String(error)}` }],
      isError: true
    };
  }
});

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  if (!parser) {
    return { resources: [] };
  }
  const files = parser.getFileList();
  return {
    resources: files.map(f => ({
      uri: `${currentDocName}://${f}`,
      name: f,
      mimeType: 'text/markdown',
      description: `${currentDocName} documentation: ${f}`
    }))
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  if (!parser) {
    throw new Error('No documentation set active');
  }
  const uri = request.params.uri;
  const fileName = uri.replace(`${currentDocName}://`, '');
  const toc = parser.getFileToc(fileName);
  
  if (!toc) {
    throw new Error(`File not found: ${fileName}`);
  }

  return {
    contents: [{
      uri,
      mimeType: 'text/markdown',
      text: `# ${fileName}\n\n${toc}`
    }]
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`[${serverName}] Server running on stdio`);
}

main().catch((error) => {
  console.error(`[${serverName}] Fatal error:`, error);
  process.exit(1);
});
