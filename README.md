# AnyDocsMCP 🚀

> Universal Documentation Pipeline for AI Assistants

Transform any documentation website into searchable knowledge for your AI.

## Overview

AnyDocsMCP automatically scrapes documentation sites and serves them via MCP (Model Context Protocol) to AI assistants like Windsurf/Cascade.

**Key Features:**
- 🤖 **4-Mode Discovery**: Sitemap → Navigation → Crawl → WebDriver (escalation)
- 📚 **Multi-Doc Support**: Manage unlimited documentation sets
- 🔄 **Version Management**: Automatic versioning with preserved history
- 🔍 **Semantic Search**: Full-text search with <200ms response
- 🌐 **MCP Integration**: Direct integration with AI assistants

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenRouter API Key ([Sign up](https://openrouter.ai/))

### Installation

```bash
git clone https://github.com/jusedit/any-docs-mcp.git
cd any-docs-mcp

# Install Python dependencies
cd scraper
pip install -r requirements.txt

# Install MCP server
cd ..
npm install
```

### Configuration

Create `%APPDATA%\AnyDocsMCP\config\settings.json`:

```json
{
  "llm_provider": "openrouter",
  "openrouter_api_key": "your-api-key-here",
  "default_model": "anthropic/claude-3.5-sonnet",
  "docs_base_dir": "%APPDATA%\\AnyDocsMCP\\docs"
}
```

### Add Documentation

```bash
cd scraper
python doc_manager.py scrape https://docs.python.org/3/ --name python3
```

### Start MCP Server

```bash
npm start
```

## Verified Documentation Sites

**Tested: 49/49 sites (100% success)** with WebDriver escalation for bot-protected sites.

| Category | Sites | Mode Distribution |
|----------|-------|-------------------|
| **Languages** | Python, Node.js, TypeScript, Java, Kotlin, Rust, Go, .NET | Sitemap/Navigation |
| **Frameworks** | React, Vue, Angular, Svelte, Django, Flask, FastAPI, Rails, Laravel, Spring Boot | Mixed (WebDriver for JS-heavy) |
| **Databases** | PostgreSQL, MySQL, SQLite, Redis, MongoDB, Elasticsearch | Sitemap/Crawl |
| **DevOps** | Docker, Kubernetes, Helm, Terraform, Ansible, Nginx | Sitemap |
| **Cloud/SaaS** | AWS, Azure, GitHub, OpenAI, Stripe, Twilio | WebDriver for protected |

**WebDriver used**: 12 sites (MySQL, OpenAI, AWS, Spring Boot, React, Tailwind, etc.)

## Architecture

```
Documentation URL
       ↓
┌─────────────────────────────────────────────────────────┐
│  URL Discovery (Multi-Mode)                             │
│  Sitemap → Navigation → Crawl → WebDriver               │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  Content Extract                                        │
│  BeautifulSoup + markdownify                            │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  Content Clean                                          │
│  Remove UI artifacts, normalize code blocks             │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  File Storage                                           │
│  JSON metadata + Versioned Markdown files               │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  MCP Server (12 Tools)                                  │
│  ─────────────────────────────────────────────────────  │
│  Management: scrape_documentation, get_scrape_status,   │
│              update_documentation, list_documentation_  │
│              sets, switch_documentation                 │
│  ─────────────────────────────────────────────────────  │
│  Navigation: search, get_overview, get_file_toc,        │
│              get_section, list_files, find_code_examples│
└─────────────────────────────────────────────────────────┘
```

## CLI Commands

```bash
# Scrape new documentation
python doc_manager.py scrape <url> --name <name>

# Search documentation
python doc_manager.py search <name> "your query"

# List installed docs
python doc_manager.py list

# Switch active doc
python doc_manager.py use <name>
```

## MCP Tools

### Documentation Management

**`scrape_documentation`**
- Scrape a new documentation site asynchronously
- Parameters:
  - `url` (required): Start URL of the documentation site
  - `name` (required): Unique identifier for this documentation set
  - `displayName` (optional): Human-readable name
- Returns: Job ID to track progress

**`get_scrape_status`**
- Check the status of a scraping job
- Parameters:
  - `jobId` (required): Job ID returned by scrape_documentation
- Returns: Progress, phase, current URL, completion status

**`update_documentation`**
- Re-scrape existing documentation to get latest content
- Parameters:
  - `name` (required): Name of documentation set to update
  - `force` (optional): Force update even if refresh timeout not reached
- Returns: Job ID to track progress

**`list_documentation_sets`**
- List all available documentation sets with metadata
- Parameters: None
- Returns: List of all docs with status, pages, last scraped time, refresh status

**`switch_documentation`**
- Switch to a different documentation set
- Parameters:
  - `name` (required): Name of documentation set to switch to
- Returns: Confirmation message

### Search & Navigation

**`search`**
- Full-text search across documentation
- Parameters:
  - `query` (required): Search query
  - `docs` (optional): Specific documentation set name
  - `maxResults` (optional): Maximum results (default: 10)
  - `fileFilter` (optional): Filter by filename
  - `titlesOnly` (optional): Return only titles without content (default: false)
- Returns: Relevant sections with content and code examples

**`get_overview`**
- Get high-level overview of all documentation files and main sections
- **Use this to browse the menu structure and understand what's available**
- Parameters:
  - `docs` (optional): Specific documentation set name
- Returns: Complete file list with main sections

**`get_file_toc`**
- Get table of contents for a specific file (all headings/sections)
- **Use this to navigate within a file using the heading hierarchy**
- Parameters:
  - `fileName` (required): File name without .md extension
  - `docs` (optional): Specific documentation set name
- Returns: Complete heading structure with all levels

**`get_section`**
- Get specific section content by title
- Parameters:
  - `title` (required): Section title to find
  - `fileName` (optional): Filter by filename
  - `docs` (optional): Specific documentation set name
- Returns: Full section content including code blocks

**`list_files`**
- List all available documentation files
- Parameters:
  - `docs` (optional): Specific documentation set name
- Returns: Grouped list of all files

**`find_code_examples`**
- Search specifically for code examples
- Parameters:
  - `query` (required): Search term to find in code
  - `language` (optional): Filter by language (python, javascript, etc.)
  - `maxResults` (optional): Maximum results (default: 5)
  - `docs` (optional): Specific documentation set name
- Returns: Code blocks matching the query

## URL Discovery Modes

1. **Sitemap** (fastest): Parse `sitemap.xml` for complete URL list
2. **Navigation** (medium): Extract from sidebar/nav menus
3. **Crawl** (fallback): Follow links within defined scope
4. **WebDriver** (escalation): Selenium for JS-heavy or bot-protected sites

**LLM Filtering**: Applied only on large sitemaps (>1000 URLs) to select most relevant pages.

## Project Structure

```
AnyDocsMCP/
├── scraper/              # Python scraping engine
│   ├── doc_manager.py    # CLI interface
│   ├── url_discovery.py  # Multi-mode discovery
│   ├── scraper_engine.py # Content extraction
│   ├── content_cleaner.py # Post-processing
│   ├── webdriver_discovery.py # Selenium fallback
│   └── requirements.txt
├── src/                  # TypeScript MCP server
│   └── mcp-server.ts
├── package.json
└── README.md
```

## Stats

- **49 Documentation Sites** verified
- **100% Success Rate** (with WebDriver escalation)
- **Average 25 URLs** per site
- **<200ms** search response
- **4 Discovery Modes** with automatic escalation

## Troubleshooting

**403 Forbidden**: Automatic WebDriver escalation handles most cases.

**Empty Results**: Check if site requires JavaScript (WebDriver will handle).

**Slow Scraping**: Reduce `max_pages` in config for large sites.

## License

MIT License - see LICENSE file
