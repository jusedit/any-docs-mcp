import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { spawn, ChildProcess } from 'child_process';
import { join } from 'path';
import { mkdirSync, writeFileSync, rmSync, existsSync } from 'fs';

interface MCPRequest {
  jsonrpc: '2.0';
  id: number;
  method: string;
  params?: any;
}

interface MCPResponse {
  jsonrpc: '2.0';
  id: number;
  result?: any;
  error?: { code: number; message: string };
}

function createFixtureDocSet(basePath: string, name: string) {
  const docPath = join(basePath, name, 'v1');
  mkdirSync(docPath, { recursive: true });
  
  // Create config.json
  writeFileSync(
    join(basePath, name, 'config.json'),
    JSON.stringify({
      name,
      display_name: `${name} Docs`,
      description: `Test documentation for ${name}`,
      start_url: 'https://example.com/docs',
      status: 'active'
    }, null, 2)
  );
  
  // Create metadata.json
  writeFileSync(
    join(basePath, name, 'metadata.json'),
    JSON.stringify({
      name,
      display_name: `${name} Docs`,
      version: 'v1',
      last_scraped: new Date().toISOString(),
      file_count: 2
    }, null, 2)
  );
  
  // Create markdown files
  writeFileSync(
    join(docPath, 'getting-started.md'),
    `# Getting Started with ${name}

## Installation

\`\`\`bash
npm install ${name.toLowerCase()}
\`\`\`

## Basic Usage

\`\`\`javascript
import { init } from '${name.toLowerCase()}';
const app = init();
\`\`\`
`
  );
  
  writeFileSync(
    join(docPath, 'api-reference.md'),
    `# API Reference for ${name}

## Core Functions

### init()

Initializes the application.

\`\`\`javascript
const app = init(options);
\`\`\`

## Types

\`\`\`typescript
interface Options {
  debug?: boolean;
}
\`\`\`
`
  );
}

describe('MCP Server E2E', () => {
  let serverProcess: ChildProcess;
  let requestId = 0;
  const responses: Map<number, MCPResponse> = new Map();
  const fixturesPath = join(__dirname, '../../test-e2e-fixtures');
  
  beforeAll(async () => {
    // Create fixture doc sets
    createFixtureDocSet(fixturesPath, 'test-docs-a');
    createFixtureDocSet(fixturesPath, 'test-docs-b');
    
    // Spawn MCP server
    const serverPath = join(__dirname, '../../dist/index.js');
    serverProcess = spawn('node', [serverPath], {
      env: {
        ...process.env,
        ANYDOCS_STORAGE_ROOT: fixturesPath
      },
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    // Wait for server to be ready
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Handle responses
    let buffer = '';
    serverProcess.stdout?.on('data', (data) => {
      buffer += data.toString();
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      
      for (const line of lines) {
        if (line.trim()) {
          try {
            // Skip PROGRESS: prefix lines
            const jsonLine = line.replace(/^PROGRESS:/, '');
            const msg = JSON.parse(jsonLine);
            if (msg.id !== undefined) {
              responses.set(msg.id, msg);
            }
          } catch {
            // Not JSON, ignore
          }
        }
      }
    });
  }, 15000);
  
  afterAll(() => {
    if (serverProcess) {
      serverProcess.kill();
    }
    // Cleanup fixtures
    if (existsSync(fixturesPath)) {
      rmSync(fixturesPath, { recursive: true });
    }
  });
  
  function sendRequest(method: string, params?: any): Promise<MCPResponse> {
    return new Promise((resolve, reject) => {
      const id = ++requestId;
      const req: MCPRequest = {
        jsonrpc: '2.0',
        id,
        method,
        params
      };
      
      const timeout = setTimeout(() => {
        reject(new Error(`Timeout waiting for response to ${method}`));
      }, 5000);
      
      const checkResponse = () => {
        const response = responses.get(id);
        if (response) {
          clearTimeout(timeout);
          responses.delete(id);
          resolve(response);
        } else {
          setTimeout(checkResponse, 100);
        }
      };
      
      serverProcess.stdin?.write(JSON.stringify(req) + '\n');
      checkResponse();
    });
  }
  
  it('responds to initialize handshake', async () => {
    const response = await sendRequest('initialize', {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'test-client', version: '1.0.0' }
    });
    
    expect(response.error).toBeUndefined();
    expect(response.result).toBeDefined();
    expect(response.result.protocolVersion).toBeDefined();
  });
  
  it('lists all available tools', async () => {
    const response = await sendRequest('tools/list');
    
    expect(response.error).toBeUndefined();
    expect(response.result).toBeDefined();
    expect(response.result.tools).toBeDefined();
    expect(response.result.tools.length).toBeGreaterThanOrEqual(5);
  });
  
  it('lists documentation sets', async () => {
    const response = await sendRequest('tools/call', {
      name: 'list_documentation_sets'
    });
    
    expect(response.error).toBeUndefined();
    expect(response.result).toBeDefined();
  });
  
  it('switches to test-docs-a', async () => {
    const response = await sendRequest('tools/call', {
      name: 'switch_documentation',
      arguments: { docName: 'test-docs-a' }
    });
    
    expect(response.error).toBeUndefined();
    expect(response.result).toBeDefined();
  });
  
  it('searches and returns results from test-docs-a', async () => {
    const response = await sendRequest('tools/call', {
      name: 'search',
      arguments: { query: 'installation' }
    });
    
    expect(response.error).toBeUndefined();
    expect(response.result).toBeDefined();
    expect(response.result.content).toBeDefined();
    expect(response.result.content.length).toBeGreaterThan(0);
  });
  
  it('switches to test-docs-b', async () => {
    const response = await sendRequest('tools/call', {
      name: 'switch_documentation',
      arguments: { docName: 'test-docs-b' }
    });
    
    expect(response.error).toBeUndefined();
    expect(response.result).toBeDefined();
  });
  
  it('switches back to test-docs-a', async () => {
    const response = await sendRequest('tools/call', {
      name: 'switch_documentation',
      arguments: { docName: 'test-docs-a' }
    });
    
    expect(response.error).toBeUndefined();
    expect(response.result).toBeDefined();
  });
});
