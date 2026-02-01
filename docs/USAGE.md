# Usage Guide

## Setup

### 1. Install Scraper Dependencies

```bash
cd scraper
pip install -r requirements.txt
```

### 2. Configure OpenRouter API Key

Create a `.env` file or set environment variable:

```bash
# Windows (PowerShell)
$env:OPENROUTER_API_KEY="your_key_here"

# Windows (CMD)
set OPENROUTER_API_KEY=your_key_here

# Linux/Mac
export OPENROUTER_API_KEY=your_key_here
```

Get your API key from: https://openrouter.ai/

### 3. Install MCP Server Dependencies

```bash
cd ../mcp-server
npm install
```

## Adding Documentation

### Basic Usage

```bash
cd scraper
python cli.py add --url https://docs.example.com --name example-docs
```

The system will:
1. Use LLM to analyze the site structure
2. Extract CSS selectors for content and navigation
3. Scrape all documentation pages
4. Convert to Markdown with proper structure
5. Store in `%APPDATA%\AnyDocsMCP\docs\example-docs\v1\`

### With Custom Display Name

```bash
python cli.py add --url https://docs.example.com --name example --display-name "Example Documentation"
```

### Re-scraping (New Version)

```bash
python cli.py update --name example-docs
```

This creates a new version (v2, v3, etc.) while keeping old versions.

### List All Documentation Sets

```bash
python cli.py list
```

## Running the MCP Server

### 1. Create Configuration

Create `mcp-server/config.json`:

```json
{
  "activeDocs": "example-docs",
  "serverName": "example-docs-mcp"
}
```

### 2. Build and Run

```bash
cd mcp-server
npm run build
npm start
```

### 3. Use in Windsurf/Claude Desktop

Add to your MCP settings:

```json
{
  "mcpServers": {
    "example-docs": {
      "command": "node",
      "args": ["C:/path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "example-docs"
      }
    }
  }
}
```

## Advanced Configuration

### Custom Storage Location

In `config.json`:

```json
{
  "activeDocs": "example-docs",
  "storageRoot": "D:\\MyDocs\\Documentation"
}
```

Or via environment:

```bash
set ANYDOCS_STORAGE_ROOT=D:\MyDocs\Documentation
```

### Multiple MCP Servers for Different Docs

You can run multiple MCP servers, each serving different documentation:

**Windsurf/Claude Desktop config:**

```json
{
  "mcpServers": {
    "react-docs": {
      "command": "node",
      "args": ["C:/path/to/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "react",
        "SERVER_NAME": "react-docs-mcp"
      }
    },
    "python-docs": {
      "command": "node",
      "args": ["C:/path/to/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "python",
        "SERVER_NAME": "python-docs-mcp"
      }
    }
  }
}
```

## MCP Tools

Once connected, the following tools are available:

### `search`
Search documentation with relevance scoring.

**Parameters:**
- `query` (required): Search terms
- `maxResults` (optional): Number of results (default: 10)
- `fileFilter` (optional): Filter by filename
- `titlesOnly` (optional): Return only titles, not full content

**Example:**
```
Search for "authentication" in the documentation
```

### `get_overview`
Get high-level overview of all documentation sections.

### `get_file_toc`
Get table of contents for a specific file.

**Parameters:**
- `fileName` (required): Filename without .md extension

### `get_section`
Retrieve specific section by title.

**Parameters:**
- `title` (required): Section title to search
- `fileName` (optional): Filter by file

### `list_files`
List all available documentation files.

### `find_code_examples`
Search for code snippets.

**Parameters:**
- `query` (required): Code to search for
- `language` (optional): Filter by language (e.g., "python", "javascript")
- `maxResults` (optional): Number of results (default: 5)

## Tips

### Site Analysis

The LLM analyzer works best with:
- Well-structured documentation sites
- Consistent CSS classes/IDs
- Clear navigation menus
- Standard documentation frameworks (VitePress, Docusaurus, etc.)

If analysis fails, you may need to manually create a config file.

### Grouping Strategies

The scraper supports different grouping strategies:
- `path_depth_2`: Group by first 2 URL path segments (default)
- `path_depth_3`: Group by first 3 URL path segments
- `single_file`: Put everything in one file (not recommended for large docs)

### Storage Structure

```
%APPDATA%\AnyDocsMCP\docs\
├── example-docs/
│   ├── config.json          # Site configuration
│   ├── metadata.json        # Statistics
│   ├── v1/                  # First scrape
│   │   ├── getting-started.md
│   │   ├── api-reference.md
│   │   └── ...
│   └── v2/                  # After re-scrape
│       └── ...
```

### Performance

- Initial scraping: Depends on site size (1-10 minutes typical)
- MCP index building: 1-5 seconds on startup
- Search queries: <100ms typically

## Troubleshooting

### "No navigation links found"

The LLM might have identified incorrect selectors. Check the config file and adjust `navigation_selectors`.

### "No content extracted"

Check `content_selectors` in the config. Try adding more selectors or adjusting `exclude_selectors`.

### "Rate limited"

Add delay between requests by modifying `scraper_engine.py` `request_delay` parameter.

### MCP Server not starting

- Verify `activeDocs` matches an existing documentation set
- Check that documentation was scraped successfully
- Ensure at least one version directory exists

## Example Workflows

### Adding React Documentation

```bash
cd scraper
python cli.py add --url https://react.dev --name react --display-name "React Official Docs"
```

### Adding Vue Documentation

```bash
python cli.py add --url https://vuejs.org/guide/introduction.html --name vue --display-name "Vue.js Guide"
```

### Keeping Documentation Updated

```bash
# Weekly cron job / scheduled task
python cli.py update --name react
python cli.py update --name vue
```
