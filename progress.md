# AnyDocsMCP Quality & Retrieval Upgrade - Progress Log

## Plan v1: quality-retrieval-upgrade-v1 ✅ COMPLETE

### Session 1-2 — 2026-02-07
- [x] 27/27 tasks completed across 6 epics
- [x] All Python tests passing (42 tests)
- [x] All TypeScript tests passing (vitest)
- [x] Branch: `plan/quality-retrieval-upgrade-v1`

---

## Plan v2: real-world-quality-upgrade

### Session 1 — 2026-02-07

- [x] Real-world data audit: 2,103 MD files, 54 MB across 46 doc-sets
- [x] Identified critical quality issues: 622 encoding errors, 161 UI artifacts, 153 TOC remnants
- [x] Strategy document: STRATEGY-v2-real-world-quality.md
- [x] 6 functional groups defined
- [x] Deep init complete: 30 tasks across 6 groups
- [x] prd.json assembled, partials cleaned up

### Backlog Summary (30 tasks, 0 passes)

| Group | Tasks | Focus |
|-------|-------|-------|
| Capture-Replay-Infrastructure | 5 | MockServer, HTTP capture, golden snapshots, MCP corpus |
| Encoding-Quality | 5 | Audit, permalink removal, mojibake repair, charset detection |
| Artifact-Cleanup-Profiles | 5 | Pattern discovery, MkDocs/Sphinx/Docusaurus/Hugo profiles |
| Content-Sizing-Chunking | 5 | File split, stub detection, table compression, quality score |
| Search-Relevance-RealData | 5 | 100 queries, precision/MRR, large corpus perf, code search |
| E2E-Pipeline-Testing | 5 | Pipeline smoke, golden diff, MCP tools, quality dashboard, CI |

### Recommended First Task

**"ResponseCapture class for recording HTTP responses"** — foundation for all other real-world tests.

## Working on ResponseCapture class

**Files to modify/create:**
- `scraper/response_capture.py` — Main ResponseCapture class with capture(), save(), load()
- `scraper/tests/test_response_capture.py` — Unit tests for all acceptance criteria

**Approach:**
1. Create dataclass CapturedResponse with status, headers, body, url
2. URL-to-slug: replace non-alphanumeric with hyphens, collapse multiple
3. Save as pair: .meta.json (metadata) + .body.html (raw content)
4. CLI entry point for manual capture (not tested in CI)

**Verification:** pytest with mocked requests

**Potential challenges:** URL slug collision handling, large response truncation

**Result:** Success — 16/16 tests passed. ResponseCapture with capture(), save(), load(), url_to_slug(), and CLI entry point fully implemented.

## Working on Capture script for 10 reference doc-sets

**Files to modify/create:**
- `tests/fixtures/real-world/capture-manifest.json` — JSON manifest with 10 doc-sets, 3-5 URLs each
- `scraper/capture_all.py` — Runner script that iterates manifest and captures all URLs
- `scraper/tests/test_capture_all.py` — Tests for manifest validation and runner logic

**Approach:**
1. Define 10 reference doc-sets: react, fastapi, tailwind, kubernetes, django, hyperapp-github, onoffice, synthflow, golang, rust-book
2. Per doc-set: landing page, tutorial, API reference, code examples, edge case
3. capture_all.py loads manifest, calls ResponseCapture for each URL
4. Tests validate JSON schema and runner logic (not live capture in CI)

**Verification:** pytest with mocked ResponseCapture

**Potential challenges:** Manifest maintenance, URL selection representativeness

**Result:** Success — 15/15 tests passed. capture-manifest.json with 10 doc-sets, capture_all.py runner, and CLI --list flag fully implemented.
