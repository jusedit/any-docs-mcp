# Quick Start Guide

Get started with AnyDocsMCP in 5 minutes.

## Prerequisites

- Python 3.10+
- Node.js 18+
- OpenRouter API key ([get one here](https://openrouter.ai/))

## Installation

### 1. Clone/Download this repository

You already have it if you're reading this!

### 2. Install Python dependencies

```bash
cd scraper
pip install -r requirements.txt
```

### 3. Install Node.js dependencies

```bash
cd ../mcp-server
npm install
npm run build
```

## First Documentation Set

### 1. Set your API key

```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-..."

# Windows CMD
set OPENROUTER_API_KEY=sk-or-v1-...

# Linux/Mac
export OPENROUTER_API_KEY=sk-or-v1-...
```

### 2. Scrape your first documentation

Let's use VitePress as an example (small, well-structured docs):

```bash
cd scraper
python cli.py add --url https://vitepress.dev/ --name vitepress
```

This will:
- ✨ Analyze the site with AI
- 📥 Scrape all documentation pages
- 📝 Convert to structured Markdown
- 💾 Store in `%APPDATA%\AnyDocsMCP\docs\vitepress\v1\`

Wait 2-3 minutes for completion.

### 3. Configure MCP server

Create `mcp-server/config.json`:

```json
{
  "activeDocs": "vitepress"
}
```

### 4. Test the MCP server

```bash
cd ../mcp-server
npm start
```

You should see:
```
[vitepress-mcp] Loading documentation from: ...
[vitepress-mcp] Building index...
[vitepress-mcp] Index ready.
[vitepress-mcp] Server running on stdio
```

Press Ctrl+C to stop.

## Use in Windsurf/Claude Desktop

### 1. Find your settings file

**Windows Windsurf:**
```
%APPDATA%\Windsurf\User\globalStorage\codeium.windsurf\settings\mcp_settings.json
```

**Mac Windsurf:**
```
~/Library/Application Support/Windsurf/User/globalStorage/codeium.windsurf/settings/mcp_settings.json
```

**Claude Desktop:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### 2. Add MCP server configuration

Replace `YOUR_PATH` with the actual path to this repository:

```json
{
  "mcpServers": {
    "vitepress-docs": {
      "command": "node",
      "args": ["C:/YOUR_PATH/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "vitepress"
      }
    }
  }
}
```

### 3. Restart Windsurf/Claude Desktop

After restart, you'll have access to documentation search tools!

## Try It Out

In Windsurf/Claude, try asking:

- "Search the vitepress documentation for getting started"
- "Show me code examples from the vitepress docs about markdown"
- "What are the main sections in the vitepress documentation?"

The AI will use the MCP tools to search and retrieve documentation content!

## Add More Documentation

```bash
cd scraper

# Add Vue docs
python cli.py add --url https://vuejs.org/guide/introduction.html --name vue

# Add Svelte docs
python cli.py add --url https://svelte.dev/docs/introduction --name svelte

# List all your documentation sets
python cli.py list
```

Then add more MCP server entries to serve different docs simultaneously!

## What's Next?

- Read [USAGE.md](USAGE.md) for detailed usage instructions
- Read [TESTING.md](TESTING.md) for testing different documentation sites
- Check [README.md](README.md) for architecture details

## Troubleshooting

**"OpenRouter API key required"**
- Set the `OPENROUTER_API_KEY` environment variable

**"No navigation links found"**
- The site structure might be complex. Check the generated config.json and adjust selectors manually

**"File not found" in MCP server**
- Make sure you've scraped the documentation first with `cli.py add`
- Check that `activeDocs` in config.json matches the scraped documentation name

**MCP server not appearing in Windsurf**
- Verify the path to `dist/index.js` is correct (use full absolute path)
- Check Windsurf logs for errors
- Make sure you ran `npm run build` first

## Quick Reference

### Common Commands

```bash
# Add documentation
python cli.py add --url <URL> --name <NAME>

# Update documentation (new version)
python cli.py update --name <NAME>

# List all documentation sets
python cli.py list

# Build MCP server
npm run build

# Run MCP server
npm start
```

### Storage Location

Documentation is stored in:
- **Windows:** `%APPDATA%\AnyDocsMCP\docs\`
- **Mac:** `~/Library/Application Support/AnyDocsMCP/docs/`
- **Linux:** `~/.local/share/AnyDocsMCP/docs/`

### MCP Tools Available

- `search` - Search documentation
- `get_overview` - Get overview of all sections
- `list_files` - List all documentation files
- `get_file_toc` - Get table of contents for a file
- `get_section` - Get specific section by title
- `find_code_examples` - Search for code examples
