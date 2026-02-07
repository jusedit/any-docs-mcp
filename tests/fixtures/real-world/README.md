# Real-World Test Fixtures

This directory contains real-world documentation fixtures for testing the AnyDocsMCP scraper and MCP server against actual documentation sites.

## Structure

```
real-world/
├── {doc-name}/
│   ├── golden/          # Golden snapshot .md files (baseline quality)
│   ├── mcp-corpus/      # Subset for MCP tool testing
│   └── captured/        # HTTP response fixtures (.meta.json + .body.html)
├── capture-manifest.json    # 10 reference doc-sets with URLs
├── quality_baseline.json    # Per-file quality metrics
└── query-suite.json         # 100 curated search queries
```

## Doc-Sets

1. **react** (Docusaurus) - React documentation
2. **fastapi** (MkDocs) - FastAPI framework docs
3. **tailwind** (custom) - Tailwind CSS docs
4. **kubernetes** (Hugo) - Kubernetes documentation
5. **django** (Sphinx) - Django framework docs
6. **hyperapp-github** (GitHub) - Hyperapp GitHub repo
7. **onoffice** (custom) - onOffice API docs
8. **synthflow** (custom) - Synthflow AI docs
9. **golang** (custom) - Go programming language docs
10. **rust-book** (mdBook) - Rust programming book

## Refreshing Fixtures

To regenerate the quality baseline:
```bash
python scraper/generate_baseline.py
```

To capture new HTTP responses:
```bash
python -m capture_all --manifest tests/fixtures/real-world/capture-manifest.json
```

## Size Limits

- Golden files: < 5 MB total
- MCP corpus: < 10 MB total
- Captured responses: < 1 MB each
