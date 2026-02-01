import { spawn } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

class MCPClient {
    constructor(docName) {
        this.docName = docName;
        this.process = null;
        this.requestId = 1;
        this.responseBuffer = '';
        this.pendingRequests = new Map();
    }

    async start() {
        return new Promise((resolve, reject) => {
            const env = { 
                ...process.env, 
                ANYDOCS_ACTIVE: this.docName,
                OPENROUTER_API_KEY: process.env.OPENROUTER_API_KEY
            };
            
            this.process = spawn('node', [join(__dirname, 'dist', 'index.js')], {
                env,
                stdio: ['pipe', 'pipe', 'pipe']
            });

            this.process.stderr.on('data', (data) => {
                console.log('[MCP Server]', data.toString().trim());
            });

            this.process.stdout.on('data', (data) => {
                const text = data.toString();
                this.responseBuffer += text;
                
                // Try to parse complete JSON-RPC messages
                const lines = this.responseBuffer.split('\n');
                this.responseBuffer = lines.pop() || ''; // Keep incomplete line
                
                for (const line of lines) {
                    if (!line.trim()) continue;
                    try {
                        const response = JSON.parse(line);
                        if (response.id && this.pendingRequests.has(response.id)) {
                            const { resolve } = this.pendingRequests.get(response.id);
                            this.pendingRequests.delete(response.id);
                            resolve(response);
                        }
                    } catch (e) {
                        // Ignore parse errors for partial responses
                    }
                }
            });

            this.process.on('error', reject);

            // Wait for server to be ready
            setTimeout(resolve, 3000);
        });
    }

    async sendRequest(method, params = {}) {
        const id = this.requestId++;
        const request = {
            jsonrpc: '2.0',
            id,
            method,
            params
        };

        return new Promise((resolve, reject) => {
            this.pendingRequests.set(id, { resolve, reject });
            this.process.stdin.write(JSON.stringify(request) + '\n');
            
            // Timeout after 5 minutes for scraping
            setTimeout(() => {
                if (this.pendingRequests.has(id)) {
                    this.pendingRequests.delete(id);
                    reject(new Error('Request timeout'));
                }
            }, 300000);
        });
    }

    stop() {
        if (this.process) {
            this.process.kill();
        }
    }
}

async function testScraping() {
    console.log('\n' + '='.repeat(100));
    console.log('TESTING: Scrape Documentation Endpoint with Synthflow API');
    console.log('='.repeat(100) + '\n');

    const client = new MCPClient('shopware6'); // Start with existing docs
    
    try {
        console.log('Starting MCP server...');
        await client.start();
        console.log('✓ MCP server started\n');

        // List available tools
        console.log('Listing available tools...');
        const toolsResponse = await client.sendRequest('tools/list');
        const tools = toolsResponse.result.tools;
        console.log(`✓ Found ${tools.length} tools:`);
        tools.forEach(tool => {
            console.log(`  - ${tool.name}`);
        });
        console.log('');

        // List current documentation sets
        console.log('Listing current documentation sets...');
        const listResponse = await client.sendRequest('tools/call', {
            name: 'list_documentation_sets',
            arguments: {}
        });
        console.log(listResponse.result.content[0].text);
        console.log('');

        // Scrape Synthflow documentation
        console.log('━'.repeat(100));
        console.log('SCRAPING: Synthflow API Documentation');
        console.log('URL: https://docs.synthflow.ai/getting-started-with-your-api');
        console.log('━'.repeat(100) + '\n');

        const scrapeResponse = await client.sendRequest('tools/call', {
            name: 'scrape_documentation',
            arguments: {
                url: 'https://docs.synthflow.ai/getting-started-with-your-api',
                name: 'synthflow',
                displayName: 'Synthflow API Documentation'
            }
        });

        console.log(scrapeResponse.result.content[0].text);
        console.log('');

        if (!scrapeResponse.result.isError) {
            // Switch to the new documentation
            console.log('━'.repeat(100));
            console.log('SWITCHING: To Synthflow documentation');
            console.log('━'.repeat(100) + '\n');

            const switchResponse = await client.sendRequest('tools/call', {
                name: 'switch_documentation',
                arguments: {
                    name: 'synthflow'
                }
            });

            console.log(switchResponse.result.content[0].text);
            console.log('');

            if (!switchResponse.result.isError) {
                // Test searching the new documentation
                console.log('━'.repeat(100));
                console.log('TESTING: Search Synthflow Documentation');
                console.log('━'.repeat(100) + '\n');

                console.log('Query: "API authentication"');
                const searchResponse = await client.sendRequest('tools/call', {
                    name: 'search',
                    arguments: {
                        query: 'API authentication',
                        maxResults: 3
                    }
                });

                console.log(searchResponse.result.content[0].text.substring(0, 1500));
                console.log('\n[...truncated for brevity...]\n');

                console.log('\nQuery: "getting started"');
                const searchResponse2 = await client.sendRequest('tools/call', {
                    name: 'search',
                    arguments: {
                        query: 'getting started',
                        maxResults: 3
                    }
                });

                console.log(searchResponse2.result.content[0].text.substring(0, 1500));
                console.log('\n[...truncated for brevity...]\n');

                // Get overview
                console.log('\nGetting documentation overview...');
                const overviewResponse = await client.sendRequest('tools/call', {
                    name: 'get_overview',
                    arguments: {}
                });

                console.log(overviewResponse.result.content[0].text.substring(0, 1000));
                console.log('\n[...truncated for brevity...]\n');
            }
        }

        console.log('\n' + '='.repeat(100));
        console.log('✓ TEST COMPLETED');
        console.log('='.repeat(100) + '\n');

    } catch (error) {
        console.error('\n✗ TEST FAILED:', error.message);
        console.error(error.stack);
        process.exit(1);
    } finally {
        client.stop();
    }
}

testScraping();
