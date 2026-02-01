# Testing Guide

This guide walks through testing the AnyDocsMCP system with real documentation sites.

## Prerequisites

1. Python 3.10+ installed
2. Node.js 18+ installed
3. OpenRouter API key (get from https://openrouter.ai/)

## Setup for Testing

### 1. Install Dependencies

```bash
# Install scraper dependencies
cd scraper
pip install -r requirements.txt

# Install MCP server dependencies
cd ../mcp-server
npm install
```

### 2. Set API Key

```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="your_api_key_here"

# Windows CMD
set OPENROUTER_API_KEY=your_api_key_here
```

## Test Cases

### Test 1: VitePress Documentation (Easy)

VitePress is a common documentation framework with clear structure.

```bash
cd scraper
python cli.py add --url https://vitepress.dev/ --name vitepress --display-name "VitePress Documentation"
```

**Expected behavior:**
- LLM should identify `.VPDoc` or similar content selectors
- Navigation from `.VPSidebar` or similar
- Should create ~10-30 markdown files
- 2-5 minute scraping time

**Verification:**
```bash
python cli.py list
# Should show vitepress with page/file counts

# Check output
dir %APPDATA%\AnyDocsMCP\docs\vitepress\v1
```

### Test 2: Docusaurus Documentation (Medium)

```bash
python cli.py add --url https://docusaurus.io/docs --name docusaurus --display-name "Docusaurus Docs"
```

**Expected behavior:**
- Different structure than VitePress
- Should identify `.theme-doc-markdown` or similar
- Navigation from sidebar
- ~20-50 files depending on version

### Test 3: MCP Server with Scraped Docs

#### 3a. Configure MCP Server

Create `mcp-server/config.json`:

```json
{
  "activeDocs": "vitepress",
  "serverName": "vitepress-mcp"
}
```

#### 3b. Build and Test

```bash
cd mcp-server
npm run build

# Test run (should build index and wait for input)
npm start
```

Expected console output:
```
[vitepress-mcp] Loading documentation from: C:\Users\...\AppData\Roaming\AnyDocsMCP\docs\vitepress\v1
[vitepress-mcp] Active documentation: vitepress
[vitepress-mcp] Building index...
[vitepress-mcp] Index ready.
[vitepress-mcp] Server running on stdio
```

Press Ctrl+C to stop.

#### 3c. Test with MCP Inspector

Install MCP Inspector:
```bash
npm install -g @modelcontextprotocol/inspector
```

Run inspector:
```bash
mcp-inspector node dist/index.js
```

Open browser to http://localhost:5173 and test tools:
- `list_files` - should return all markdown files
- `get_overview` - should show documentation structure
- `search` with query "getting started" - should return relevant sections

### Test 4: Update/Re-scrape

```bash
cd scraper
python cli.py update --name vitepress
```

**Expected behavior:**
- Creates v2 directory
- Scrapes fresh content
- Updates metadata.json

**Verification:**
```bash
dir %APPDATA%\AnyDocsMCP\docs\vitepress
# Should show both v1 and v2 directories

python cli.py list
# Should show updated timestamp
```

### Test 5: Complex Documentation Site

Try a more complex site with deeper hierarchy:

```bash
python cli.py add --url https://developer.mozilla.org/en-US/docs/Web --name mdn-web --display-name "MDN Web Docs"
```

**Note:** MDN is very large. This will take 15-30 minutes and create 100+ files. 
Consider using a smaller subsection or hitting Ctrl+C after ~50 pages for testing.

### Test 6: Multiple MCP Servers

Test running multiple documentation sets simultaneously.

#### 6a. Scrape Multiple Sites

```bash
cd scraper
python cli.py add --url https://vuejs.org/guide/introduction.html --name vue
python cli.py add --url https://svelte.dev/docs/introduction --name svelte
```

#### 6b. Configure Windsurf/Claude Desktop

Edit your MCP settings file:

**Windows:** `%APPDATA%\Windsurf\User\globalStorage\codeium.windsurf\settings\mcp_settings.json`

```json
{
  "mcpServers": {
    "vitepress-docs": {
      "command": "node",
      "args": ["C:/Users/YOUR_USERNAME/.windsurf/worktrees/AnyDocsMCP/AnyDocsMCP-0078e275/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "vitepress"
      }
    },
    "vue-docs": {
      "command": "node",
      "args": ["C:/Users/YOUR_USERNAME/.windsurf/worktrees/AnyDocsMCP/AnyDocsMCP-0078e275/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "vue"
      }
    }
  }
}
```

#### 6c. Restart Windsurf

After restart, you should see both MCP servers available with their respective tools.

## Validation Checklist

### Scraper Validation

- [ ] LLM successfully analyzes site structure
- [ ] Extracts navigation links (>10 links for typical docs)
- [ ] Content extraction produces readable markdown
- [ ] Code blocks are preserved correctly
- [ ] Source URLs are maintained
- [ ] Files are grouped logically
- [ ] Config is saved correctly
- [ ] Metadata includes accurate counts

### MCP Server Validation

- [ ] Server starts without errors
- [ ] Index builds successfully
- [ ] `list_files` returns all files
- [ ] `get_overview` shows structure
- [ ] `search` finds relevant content
- [ ] `get_section` retrieves correct sections
- [ ] `find_code_examples` locates code snippets
- [ ] Source URLs are displayed in results

### Integration Validation

- [ ] Multiple documentation sets can coexist
- [ ] Version management works (v1, v2, etc.)
- [ ] Re-scraping creates new version
- [ ] MCP server uses latest version automatically
- [ ] Multiple MCP servers can run simultaneously
- [ ] Works in Windsurf/Claude Desktop

## Common Issues and Solutions

### Issue: "No navigation links found"

**Cause:** LLM couldn't identify navigation structure

**Solution:**
1. Check the site's HTML for navigation element
2. Manually edit config.json and add correct selector:
   ```json
   "navigation_selectors": ["nav.sidebar", ".docs-sidebar", "#sidebar"]
   ```
3. Re-run update command

### Issue: "No content extracted"

**Cause:** Content selector is incorrect

**Solution:**
1. Inspect the documentation page
2. Find the main content container ID/class
3. Edit config.json:
   ```json
   "content_selectors": ["main.content", "article.doc", ".markdown-body"]
   ```

### Issue: Too many/few files created

**Cause:** Grouping strategy doesn't match site structure

**Solution:**
Edit config.json and change `grouping_strategy`:
- `path_depth_2` - fewer, larger files
- `path_depth_3` - more, smaller files
- `single_file` - everything in one file

Then run update to re-scrape.

### Issue: MCP server can't find documentation

**Cause:** activeDocs name doesn't match scraped docs

**Solution:**
1. Run `python cli.py list` to see available docs
2. Update config.json with exact name:
   ```json
   "activeDocs": "exact-name-from-list"
   ```

### Issue: Search returns no results

**Cause:** Index might not include the content

**Solution:**
1. Check if files exist in version directory
2. Verify files contain content (open .md files)
3. Try broader search terms
4. Check `fileFilter` isn't excluding results

## Performance Benchmarks

Typical performance on standard documentation sites:

| Metric | Small Site (50 pages) | Medium Site (200 pages) | Large Site (500+ pages) |
|--------|----------------------|------------------------|------------------------|
| Scrape time | 1-2 min | 5-10 min | 15-30 min |
| Storage size | 1-5 MB | 5-20 MB | 20-100 MB |
| Files created | 5-15 | 15-40 | 40-100 |
| Index build time | <1 sec | 1-2 sec | 2-5 sec |
| Search latency | <50 ms | <100 ms | <200 ms |

## Debugging

### Enable Verbose Logging

Edit scraper files to add more print statements, or run with Python's verbose flag:

```bash
python -v cli.py add --url <URL> --name <NAME>
```

### Check MCP Server Logs

The server logs to stderr, which should appear in Windsurf's output panel or terminal.

### Inspect Generated Config

```bash
type %APPDATA%\AnyDocsMCP\docs\<doc-name>\config.json
```

### Manual Index Test

```bash
cd mcp-server
npm run dev
# Then manually send MCP protocol messages
```

## Success Criteria

The system is working correctly if:

1. ✅ Can scrape at least 3 different documentation sites
2. ✅ LLM analysis succeeds >80% of the time
3. ✅ Content extraction preserves markdown formatting
4. ✅ Code blocks are correctly identified and extracted
5. ✅ MCP server starts and builds index without errors
6. ✅ Search returns relevant results
7. ✅ Multiple documentation sets can coexist
8. ✅ Can integrate with Windsurf/Claude Desktop
