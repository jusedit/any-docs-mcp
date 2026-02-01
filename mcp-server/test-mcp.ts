import { spawn } from 'child_process';
import { join } from 'path';

interface MCPRequest {
    jsonrpc: string;
    id: number;
    method: string;
    params?: any;
}

interface MCPResponse {
    jsonrpc: string;
    id: number;
    result?: any;
    error?: any;
}

class MCPTester {
    private process: any;
    private requestId = 1;
    private responseBuffer = '';

    constructor(private docName: string) {}

    async start(): Promise<void> {
        return new Promise((resolve, reject) => {
            const env = { ...process.env, ANYDOCS_ACTIVE: this.docName };
            
            this.process = spawn('node', [join(__dirname, 'index.js')], {
                env,
                stdio: ['pipe', 'pipe', 'pipe']
            });

            this.process.stderr.on('data', (data: Buffer) => {
                console.log('[Server Log]', data.toString());
            });

            this.process.stdout.on('data', (data: Buffer) => {
                this.responseBuffer += data.toString();
            });

            setTimeout(resolve, 2000);
        });
    }

    async sendRequest(method: string, params?: any): Promise<any> {
        const request: MCPRequest = {
            jsonrpc: '2.0',
            id: this.requestId++,
            method,
            params
        };

        this.responseBuffer = '';
        this.process.stdin.write(JSON.stringify(request) + '\n');

        await new Promise(resolve => setTimeout(resolve, 1000));

        const lines = this.responseBuffer.split('\n').filter(l => l.trim());
        for (const line of lines) {
            try {
                const response: MCPResponse = JSON.parse(line);
                if (response.id === request.id - 1) {
                    return response.result;
                }
            } catch (e) {
                // Ignore parse errors
            }
        }

        return null;
    }

    async stop(): Promise<void> {
        if (this.process) {
            this.process.kill();
        }
    }
}

async function testOnOffice() {
    console.log('\n' + '='.repeat(80));
    console.log('TESTING ONOFFICE API DOCUMENTATION');
    console.log('='.repeat(80) + '\n');

    const tester = new MCPTester('onoffice');
    await tester.start();

    console.log('Question 1: How to modify search criteria?\n');
    const result1 = await tester.sendRequest('tools/call', {
        name: 'search',
        arguments: {
            query: 'modify search criteria filter',
            maxResults: 5
        }
    });
    
    if (result1 && result1.content) {
        console.log(result1.content[0].text.substring(0, 2000));
        console.log('\n[...truncated for brevity...]\n');
    }

    console.log('\n' + '-'.repeat(80) + '\n');

    console.log('Question 2: Wie werden zuständige Betreuer von einem Kunden aufgerufen?\n');
    const result2 = await tester.sendRequest('tools/call', {
        name: 'search',
        arguments: {
            query: 'zuständige betreuer kunden relations',
            maxResults: 5
        }
    });

    if (result2 && result2.content) {
        console.log(result2.content[0].text.substring(0, 2000));
        console.log('\n[...truncated for brevity...]\n');
    }

    await tester.stop();
}

async function testShopware() {
    console.log('\n' + '='.repeat(80));
    console.log('TESTING SHOPWARE 6 DEVELOPER DOCUMENTATION');
    console.log('='.repeat(80) + '\n');

    const tester = new MCPTester('shopware6');
    await tester.start();

    console.log('Question 1: What is the difference between apps and plugins? When to use what?\n');
    const result1 = await tester.sendRequest('tools/call', {
        name: 'search',
        arguments: {
            query: 'difference between apps and plugins when to use',
            maxResults: 5
        }
    });

    if (result1 && result1.content) {
        console.log(result1.content[0].text.substring(0, 2000));
        console.log('\n[...truncated for brevity...]\n');
    }

    console.log('\n' + '-'.repeat(80) + '\n');

    console.log('Question 2: How to retrieve product data?\n');
    const result2 = await tester.sendRequest('tools/call', {
        name: 'search',
        arguments: {
            query: 'retrieve product data API read',
            maxResults: 5
        }
    });

    if (result2 && result2.content) {
        console.log(result2.content[0].text.substring(0, 2000));
        console.log('\n[...truncated for brevity...]\n');
    }

    await tester.stop();
}

async function main() {
    console.log('AnyDocsMCP Test Suite');
    console.log('Testing MCP servers with scraped documentation\n');

    try {
        await testOnOffice();
        await testShopware();
        
        console.log('\n' + '='.repeat(80));
        console.log('ALL TESTS COMPLETED');
        console.log('='.repeat(80));
    } catch (error) {
        console.error('Test error:', error);
        process.exit(1);
    }
}

main();
