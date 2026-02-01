import { MarkdownParser } from './dist/markdown-parser.js';
import path from 'path';
import os from 'os';

const appdata = process.env.APPDATA || path.join(os.homedir(), '.local', 'share');
const storageRoot = path.join(appdata, 'AnyDocsMCP', 'docs');

async function testOnOffice() {
    console.log('\n' + '='.repeat(100));
    console.log('TESTING: onOffice API Documentation');
    console.log('='.repeat(100) + '\n');

    const docsPath = path.join(storageRoot, 'onoffice', 'v1');
    const parser = new MarkdownParser(docsPath, 'onoffice');
    
    console.log(`Loading documentation from: ${docsPath}`);
    console.log('Building index...');
    const index = parser.buildIndex();
    console.log(`✓ Index built: ${index.allSections.length} sections from ${index.files.size} files\n`);

    // Question 1
    console.log('━'.repeat(100));
    console.log('QUESTION 1: How to modify search criteria?');
    console.log('━'.repeat(100) + '\n');
    
    const results1 = parser.search('modify search criteria filter', { maxResults: 3 });
    
    console.log(`Found ${results1.length} results:\n`);
    results1.forEach((section, idx) => {
        console.log(`[${idx + 1}] ${section.title}`);
        console.log(`    File: ${section.file}.md`);
        if (section.sourceUrl) console.log(`    Source: ${section.sourceUrl}`);
        console.log(`    Content preview: ${section.content.substring(0, 300).replace(/\n/g, ' ')}...`);
        console.log('');
    });

    // Question 2
    console.log('\n' + '━'.repeat(100));
    console.log('QUESTION 2: Wie werden zuständige Betreuer von einem Kunden aufgerufen?');
    console.log('(How are responsible supervisors/contacts called from a customer?)');
    console.log('━'.repeat(100) + '\n');
    
    const results2 = parser.search('zuständige betreuer kunden relations', { maxResults: 3 });
    
    console.log(`Found ${results2.length} results:\n`);
    results2.forEach((section, idx) => {
        console.log(`[${idx + 1}] ${section.title}`);
        console.log(`    File: ${section.file}.md`);
        if (section.sourceUrl) console.log(`    Source: ${section.sourceUrl}`);
        console.log(`    Content preview: ${section.content.substring(0, 300).replace(/\n/g, ' ')}...`);
        if (section.codeBlocks.length > 0) {
            console.log(`    Code examples: ${section.codeBlocks.length}`);
        }
        console.log('');
    });
}

async function testShopware() {
    console.log('\n' + '='.repeat(100));
    console.log('TESTING: Shopware 6 Developer Documentation');
    console.log('='.repeat(100) + '\n');

    const docsPath = path.join(storageRoot, 'shopware6', 'v1');
    const parser = new MarkdownParser(docsPath, 'shopware6');
    
    console.log(`Loading documentation from: ${docsPath}`);
    console.log('Building index...');
    const index = parser.buildIndex();
    console.log(`✓ Index built: ${index.allSections.length} sections from ${index.files.size} files\n`);

    // Question 1
    console.log('━'.repeat(100));
    console.log('QUESTION 1: What is the difference between apps and plugins? When to use what?');
    console.log('━'.repeat(100) + '\n');
    
    const results1 = parser.search('difference between apps and plugins when to use', { maxResults: 3 });
    
    console.log(`Found ${results1.length} results:\n`);
    results1.forEach((section, idx) => {
        console.log(`[${idx + 1}] ${section.title}`);
        console.log(`    File: ${section.file}.md`);
        if (section.sourceUrl) console.log(`    Source: ${section.sourceUrl}`);
        console.log(`    Content preview: ${section.content.substring(0, 400).replace(/\n/g, ' ')}...`);
        console.log('');
    });

    // Question 2
    console.log('\n' + '━'.repeat(100));
    console.log('QUESTION 2: How to retrieve product data?');
    console.log('━'.repeat(100) + '\n');
    
    const results2 = parser.search('retrieve product data read API', { maxResults: 3 });
    
    console.log(`Found ${results2.length} results:\n`);
    results2.forEach((section, idx) => {
        console.log(`[${idx + 1}] ${section.title}`);
        console.log(`    File: ${section.file}.md`);
        if (section.sourceUrl) console.log(`    Source: ${section.sourceUrl}`);
        console.log(`    Content preview: ${section.content.substring(0, 400).replace(/\n/g, ' ')}...`);
        if (section.codeBlocks.length > 0) {
            console.log(`    Code examples: ${section.codeBlocks.length}`);
            console.log(`    First example (${section.codeBlocks[0].language}):`);
            console.log(section.codeBlocks[0].code.substring(0, 200));
        }
        console.log('');
    });
}

async function main() {
    console.log('\n');
    console.log('╔════════════════════════════════════════════════════════════════════════════════════════════════╗');
    console.log('║                           AnyDocsMCP - MCP Server Test Suite                                  ║');
    console.log('╚════════════════════════════════════════════════════════════════════════════════════════════════╝');

    try {
        await testOnOffice();
        await testShopware();
        
        console.log('\n' + '='.repeat(100));
        console.log('✓ ALL TESTS COMPLETED SUCCESSFULLY');
        console.log('='.repeat(100) + '\n');
    } catch (error) {
        console.error('\n✗ TEST FAILED:', error.message);
        console.error(error.stack);
        process.exit(1);
    }
}

main();
