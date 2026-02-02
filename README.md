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
┌─────────────────┐
│  URL Discovery  │ → Sitemap → Navigation → Crawl → WebDriver
└────────┬────────┘
         ↓
┌─────────────────┐
│ Content Extract │ → BeautifulSoup + markdownify
└────────┬────────┘
         ↓
┌─────────────────┐
│ Content Clean   │ → Remove UI artifacts, normalize
└────────┬────────┘
         ↓
┌─────────────────┐
│ File Storage    │ → JSON metadata + Markdown files
└────────┬────────┘
         ↓
┌─────────────────┐
│ MCP Server      │ → search_docs, read_doc, list_docs
└─────────────────┘
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

| Tool | Description |
|------|-------------|
| `scrape_docs` | Scrape documentation from URL |
| `search_docs` | Full-text search with context |
| `read_doc` | Get specific document content |
| `list_docs` | List available documents |
| `switch_doc` | Change active documentation set |

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
