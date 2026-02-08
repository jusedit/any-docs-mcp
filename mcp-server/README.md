# AnyDocs MCP Server v2

An MCP server that scrapes documentation sites and injects them into AI coding agent contexts (Windsurf, Cursor, Claude Code, Antigravity).

## How It Works

1. **Scrape** — The server returns a CLI command to scrape a documentation site via the scraper
2. **Store** — Scraped docs are stored globally in `%APPDATA%/AnyDocsMCP/v2/` (shared across projects)
3. **Inject** — Docs are copied into your project and a compact index is added as an always-on IDE rule
4. **Use** — The AI agent reads individual doc files on-demand with minimal context window usage

## Setup

### 1. Build

```bash
cd mcp-server
npm install
npm run build
```

### 2. Configure in your IDE

#### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-...",
        "ANYDOCS_IDE": "windsurf"
      }
    }
  }
}
```

#### Cursor

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-...",
        "ANYDOCS_IDE": "cursor"
      }
    }
  }
}
```

#### Claude Code

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-...",
        "ANYDOCS_IDE": "claude"
      }
    }
  }
}
```

#### Antigravity (Jules / Gemini)

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/path/to/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-...",
        "ANYDOCS_IDE": "antigravity"
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANYDOCS_IDE` | No | `windsurf` | Target IDE: `windsurf`, `cursor`, `claude`, `antigravity` |
| `OPENROUTER_API_KEY` | Yes* | — | API key for LLM-powered scraping (*required for scraping) |
| `ANYDOCS_STORAGE_ROOT` | No | `%APPDATA%/AnyDocsMCP/v2/` | Override global docs storage path |
| `ANYDOCS_SCRAPER_PATH` | No | `../scraper` (relative to repo) | Override path to scraper |

## MCP Tools

### `scrape_docs`
Returns a CLI command to scrape a documentation site. Run the command in your terminal.

```
scrape_docs(url: "https://docs.example.com", name: "example-docs", max_pages: 500)
```

### `list_docs`
Lists all documentation sets in the global storage.

### `remove_docs`
Permanently deletes a doc set from global storage.

```
remove_docs(name: "example-docs")
```

### `add_docs_to_project`
Copies docs into the project and creates an always-on IDE rule with the documentation index.

```
add_docs_to_project(name: "example-docs", project_root: "/path/to/project")
```

### `remove_docs_from_project`
Removes docs and the IDE rule from the project.

```
remove_docs_from_project(name: "example-docs", project_root: "/path/to/project")
```

### `list_project_docs`
Lists documentation sets currently added to a project.

```
list_project_docs(project_root: "/path/to/project")
```

## IDE Integration Details

### Windsurf
- Docs are copied to `.windsurf/docs/<name>/`
- Index rule is created at `.windsurf/rules/docs-<name>.md` with `trigger: always_on`
- The rule contains a compact pipe-separated index (~500-1000 bytes)

### Cursor
- Docs are copied to `.cursor/docs/<name>/`
- Index rule is created at `.cursor/rules/docs-<name>.mdc` with `alwaysApply: true`

### Claude Code
- Docs are copied to `.docs/<name>/`
- Index is injected into `CLAUDE.md` between `<!-- ANYDOCS-START:name -->` markers

### Antigravity (Jules / Gemini)
- Docs are copied to `.agent/docs/<name>/`
- Index rule is created at `.agent/rules/docs-<name>.md`
- Set rule activation to **"Always On"** in Antigravity's Customizations panel
- Rules are plain markdown (max 12,000 chars per file)

## Storage Layout

```
%APPDATA%/AnyDocsMCP/v2/
  react-docs/
    AGENTS.md          ← compact index (~500 bytes)
    manifest.json      ← metadata (URLs, page count, etc.)
    md/raw/            ← individual markdown files (1:1 URL mapping)
      docs/
        getting-started.md
        api-reference.md
        ...
  tailwind-docs/
    ...
```

## Architecture

```
┌─────────────────────────────────────────────┐
│  AI Coding Agent (Windsurf/Cursor/Claude/    │
│                    Antigravity)               │
│                                             │
│  reads .windsurf/rules/docs-react.md        │
│  → sees compact index (500 bytes)           │
│  → reads individual files on-demand         │
└──────────────┬──────────────────────────────┘
               │ MCP Protocol
┌──────────────▼──────────────────────────────┐
│  AnyDocs MCP Server v2                      │
│                                             │
│  scrape_docs → returns CLI command          │
│  add_docs_to_project → copies + injects     │
│  remove_docs_from_project → cleans up       │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│  Global Storage (%APPDATA%/AnyDocsMCP/v2/)  │
│                                             │
│  react-docs/md/raw/...                      │
│  tailwind-docs/md/raw/...                   │
└─────────────────────────────────────────────┘
```
