"""
End-to-End Pipeline Test: Scrape → Clean → Write → MCP Index → MCP Search

Tests the complete pipeline from serving HTML documentation pages through
the scraper engine to indexing and searching via the MCP MarkdownParser.

Phase A (Python): HTTP Server → ScraperEngine → .md output files
Phase B (TypeScript): MarkdownParser → buildIndex → search → verify
"""
import json
import os
import sys
import shutil
import subprocess
import threading
import tempfile
import time
import pytest
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime

# Add scraper to path
SCRAPER_DIR = Path(__file__).parent.parent.parent / "scraper"
sys.path.insert(0, str(SCRAPER_DIR))

from models import DocumentationConfig, SiteAnalysis
from storage import StorageManager
from scraper_engine import ScraperEngine

# ─── Constants ───────────────────────────────────────────────────────

FIXTURES_DIR = Path(__file__).parent / "html_fixtures"
E2E_OUTPUT_DIR = Path(__file__).parent / "scraper_output"
MCP_SERVER_DIR = Path(__file__).parent.parent.parent / "mcp-server"
PROJECT_ROOT = Path(__file__).parent.parent.parent


class SilentHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves from html_fixtures with clean URL routing."""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(FIXTURES_DIR), **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress request logging

    def do_GET(self):
        # Route clean URLs to .html files
        path = self.path.rstrip("/")
        if path and not path.endswith(".html") and not "." in path.split("/")[-1]:
            # Try adding .html
            html_path = FIXTURES_DIR / path.lstrip("/")
            if not html_path.exists() and (html_path.with_suffix(".html")).exists():
                self.path = path + ".html"
            elif (html_path / "index.html").exists():
                self.path = path + "/index.html"
        super().do_GET()


def start_http_server(port=0):
    """Start a threaded HTTP server serving the HTML fixtures."""
    server = HTTPServer(("127.0.0.1", port), SilentHandler)
    actual_port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, actual_port


# ─── Phase A: Python Scraper Tests ──────────────────────────────────

class TestPhaseA_Scraper:
    """Phase A: Serve HTML → Scrape → Verify .md output."""

    @pytest.fixture(autouse=True, scope="class")
    def setup_pipeline(self, request):
        """Start HTTP server, run scraper, store output for Phase B."""
        # Start server
        server, port = start_http_server()
        request.cls.server = server
        request.cls.port = port
        request.cls.base_url = f"http://127.0.0.1:{port}"

        # Clean output directory
        if E2E_OUTPUT_DIR.exists():
            shutil.rmtree(E2E_OUTPUT_DIR)
        E2E_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Create StorageManager pointing to our output dir
        storage = StorageManager(root_path=str(E2E_OUTPUT_DIR))

        # Create config (bypass SiteAnalyzer — we know the HTML structure)
        config = DocumentationConfig(
            name="e2e-testdocs",
            display_name="E2E Test Documentation",
            start_url=f"http://127.0.0.1:{port}/docs/",
            site_analysis=SiteAnalysis(
                content_selectors=["main"],
                navigation_selectors=["nav.sidebar"],
                title_selector="h1",
                exclude_selectors=["nav"],
                url_pattern=f"http://127.0.0.1:{port}/docs/.*",
                base_url=f"http://127.0.0.1:{port}",
                grouping_strategy="path_depth_2",
                notes="E2E test fixture site",
            ),
            version="v1",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        storage.save_config(config)
        version = storage.create_version("e2e-testdocs")

        # Run scraper
        engine = ScraperEngine(config, storage, max_workers=2)
        page_counts = engine.scrape_all(version, max_pages=20)

        request.cls.page_counts = page_counts
        request.cls.storage = storage
        request.cls.version = version
        request.cls.output_path = storage.get_docs_path("e2e-testdocs", version)

        yield

        # Teardown
        server.shutdown()

    def test_scraper_produced_output_files(self):
        """Scraper created at least 1 .md file."""
        md_files = list(self.output_path.glob("*.md"))
        assert len(md_files) >= 1, f"Expected .md files in {self.output_path}, found: {md_files}"
        print(f"\n  [OK] Scraper produced {len(md_files)} .md file(s)")
        for f in md_files:
            print(f"     - {f.name} ({f.stat().st_size:,} bytes)")

    def test_output_contains_expected_content(self):
        """Output .md files contain cleaned documentation content."""
        all_content = ""
        for md_file in self.output_path.glob("*.md"):
            all_content += md_file.read_text(encoding="utf-8")

        # Content from our HTML fixtures should be present
        assert "Getting Started" in all_content, "Missing 'Getting Started' content"
        assert "Authentication" in all_content, "Missing 'Authentication' content"
        assert "API Reference" in all_content or "API" in all_content, "Missing API content"
        print("  [OK] Output contains expected documentation content")

    def test_output_has_code_blocks(self):
        """Output preserves code blocks from HTML."""
        all_content = ""
        for md_file in self.output_path.glob("*.md"):
            all_content += md_file.read_text(encoding="utf-8")

        assert "```" in all_content, "No code blocks found in output"
        # Check for specific code patterns from our fixtures
        code_block_count = all_content.count("```")
        assert code_block_count >= 4, f"Expected ≥4 code fences, found {code_block_count}"
        print(f"  [OK] Output contains {code_block_count // 2} code blocks")

    def test_output_has_headings(self):
        """Output has proper markdown heading structure."""
        all_content = ""
        for md_file in self.output_path.glob("*.md"):
            all_content += md_file.read_text(encoding="utf-8")

        h1_count = len([l for l in all_content.split("\n") if l.startswith("# ")])
        h2_count = len([l for l in all_content.split("\n") if l.startswith("## ")])

        assert h1_count >= 1, f"Expected ≥1 h1, found {h1_count}"
        assert h2_count >= 3, f"Expected ≥3 h2, found {h2_count}"
        print(f"  [OK] Heading structure: {h1_count} h1, {h2_count} h2")

    def test_output_has_source_urls(self):
        """Output includes source URLs for traceability."""
        all_content = ""
        for md_file in self.output_path.glob("*.md"):
            all_content += md_file.read_text(encoding="utf-8")

        assert "**Source:**" in all_content, "Missing source URL annotations"
        source_count = all_content.count("**Source:**")
        print(f"  [OK] {source_count} source URL(s) preserved")

    def test_no_raw_html_in_output(self):
        """Output is clean markdown — no HTML tags leaked through."""
        for md_file in self.output_path.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            # Allow some markdown-compatible HTML, but no full tags
            assert "<nav" not in content, f"Raw <nav> HTML in {md_file.name}"
            assert "<body" not in content, f"Raw <body> HTML in {md_file.name}"
            assert "<head" not in content, f"Raw <head> HTML in {md_file.name}"
        print("  [OK] No raw HTML tags in output")

    def test_page_counts_match(self):
        """Scraper reports correct page counts."""
        total = sum(self.page_counts.values())
        assert total >= 3, f"Expected ≥3 pages scraped, got {total}"
        print(f"  [OK] Scraped {total} pages into {len(self.page_counts)} file group(s)")


# ─── Phase B: TypeScript MCP Server Tests ────────────────────────────

class TestPhaseB_MCPServer:
    """Phase B: Read scraped .md → MarkdownParser → search/index/overview."""

    @pytest.fixture(autouse=True, scope="class")
    def setup_mcp_test(self, request):
        """Ensure Phase A output exists, then run TypeScript tests."""
        # Phase A must have run first (pytest runs classes in order)
        output_path = E2E_OUTPUT_DIR / "e2e-testdocs" / "v1"
        if not output_path.exists() or not list(output_path.glob("*.md")):
            pytest.skip("Phase A output not available — run Phase A first")
        request.cls.output_path = output_path

    def test_mcp_typescript_e2e(self):
        """Run the TypeScript E2E test that indexes and searches the scraped output."""
        ts_test_file = MCP_SERVER_DIR / "src" / "__tests__" / "e2e-pipeline.test.ts"
        if not ts_test_file.exists():
            pytest.skip("TypeScript E2E test not yet created")

        # Set env var so the TS test knows where to find the scraped docs
        env = os.environ.copy()
        env["E2E_DOCS_PATH"] = str(self.output_path)

        result = subprocess.run(
            "npx vitest run e2e-pipeline --reporter=verbose",
            cwd=str(MCP_SERVER_DIR),
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
            shell=True,
        )

        print(f"\n  TypeScript stdout:\n{result.stdout}")
        if result.stderr:
            print(f"  TypeScript stderr:\n{result.stderr}")

        assert result.returncode == 0, (
            f"TypeScript E2E tests failed:\n{result.stdout}\n{result.stderr}"
        )
        print("  [OK] TypeScript MCP E2E tests passed")


# ─── Standalone runner ───────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])
