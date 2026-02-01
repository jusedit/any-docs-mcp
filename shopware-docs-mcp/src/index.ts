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

const DOCS_PATH = process.env.SHOPWARE_DOCS_PATH || 'C:\\Users\\jonas\\Documents\\Python\\Karl & Engel\\Shopware';

const parser = new MarkdownParser(DOCS_PATH);

// Pre-build index on startup
console.error('[shopware-docs-mcp] Building index...');
parser.buildIndex();
console.error('[shopware-docs-mcp] Index ready.');

const server = new Server(
  {
    name: 'shopware-docs-mcp',
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

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'search',
        description: 'Search the Shopware documentation. Returns relevant sections with content and code examples. Use this for finding specific topics, APIs, or code patterns.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search query (e.g., "plugin erstellen", "DataAbstractionLayer", "event subscriber")'
            },
            maxResults: {
              type: 'number',
              description: 'Maximum number of results (default: 10)',
              default: 10
            },
            fileFilter: {
              type: 'string',
              description: 'Filter by filename (e.g., "plugins" to only search plugin docs)'
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
              description: 'Name of the file without .md extension (e.g., "guides-plugins-plugins")'
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
              description: 'Section title to find (e.g., "Plugin Base Guide", "Create your first plugin")'
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
              description: 'Search term to find in code examples (e.g., "EntityRepository", "subscriber", "composer")'
            },
            language: {
              type: 'string',
              description: 'Filter by programming language (e.g., "php", "bash", "javascript")'
            },
            maxResults: {
              type: 'number',
              description: 'Maximum number of results',
              default: 5
            }
          },
          required: ['query']
        }
      }
    ]
  };
});

// Handle tool calls
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

// List resources (documentation files)
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const files = parser.getFileList();
  return {
    resources: files.map(f => ({
      uri: `shopware-docs://${f}`,
      name: f,
      mimeType: 'text/markdown',
      description: `Shopware documentation: ${f}`
    }))
  };
});

// Read resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const fileName = uri.replace('shopware-docs://', '');
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

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('[shopware-docs-mcp] Server running on stdio');
}

main().catch((error) => {
  console.error('[shopware-docs-mcp] Fatal error:', error);
  process.exit(1);
});
