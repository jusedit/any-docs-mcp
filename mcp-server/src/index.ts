#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { MarkdownParser, Section } from './markdown-parser.js';
import { loadConfig, getDocsPath } from './config.js';

const config = loadConfig();
const docsPath = getDocsPath(config);
const serverName = config.serverName || `${config.activeDocs}-mcp`;

console.error(`[${serverName}] Loading documentation from: ${docsPath}`);
console.error(`[${serverName}] Active documentation: ${config.activeDocs}`);

const parser = new MarkdownParser(docsPath, config.activeDocs);

console.error(`[${serverName}] Building index...`);
parser.buildIndex();
console.error(`[${serverName}] Index ready.`);

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
  return {
    tools: [
      {
        name: 'search',
        description: `Search the ${config.activeDocs} documentation. Returns relevant sections with content and code examples. Use this for finding specific topics, APIs, or code patterns.`,
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search query (e.g., "getting started", "API reference", "configuration")'
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
          properties: {}
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
            }
          },
          required: ['title']
        }
      },
      {
        name: 'list_files',
        description: 'List all available documentation files.',
        inputSchema: {
          type: 'object',
          properties: {}
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
            }
          },
          required: ['query']
        }
      },
      {
        name: 'scrape_documentation',
        description: 'Scrape a new documentation site and add it to the available documentation sets. This uses LLM-powered analysis to automatically extract content. Returns a job ID to track progress.',
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
        name: 'list_documentation_sets',
        description: 'List all available documentation sets that have been scraped and are available for querying.',
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
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'search': {
        const query = args?.query as string;
        const maxResults = (args?.maxResults as number) || 10;
        const fileFilter = args?.fileFilter as string | undefined;
        const titlesOnly = args?.titlesOnly as boolean || false;

        const results = parser.search(query, { maxResults, fileFilter });
        
        if (results.length === 0) {
          return {
            content: [{ type: 'text', text: `No results found for "${query}".` }]
          };
        }

        const formatted = results.map(s => formatSection(s, !titlesOnly)).join('\n\n---\n\n');
        return {
          content: [{ 
            type: 'text', 
            text: `Found ${results.length} results for "${query}":\n\n${formatted}` 
          }]
        };
      }

      case 'get_overview': {
        const overview = parser.getOverview();
        return {
          content: [{ type: 'text', text: overview }]
        };
      }

      case 'get_file_toc': {
        const fileName = args?.fileName as string;
        const toc = parser.getFileToc(fileName);
        if (!toc) {
          return {
            content: [{ type: 'text', text: `File "${fileName}" not found. Use list_files to see available files.` }]
          };
        }
        return {
          content: [{ type: 'text', text: `# Table of Contents: ${fileName}\n\n${toc}` }]
        };
      }

      case 'get_section': {
        const title = args?.title as string;
        const fileName = args?.fileName as string | undefined;
        const sections = parser.getSectionByTitle(title, fileName);
        
        if (sections.length === 0) {
          return {
            content: [{ type: 'text', text: `No section found with title "${title}".` }]
          };
        }

        const formatted = sections.map(s => formatSection(s, true)).join('\n\n---\n\n');
        return {
          content: [{ type: 'text', text: formatted }]
        };
      }

      case 'list_files': {
        const files = parser.getFileList();
        const grouped: Record<string, string[]> = {};
        
        for (const file of files) {
          const prefix = file.split('-')[0];
          if (!grouped[prefix]) grouped[prefix] = [];
          grouped[prefix].push(file);
        }
        
        let output = '# Available Documentation Files\n\n';
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

        const index = parser.getIndex();
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
            content: [{ type: 'text', text: `No code examples found for "${query}".` }]
          };
        }

        let output = `Found ${topMatches.length} code examples for "${query}":\n\n`;
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
        const name = args?.name as string;
        const displayName = (args?.displayName as string) || name;

        const { spawn } = await import('child_process');
        const path = await import('path');
        const { fileURLToPath } = await import('url');
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const scraperPath = path.join(__dirname, '..', '..', 'scraper');

        return new Promise((resolve) => {
          const pythonProcess = spawn('python', [
            'cli.py',
            'add',
            '--url', url,
            '--name', name,
            '--display-name', displayName
          ], {
            cwd: scraperPath,
            env: {
              ...process.env,
              OPENROUTER_API_KEY: process.env.OPENROUTER_API_KEY || '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'
            }
          });

          let output = '';
          let errorOutput = '';

          pythonProcess.stdout.on('data', (data: Buffer) => {
            output += data.toString();
            console.error('[scraper]', data.toString());
          });

          pythonProcess.stderr.on('data', (data: Buffer) => {
            errorOutput += data.toString();
            console.error('[scraper-error]', data.toString());
          });

          pythonProcess.on('close', (code: number) => {
            if (code === 0) {
              resolve({
                content: [{
                  type: 'text',
                  text: `✅ Successfully scraped documentation!\n\n**Name:** ${name}\n**Display Name:** ${displayName}\n**URL:** ${url}\n\nThe documentation is now available. Use \`switch_documentation\` to switch to it, or restart the server with this documentation set active.\n\n**Output:**\n${output.substring(0, 1000)}${output.length > 1000 ? '...\n\n(truncated)' : ''}`
                }]
              });
            } else {
              resolve({
                content: [{
                  type: 'text',
                  text: `❌ Failed to scrape documentation.\n\n**Error Code:** ${code}\n**Error Output:**\n${errorOutput}\n\n**Output:**\n${output}`
                }],
                isError: true
              });
            }
          });
        });
      }

      case 'list_documentation_sets': {
        const { spawn } = await import('child_process');
        const path = await import('path');
        const { fileURLToPath } = await import('url');
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const scraperPath = path.join(__dirname, '..', '..', 'scraper');

        return new Promise((resolve) => {
          const pythonProcess = spawn('python', ['cli.py', 'list'], {
            cwd: scraperPath
          });

          let output = '';

          pythonProcess.stdout.on('data', (data: Buffer) => {
            output += data.toString();
          });

          pythonProcess.on('close', (code: number) => {
            if (code === 0) {
              resolve({
                content: [{
                  type: 'text',
                  text: `# Available Documentation Sets\n\n${output}\n\n**Currently Active:** ${config.activeDocs}`
                }]
              });
            } else {
              resolve({
                content: [{
                  type: 'text',
                  text: `Error listing documentation sets.`
                }],
                isError: true
              });
            }
          });
        });
      }

      case 'switch_documentation': {
        const newDocName = args?.name as string;
        
        try {
          const { getStorageRoot } = await import('./config.js');
          const path = await import('path');
          const { existsSync, readdirSync } = await import('fs');
          
          const storageRoot = getStorageRoot(config);
          const docDir = path.join(storageRoot, newDocName);
          
          if (!existsSync(docDir)) {
            return {
              content: [{
                type: 'text',
                text: `❌ Documentation set "${newDocName}" not found. Use \`list_documentation_sets\` to see available sets.`
              }],
              isError: true
            };
          }

          const versions = readdirSync(docDir).filter((d: string) => 
            d.startsWith('v') && existsSync(path.join(docDir, d))
          );

          if (versions.length === 0) {
            return {
              content: [{
                type: 'text',
                text: `❌ No versions found for "${newDocName}". The documentation may be incomplete.`
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

          // Replace global parser
          Object.assign(parser, newParser);

          return {
            content: [{
              type: 'text',
              text: `✅ Successfully switched to documentation set: **${newDocName}**\n\nVersion: ${latestVersion}\nPath: ${newDocsPath}\n\nYou can now search this documentation using the search tools.`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: `❌ Error switching documentation: ${error instanceof Error ? error.message : String(error)}`
            }],
            isError: true
          };
        }
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
  const files = parser.getFileList();
  return {
    resources: files.map(f => ({
      uri: `${config.activeDocs}://${f}`,
      name: f,
      mimeType: 'text/markdown',
      description: `${config.activeDocs} documentation: ${f}`
    }))
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const fileName = uri.replace(`${config.activeDocs}://`, '');
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
