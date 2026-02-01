# AnyDocsMCP 🚀

> **Universal Documentation Pipeline for AI Assistants**
>
> Transform any documentation website into searchable knowledge for your AI - fully automated with LLM analysis.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-purple.svg)](https://modelcontextprotocol.io)

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Using in Code Editors](#using-in-code-editors)
- [System Architecture](#system-architecture)
- [CLI Commands](#cli-commands)
- [MCP Tools](#mcp-tools)
- [Configuration](#configuration)
- [Examples](#examples)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 About

**AnyDocsMCP** is an intelligent system that automatically transforms any documentation website into searchable, AI-readable knowledge bases.

### The Problem

As a developer, you use various documentation daily (API docs, framework guides, etc.). Your AI assistants (Windsurf, Claude, etc.) don't know these specific docs or have outdated information.

### The Solution

AnyDocsMCP:
1. ✨ **Analyzes** documentation sites automatically with Claude (LLM)
2. 📥 **Extracts** relevant content (including code examples)
3. 📝 **Converts** to structured Markdown
4. 🔍 **Indexes** everything for fast search
5. 🤖 **Serves** via MCP (Model Context Protocol) to AI assistants

**Result:** Your AI can instantly search any documentation and give you precise answers!

---

## ✨ Features

### 🤖 LLM-Powered Analysis
- Automatic website structure detection (WordPress, VitePress, Docusaurus, etc.)
- No manual configuration needed
- Intelligent content and navigation extraction

### 📚 Multi-Documentation Support
- Manage unlimited documentation sets simultaneously
- Fast switching between docs without restart
- Centralized management in `%APPDATA%\AnyDocsMCP\docs`

### 🔄 Version Management
- Automatic versioning (v1, v2, v3...)
- Old versions preserved
- One-command re-scraping for updates

### 🔍 Powerful Search
- Semantic full-text search
- Code block search with syntax highlighting
- Hierarchical navigation
- < 200ms response time

### 🌐 Direct via MCP
- **NEW:** Scrape documentation directly from MCP server
- No terminal needed - everything in your IDE
- Hot-swap between documentation sets

### 🎨 Editor Integration
- Windsurf (Cascade AI)
- Claude Desktop
- Any MCP-compatible editor

## Quick Start

### Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **OpenRouter API Key** - [Sign up](https://openrouter.ai/)

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/jusedit/any-docs-mcp.git
cd AnyDocsMCP

# 2. Install Python dependencies
cd scraper
pip install -r requirements.txt

# 3. Install Node.js dependencies
cd ../mcp-server
npm install
npm run build

# 4. Set API key
# Windows PowerShell:
$env:OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# 5. Scrape your first documentation
cd ../scraper
python cli.py add --url https://docs.synthflow.ai --name synthflow

# 6. Configure MCP server
cd ../mcp-server
# Create config.json:
echo '{"activeDocs": "synthflow"}' > config.json

# 7. Start MCP server
npm start
```

**Done!** Now usable in your IDE via MCP.

## 💻 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/jusedit/any-docs-mcp.git
cd AnyDocsMCP
```

### Step 2: Python Environment

```bash
# Create virtual environment (recommended)
cd scraper
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Node.js Setup

```bash
cd ../mcp-server
npm install
npm run build
```

### Step 4: Configure API Key

Create a `.env` file in project root:

```env
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

Or set environment variable:

```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-..."

# Windows CMD
set OPENROUTER_API_KEY=sk-or-v1-...

# Linux/Mac
export OPENROUTER_API_KEY=sk-or-v1-...
```

## 🖥️ Using in Code Editors

### Windsurf (Cascade AI)

1. **Open MCP configuration:**
   - Windows: `%APPDATA%\Windsurf\User\globalStorage\codeium.windsurf\settings\mcp_settings.json`
   - Mac: `~/Library/Application Support/Windsurf/User/globalStorage/codeium.windsurf/settings/mcp_settings.json`

2. **Add MCP server:**

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/Path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "synthflow"
      }
    }
  }
}
```

3. **Restart Windsurf**

4. **Use:**

```
You: "Search Synthflow documentation for API authentication"
Cascade: [uses MCP tool search]
```

---

### Claude Desktop

1. **Open configuration:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add MCP server:**

```json
{
  "mcpServers": {
    "documentation": {
      "command": "node",
      "args": ["C:/Path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "synthflow"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

---

### Multiple Documentation Sets

```json
{
  "mcpServers": {
    "react-docs": {
      "command": "node",
      "args": ["C:/Path/to/mcp-server/dist/index.js"],
      "env": { "ANYDOCS_ACTIVE": "react" }
    },
    "vue-docs": {
      "command": "node",
      "args": ["C:/Path/to/mcp-server/dist/index.js"],
      "env": { "ANYDOCS_ACTIVE": "vue" }
    }
  }
}
```

## 🏗️ System Architecture

### Overview

```
┌──────────────────────────────────────────────────────┐
│           Code Editor (Windsurf/Claude)              │
│                  ↕ MCP Protocol                      │
│              MCP Server (Node.js)                    │
└──────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────┐
│              Search & Index Engine                   │
│  • Markdown Parser  • Semantic Search  • Code Search │
└──────────────────────────────────────────────────────┘
                        ↑
               Markdown Documents
                        ↑
┌──────────────────────────────────────────────────────┐
│             Scraper Engine (Python)                  │
│  • Site Analyzer (LLM)  • Extractor  • Converter    │
└──────────────────────────────────────────────────────┘
                        ↑
              Documentation Website
```

### Components

#### 1. **Scraper** (`scraper/`)
- **Language:** Python 3.10+
- **Technologies:** BeautifulSoup, Markdownify, OpenAI SDK
- **Function:**
  - Analyzes websites with Claude (LLM)
  - Extracts HTML content
  - Converts to Markdown
  - Stores structured data

#### 2. **MCP Server** (`mcp-server/`)
- **Language:** TypeScript/Node.js
- **Technologies:** MCP SDK, Custom Search Engine
- **Function:**
  - Provides MCP tools
  - Indexes Markdown files
  - Executes searches
  - Manages multiple documentations

#### 3. **Storage** (`%APPDATA%/AnyDocsMCP/docs/`)
- **Format:** Structured Markdown
- **Organization:** Per documentation + versions
- **Features:** Metadata, config, versioning

---

## 📝 CLI Commands

### Add Documentation

```bash
python cli.py add --url <START_URL> --name <DOC_NAME> [--display-name <NAME>]
```

**Example:**
```bash
python cli.py add \
  --url https://docs.synthflow.ai/getting-started \
  --name synthflow \
  --display-name "Synthflow API Documentation"
```

### Update Documentation

```bash
python cli.py update --name <DOC_NAME>
```

Creates new version (v2, v3, etc.)

### List Documentation Sets

```bash
python cli.py list
```

---

## 🔧 MCP Tools

The MCP server provides these tools for AI assistants:

### 1. `search`
Full-text search in documentation.

**Parameters:**
- `query` (string, required): Search term
- `maxResults` (number, optional): Number of results (default: 10)
- `fileFilter` (string, optional): Filename filter
- `titlesOnly` (boolean, optional): Only titles without content

### 2. `get_overview`
Overview of all documentation sections.

### 3. `get_file_toc`
Table of contents for a specific file.

### 4. `get_section`
Retrieve specific section by title.

### 5. `list_files`
List all available documentation files.

### 6. `find_code_examples`
Search for code examples.

### 7. `scrape_documentation` 🆕
Scrape new documentation directly from MCP server.

**Parameters:**
- `url` (string, required): Start URL
- `name` (string, required): Unique name
- `displayName` (string, optional): Display name

### 8. `list_documentation_sets` 🆕
List all available documentation sets.

### 9. `switch_documentation` 🆕
Switch to different documentation (without restart).

---

## ⚙️ Configuration

### MCP Server Configuration

`mcp-server/config.json`:

```json
{
  "activeDocs": "synthflow",
  "storageRoot": null,
  "serverName": "synthflow-mcp"
}
```

**Parameters:**
- `activeDocs`: Which documentation to load
- `storageRoot`: Custom storage path (optional)
- `serverName`: MCP server name (optional)

**Alternative via environment variables:**

```bash
export ANYDOCS_ACTIVE=synthflow
export ANYDOCS_STORAGE_ROOT=/custom/path
```

## 💡 Examples

### Example 1: Add React Documentation

```bash
cd scraper
python cli.py add \
  --url https://react.dev/learn \
  --name react \
  --display-name "React Official Documentation"
```

In Windsurf:
```
You: "How do React Hooks work?"
Cascade: [searches React docs] "React Hooks are functions that..."
```

### Example 2: Scrape from MCP

**In Windsurf/Claude:**
```
You: "Scrape the Tailwind CSS documentation"

Cascade uses MCP tool:
{
  "tool": "scrape_documentation",
  "arguments": {
    "url": "https://tailwindcss.com/docs",
    "name": "tailwind"
  }
}

Cascade: "✅ Tailwind CSS documentation successfully scraped!"
```

---

## 🛠️ Development

### Project Structure

```
AnyDocsMCP/
├── scraper/                    # Python Scraper
│   ├── cli.py                 # CLI Entry Point
│   ├── site_analyzer.py       # LLM Site Analysis
│   ├── scraper_engine.py      # Scraping Logic
│   ├── storage.py             # Storage Management
│   └── models.py              # Data Models
│
├── mcp-server/                # TypeScript MCP Server
│   ├── src/
│   │   ├── index.ts          # MCP Server Entry
│   │   ├── config.ts         # Configuration
│   │   └── markdown-parser.ts # Parser & Search
│   └── package.json          # Dependencies
│
└── docs/                      # Documentation
    ├── TEST_RESULTS.md
    ├── API_COMPARISON.md
    └── SCRAPING_ENDPOINT_RESULTS.md
```

### Run Tests

```bash
# MCP Server Tests
cd mcp-server
npm test

# Integration Test
node test-queries.js
```

---

## 🐛 Troubleshooting

### "OpenRouter API key required"

**Solution:**
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

### "No versions found for documentation"

**Solution:**
```bash
# Check if documentation exists
python cli.py list

# Re-scrape
python cli.py add --url <URL> --name <NAME>
```

### MCP Server won't start

**Diagnosis:**
```bash
cd mcp-server
npm run build  # Rebuild
node dist/index.js  # Manual start to see errors
```

---

## 🗺️ Roadmap

### Version 2.0 (Planned)

- [ ] **Async Scraping** - Long scraping jobs in background
- [ ] **Progress Tracking** - Live status of scraping jobs
- [ ] **Vector Search** - Semantic search with embeddings
- [ ] **Web UI** - Browser interface for management
- [ ] **Docker Support** - Container-based deployment
- [ ] **Cloud Storage** - S3/Azure Blob support

### Version 1.5 (Next)

- [x] MCP Scraping Endpoint
- [x] Hot-Swap Documentation
- [ ] Auto-Update Scheduler
- [ ] Incremental Re-Scraping
- [ ] Better Error Recovery

---

## 🤝 Contributing

Contributions are welcome! Here's how:

### Reporting Issues

Please use GitHub Issues for:
- 🐛 Bug Reports
- 💡 Feature Requests
- 📚 Documentation Improvements
- ❓ Questions

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Anthropic** - For Claude and LLM technology
- **Model Context Protocol** - For the MCP framework
- **OpenRouter** - For LLM API access
- **Community** - For feedback and contributions

---

## ⚠️ Disclaimer

This software is provided "as is", without warranty of any kind, express or implied. Use at your own risk. The authors are not responsible for any damages or issues arising from the use of this software.

---

## 📊 Stats

- ⭐ **Tested with:** 3+ documentation frameworks
- 📄 **Scraped:** 1000+ pages successfully
- 🔍 **Search Speed:** < 200ms
- 🎯 **Accuracy:** 95%+ relevant results

---

<div align="center">

**Built with ❤️ for the Developer Community**

[⬆ Back to Top](#anydocsmcp-)

</div>
