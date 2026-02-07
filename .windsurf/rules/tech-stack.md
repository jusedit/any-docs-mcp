---
trigger: always_on
---

<tech_stack>
## Scraper (Python)
- **Language:** Python 3.10+
- **HTTP:** requests
- **HTML Parsing:** beautifulsoup4
- **HTML→MD:** markdownify
- **Models:** pydantic 2.x
- **CLI:** click
- **LLM:** openai SDK → OpenRouter (Claude 3.5 Sonnet / Haiku)
- **WebDriver:** selenium + webdriver-manager (optional)
- **Test Framework:** pytest (to be added)

## MCP Server (TypeScript / Node.js)
- **Language:** TypeScript 5.3+
- **Runtime:** Node.js 18+
- **MCP SDK:** @modelcontextprotocol/sdk ^1.0.0
- **Module:** ESM (`"type": "module"`)
- **Build:** tsc → dist/
- **Test Framework:** vitest (to be added)

## Storage
- **Format:** Markdown files grouped by URL path
- **Location:** %APPDATA%/AnyDocsMCP/docs (Windows) or ~/.local/share/AnyDocsMCP/docs
- **Versioning:** v1, v2, … directories per doc set
- **Config:** config.json + metadata.json per doc set
</tech_stack>

<coding_conventions>
## Code Style
- Python: PEP 8, type hints on public APIs
- TypeScript: strict mode, no `any` unless unavoidable
- No unnecessary comments — self-documenting code

## Testing Standards
- Tests live in `scraper/tests/` (Python) and `mcp-server/src/__tests__/` (TS)
- Golden-file fixtures in `tests/fixtures/`
- All tasks must have tests before marking passes:true
- No live network calls in unit tests — use fixtures

## Git Workflow
- Commit format: `type: description` (feat, fix, test, refactor, chore)
- Each task = 1 PR-sized commit
- All commits must pass tests

## Verification Commands
```bash
# Python tests
cd scraper && python -m pytest tests/ -v

# TypeScript tests
cd mcp-server && npx vitest run

# Build
cd mcp-server && npm run build
```
</coding_conventions>
