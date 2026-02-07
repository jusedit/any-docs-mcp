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

### Backlog Summary (30 tasks, 1 passes)

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

## Working on FixtureHTTPServer mock server

**Files to modify/create:**
- `scraper/tests/fixture_server.py` — FixtureHTTPServer class with ThreadingHTTPServer
- `scraper/tests/conftest.py` — pytest fixture for mock_http_server
- `scraper/tests/test_fixture_server.py` — Tests for server functionality

**Approach:**
1. ThreadingHTTPServer subclass that serves captured fixtures
2. URL pattern matching: /{doc-name}/{path} → lookup fixture
3. Returns stored status, headers, body from .meta.json + .body.html
4. Pytest fixture handles start/stop lifecycle
5. get_rewritten_url() converts original URLs to localhost URLs

**Verification:** pytest with real server on random port

**Potential challenges:** Concurrent request handling, port allocation, fixture path resolution

**Result:** Success — 14/14 tests passed. FixtureHTTPServer with ThreadingHTTPServer, pytest fixture, and URL rewriting fully implemented.

## Working on Golden markdown output snapshots

**Files to modify/create:**
- `tests/fixtures/real-world/{doc-name}/golden/*.md` — 1-2 representative .md files per doc-set
- `tests/fixtures/real-world/quality_baseline.json` — Per-file metrics baseline
- `scraper/generate_baseline.py` — Script to scan golden files and regenerate baseline
- `scraper/tests/test_golden_fixtures.py` — Tests validating golden files exist and meet criteria

**Approach:**
1. Copy content-rich .md files from %APPDATA%/AnyDocsMCP/docs/{doc}/v*/ to golden/
2. Skip stub files (<500 chars), pick files with code examples and headings
3. quality_baseline.json records: encoding_errors, artifacts, headings, code_blocks, char_count
4. generate_baseline.py regenerates metrics on demand

**Verification:** pytest checking file existence and baseline validity

**Potential challenges:** File selection criteria, path resolution from %APPDATA%

**Result:** Success — 12/12 tests passed. Golden fixtures created for 3 doc-sets (react, fastapi, tailwind), quality_baseline.json with metrics, generate_baseline.py script fully implemented.

## Working on Encoding audit script

**Files to modify/create:**
- `scraper/encoding_audit.py` — Script to scan markdown and categorize encoding defects
- `scraper/tests/test_encoding_audit.py` — Tests for audit functionality

**Approach:**
1. Scan directory of .md files for encoding defects
2. Categories: mojibake (â€™, â€œ), broken-latin (Â + non-ASCII), permalink-anchors (¶), html-entities
3. Report includes: file_path, line_number, context (±20 chars), pattern matched
4. Summary: total_files, affected_files, defects_by_category
5. CLI: python -m encoding_audit <directory> [--output report.json]

**Verification:** pytest with crafted fixtures containing each defect type

**Potential challenges:** Pattern accuracy, avoiding false positives

**Result:** Success — 16/16 tests passed. EncodingAuditor with mojibake, broken_latin, permalink_anchors, html_entities detection, and CLI fully implemented.

## Working on Cycles 6+7: Permalink removal + Pattern discovery

**Files modified/created:**
- `scraper/content_cleaner.py` — Added `remove_permalink_anchors()` method
- `scraper/pattern_discovery.py` — Pattern discovery script
- `scraper/tests/test_cycles_6_7.py` — Combined tests for both cycles

**Cycle 6 (Permalink removal):**
- Removes trailing ¶ from headings
- Removes [¶](#anchor) permalink links
- Removes []( #anchor) empty anchor links
- Preserves inline code in headings

**Cycle 7 (Pattern discovery):**
- Scans directory for recurring patterns >30% threshold
- Identifies boilerplate vs content
- Returns PatternCandidate with regex suggestions
- CLI for interactive discovery

**Result:** Success — 9/9 tests passed. Both cycles complete.
