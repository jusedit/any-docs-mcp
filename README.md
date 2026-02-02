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

## ⚠️ Security Disclaimer

**Use at your own risk.** This software scrapes and processes web content, which may contain:
- Malicious code or injection attempts
- Untrusted content that could influence AI behavior
- Potential prompt injection vulnerabilities

**Best Practices:**
- Only scrape documentation from trusted sources
- Review scraped content before use in production
- Be aware that scraped content is injected into your AI assistant's context
- Consider the security implications of automated web scraping

By using this software, you acknowledge these risks and agree to use it at your own discretion.

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
cd ../mcp-server
npm install
npm run build
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

## 🖥️ Using in Code Editors

### Windsurf (Cascade AI)

1. **Open MCP configuration:**
   - Windows: `C:\Users\User\.codeium\windsurf\mcp_config.json`

2. **Add MCP server:**

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/Path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-v1-your-key-here"
      }
    }
  }
}
```

3. **Restart Windsurf** and the MCP server will be available in your AI assistant.

## ⚙️ Configuration

### Environment Variables

Configure the MCP server behavior using environment variables in your MCP configuration:

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/Path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-v1-your-key-here",
        "ANYDOCS_ACTIVE": "python3",
        "ANYDOCS_STORAGE_ROOT": "C:/Custom/Path/docs",
        "ANYDOCS_REFRESH_DAYS": "7"
      }
    }
  }
}
```

**Available Variables:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | **Yes** | - | OpenRouter API key for LLM-powered site analysis |
| `ANYDOCS_ACTIVE` | No | `""` | Default documentation set to load on startup (e.g., `"python3"`) |
| `ANYDOCS_STORAGE_ROOT` | No | `%APPDATA%/AnyDocsMCP/docs` | Custom storage location for scraped documentation |
| `ANYDOCS_REFRESH_DAYS` | No | `30` | Number of days before documentation needs refresh |

**Notes:**
- If `ANYDOCS_ACTIVE` is not set, use `list_documentation_sets` and `switch_documentation` to select a doc set
- Storage root defaults to OS-specific application data directory
- Refresh interval prevents unnecessary re-scraping; use `force: true` in `update_documentation` to override

## ✅ Verified Documentation Sites (49/49)

Successfully tested with 100% success rate using automatic WebDriver escalation for bot-protected sites.

### Programming Languages
- **Python 3 Documentation** - https://docs.python.org/3/
- **Node.js API** - https://nodejs.org/api/
- **TypeScript Documentation** - https://www.typescriptlang.org/docs/
- **Java SE Documentation** - https://docs.oracle.com/en/java/javase/
- **Kotlin Documentation** - https://kotlinlang.org/docs/home.html
- **Rust Book** - https://doc.rust-lang.org/book/
- **Go Documentation** - https://go.dev/doc/
- **Microsoft .NET** - https://learn.microsoft.com/en-us/dotnet/

### Tools & Build Systems
- **Git Documentation** - https://git-scm.com/docs
- **Linux Man Pages** - https://man7.org/linux/man-pages/
- **Swagger/OpenAPI** - https://swagger.io/docs/
- **gRPC Documentation** - https://grpc.io/docs/
- **Webpack Docs** - https://webpack.js.org/concepts/
- **ESLint Documentation** - https://eslint.org/docs/latest/
- **Vite Guide** - https://vite.dev/guide/
- **Tailwind CSS** - https://tailwindcss.com/docs

### Web Frameworks (Frontend)
- **React Documentation** - https://react.dev/
- **Next.js Docs** - https://nextjs.org/docs
- **Vue.js Guide** - https://vuejs.org/guide/
- **Nuxt Documentation** - https://nuxt.com/docs
- **Angular Documentation** - https://angular.dev/
- **Svelte Documentation** - https://svelte.dev/docs
- **SvelteKit Documentation** - https://svelte.dev/docs/kit

### Web Frameworks (Backend)
- **Django Documentation** - https://docs.djangoproject.com/en/stable/
- **Flask Documentation** - https://flask.palletsprojects.com/en/stable/
- **FastAPI Documentation** - https://fastapi.tiangolo.com/
- **Ruby on Rails Guides** - https://guides.rubyonrails.org/
- **Laravel Documentation** - https://laravel.com/docs
- **Spring Boot Reference** - https://docs.spring.io/spring-boot/reference/index.html

### Databases
- **PostgreSQL Documentation** - https://www.postgresql.org/docs/current/
- **MySQL Documentation** - https://dev.mysql.com/doc/
- **SQLite Documentation** - https://www.sqlite.org/docs.html
- **Redis Documentation** - https://redis.io/docs/latest/
- **MongoDB Documentation** - https://www.mongodb.com/docs/
- **Elasticsearch Reference** - https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html

### Message Queues & Streaming
- **Apache Kafka** - https://kafka.apache.org/documentation/
- **RabbitMQ Documentation** - https://www.rabbitmq.com/docs

### DevOps & Infrastructure
- **Docker Documentation** - https://docs.docker.com/
- **Kubernetes Documentation** - https://kubernetes.io/docs/
- **Helm Documentation** - https://helm.sh/docs/
- **Terraform Documentation** - https://developer.hashicorp.com/terraform/docs
- **Ansible Documentation** - https://docs.ansible.com/ansible/latest/
- **Nginx Documentation** - https://nginx.org/en/docs/

### Cloud Providers & APIs
- **GitHub Documentation** - https://docs.github.com/en
- **AWS Documentation** - https://docs.aws.amazon.com/
- **Google Cloud Documentation** - https://docs.cloud.google.com/docs
- **Microsoft Azure** - https://learn.microsoft.com/en-us/azure/
- **OpenAI Platform** - https://platform.openai.com/docs/overview
- **Stripe Documentation** - https://docs.stripe.com/
- **Twilio Documentation** - https://www.twilio.com/docs

**Discovery Modes Used:**
- Sitemap: 28 sites (fastest)
- Navigation: 9 sites (medium)
- Crawl: 7 sites (fallback)
- WebDriver: 12 sites (for JS-heavy or bot-protected)

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

**`get_scrape_logs`**
- Read log output from a scraping job for debugging
- **Use this when scrapes fail or to understand what happened during scraping**
- Parameters:
  - `jobId` (required): Job ID to get logs for
  - `lines` (optional): Number of lines to return (default: 100, max: 1000)
- Returns: Timestamped log output with stdout and stderr

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
