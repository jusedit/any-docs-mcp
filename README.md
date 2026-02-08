# AnyDocsMCP

> Scrape any documentation site and inject it into your AI coding agent's context.

Works with **Windsurf**, **Cursor**, **Claude Code**, and **Antigravity (Jules/Gemini)**.

[Landing Page](https://jusedit.github.io/any-docs-mcp) | [MCP Server Docs](mcp-server/README.md) | [Scraper Docs](scraper/README.md)

## Why This Works

Inspired by [`@gaojude/next-agents-md`](https://github.com/gaojude/next-agents-md) and Vercel's research on [retrieval-led reasoning](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals):

> A compressed 8KB docs index embedded directly in `AGENTS.md` achieved a **100% pass rate**, while skills maxed out at 79%. Passive context beats active retrieval because there is no decision point -- the agent doesn't need to decide "should I look this up?" The information is already there.

AnyDocsMCP applies this pattern to **any** documentation site, not just Next.js. The scraper produces a compact pipe-delimited index that fits in ~500 bytes, pointing the agent to individual doc files it can read on-demand. This shifts agents from pre-training-led reasoning to retrieval-led reasoning.

## How It Works

```
  You                          AnyDocs MCP                    Your Project
   │                               │                              │
   │  "scrape react docs"          │                              │
   ├──────────────────────────────>│                              │
   │  CLI command to run           │                              │
   │<──────────────────────────────┤                              │
   │                               │                              │
   │  (run scrape command)         │                              │
   ├──────────────────────────────>│  stored in AppData           │
   │                               ├─────────────────>            │
   │  "add react-docs to project"  │                              │
   ├──────────────────────────────>│  copy docs + inject index    │
   │                               ├─────────────────────────────>│
   │                               │                              │
   │  AI agent now has persistent  │  .windsurf/rules/            │
   │  access to react docs         │  .windsurf/docs/react-docs/  │
```

1. **Scrape** -- The MCP server returns a CLI command. You run it to scrape a documentation site.
2. **Store** -- Scraped docs are stored globally in `%APPDATA%/AnyDocsMCP/v2/` (shared across projects).
3. **Inject** -- Docs are copied into your project and a compact index (~500 bytes) is added as an always-on IDE rule.
4. **Use** -- The AI agent sees the index in every conversation and reads individual doc files on-demand.

## Quick Start

### Prerequisites

- Python 3.10+ (for scraper)
- Node.js 18+ (for MCP server)
- [OpenRouter API Key](https://openrouter.ai/) (for LLM-powered scraping)
- Chrome/Chromium (optional, for SPA sites)

### Installation

```bash
git clone https://github.com/jusedit/any-docs-mcp.git
cd any-docs-mcp

# Scraper
cd scraper && pip install -r requirements.txt

# MCP Server
cd ../mcp-server && npm install && npm run build
```

### Configure Your IDE

Add to your IDE's MCP configuration:

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["/path/to/any-docs-mcp/mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-...",
        "ANYDOCS_IDE": "windsurf"
      }
    }
  }
}
```

Set `ANYDOCS_IDE` to your IDE: `windsurf` (default), `cursor`, `claude`, or `antigravity`.

See [MCP Server README](mcp-server/README.md) for full IDE configuration examples.

### Usage

Once configured, the AI agent has 6 tools available:

| Tool | Description |
|------|-------------|
| `scrape_docs` | Returns CLI command to scrape a documentation site |
| `list_docs` | Lists all doc sets in global storage |
| `remove_docs` | Deletes a doc set from global storage |
| `add_docs_to_project` | Copies docs into project + injects index as IDE rule |
| `remove_docs_from_project` | Removes docs + rule from project |
| `list_project_docs` | Lists docs currently added to this project |

## IDE Support

| IDE | Docs Path | Rules Path | Format |
|-----|-----------|------------|--------|
| **Windsurf** | `.windsurf/docs/<name>/` | `.windsurf/rules/docs-<name>.md` | `trigger: always_on` |
| **Cursor** | `.cursor/docs/<name>/` | `.cursor/rules/docs-<name>.mdc` | `alwaysApply: true` |
| **Claude Code** | `.docs/<name>/` | `CLAUDE.md` | `<!-- ANYDOCS -->` markers |
| **Antigravity** | `.agent/docs/<name>/` | `.agent/rules/docs-<name>.md` | Always On |

## Scraper Pipeline

The scraper uses a 7-step LLM-assisted pipeline:

1. **Engine Selection** -- cURL vs Selenium (auto-detects SPAs via link-count heuristic)
2. **URL Discovery** -- Sitemap + BFS quick-sample (uses Selenium for SPAs)
3. **LLM Analysis** -- Scope rules + CSS selectors with retry loop
4. **Sample Crawl** -- 5 pages for selector refinement
5. **LLM Refinement** -- Improve prune selectors from actual output
6. **Full Crawl** -- All pages with quality check + cross-page dedup
7. **Index Generation** -- Compact AGENTS.md (~500 bytes, no LLM)

## Project Structure

```
any-docs-mcp/
  scraper/                 # Python scraping engine
    cli.py                 # CLI entry point
    pipeline.py            # 7-step orchestrator
    engine_selector.py     # cURL vs Selenium decision
    discovery.py           # URL discovery (sitemap + BFS)
    llm_analyzer.py        # LLM-powered scope + selector analysis
    crawler.py             # Parallel page fetcher + HTML-to-MD
    content_cleaner.py     # UI artifact removal
    dedup.py               # Cross-page deduplication
    grouper.py             # AGENTS.md index generator
    tests/                 # Unit tests (53 tests)
    requirements.txt
  mcp-server/              # TypeScript MCP server
    src/
      index.ts             # MCP tools + handlers
      storage.ts           # AppData docs management
      ide-adapter.ts       # IDE-specific adapters
    package.json
  docs/                    # GitHub Pages landing page
  .env.example             # Environment variable template
  LICENSE                  # MIT
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | Yes* | -- | API key for LLM-powered scraping |
| `ANYDOCS_IDE` | No | `windsurf` | Target IDE |
| `ANYDOCS_STORAGE_ROOT` | No | `%APPDATA%/AnyDocsMCP/v2/` | Override storage path |
| `ANYDOCS_SCRAPER_PATH` | No | auto-detected | Override scraper path |

## Security

**Use at your own risk.** Scraped content is injected into your AI agent's context. Only scrape documentation from trusted sources. Review content before use in production.

## License

MIT -- see [LICENSE](LICENSE)
