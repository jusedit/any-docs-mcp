# Scraper — LLM-Powered Documentation Scraper

A pipeline that scrapes documentation sites and produces:
- **1:1 Markdown files** (one per URL)
- **Grouped/merged Markdown files** (thematic)
- **AGENTS.md** — a compressed index for AI agents (retrieval-led reasoning)
- **manifest.json** — full metadata (URLs, hashes, headings)

## Architecture

```
Start URL → Engine Selector → Discovery Worker → LLM Analyzer
         → Crawler & Transform → LLM Grouper → AGENTS.md + Package
```

### Modules

| Module | PRD Ref | Purpose |
|--------|---------|---------|
| `engine_selector.py` | FR1 | cURL vs Selenium decision via content-diff heuristic |
| `discovery.py` | FR2 | robots.txt, sitemap, quick-sample BFS, canonicalize |
| `llm_analyzer.py` | FR3 | LLM-generated URL filters + CSS selectors (OpenRouter) |
| `crawler.py` | FR4 | Frontier queue, fetch, extract, clean, HTML→MD, 1:1 write |
| `grouper.py` | FR5 | LLM grouping plan + AGENTS.md generation |
| `pipeline.py` | — | Orchestrator tying FR1–FR5 together |
| `cli.py` | — | Click-based CLI entry point |
| `content_cleaner.py` | — | Markdown post-processing (artifacts, encoding, dedup) |
| `models.py` | — | Pydantic data models |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (optional — falls back to heuristics without it)
export OPENROUTER_API_KEY=sk-or-v1-...

# Scrape a documentation site
python cli.py scrape --url https://docs.example.com --name example-docs

# Test engine selection only
python cli.py test-engine --url https://docs.example.com

# Test URL discovery only
python cli.py test-discovery --url https://docs.example.com
```

## Output Structure

```
output/<name>/
├── AGENTS.md              # Compressed index for AI agents
├── manifest.json          # Full metadata (URLs, hashes, headings)
├── engine-decision.json   # Engine selection report
├── llm-analysis.json      # LLM analyzer output (scope + selectors)
├── group-plan.json        # Grouping plan
├── md/
│   ├── raw/               # 1:1 URL → Markdown files
│   │   ├── docs/
│   │   │   ├── intro.md
│   │   │   └── api/
│   │   │       └── v1.md
│   │   └── ...
│   └── grouped/           # Merged thematic files
│       ├── getting-started.md
│       ├── api-reference.md
│       └── ...
```

## Configuration

| CLI Option | Default | Description |
|------------|---------|-------------|
| `--url` | required | Start URL of documentation |
| `--name` | required | Unique name for doc set |
| `--output` | `./output/<name>` | Output directory |
| `--max-pages` | 500 | Max pages to crawl |
| `--workers` | 10 | Concurrent workers (cURL mode) |
| `--threshold` | 0.3 | Engine diff threshold |
| `--analyzer-model` | `qwen/qwen3-coder-next` | LLM for analysis |
| `--grouper-model` | `qwen/qwen3-coder-next` | LLM for grouping |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | No* | OpenRouter API key for LLM features |

*Without API key, LLM features fall back to heuristic-based analysis.

## Tests

```bash
cd scraper
python -m pytest tests/ -v
```

## Design Principles

1. **Determinism** — Same input → same output (hashes in manifest)
2. **No site-specific hacks** — All logic is generic heuristics
3. **Retrieval > Pre-training** — AGENTS.md enforces retrieval-led reasoning
4. **Graceful degradation** — Works without LLM (heuristic fallbacks)
5. **Security** — Content treated as untrusted, no script execution
