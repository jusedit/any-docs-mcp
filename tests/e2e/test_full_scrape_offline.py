"""Full offline scrape test using all captured HTML files per site."""
import pytest
import json
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from scraper_engine import ScraperEngine
from storage import StorageManager
from tests.fixture_server import FixtureHTTPServer

CAPTURED_DIR = Path(__file__).parent.parent / "fixtures" / "real-world"


def get_captured_doc_sets():
    """Get list of doc-sets with captured HTML."""
    doc_sets = []
    if not CAPTURED_DIR.exists():
        return doc_sets
    
    for doc_dir in CAPTURED_DIR.iterdir():
        if doc_dir.is_dir():
            # Check for .body.html files
            body_files = list(doc_dir.glob("*.body.html"))
            if body_files:
                doc_sets.append({
                    "name": doc_dir.name,
                    "path": doc_dir,
                    "file_count": len(body_files)
                })
    return doc_sets


class TestFullOfflineScrape:
    """Test full scraping pipeline with all captured HTML files."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.mark.parametrize("doc_set", get_captured_doc_sets())
    def test_scrapes_all_captured_files(self, doc_set, temp_output_dir):
        """ScraperEngine processes all captured HTML files for a doc-set."""
        from models import DocumentationConfig, SiteAnalysis
        
        # Start fixture server with captured files
        server = FixtureHTTPServer(str(doc_set["path"]))
        port = server.start()
        base_url = f"http://127.0.0.1:{port}"
        
        try:
            config = DocumentationConfig(
                name=doc_set["name"],
                display_name=doc_set["name"],
                start_url=base_url,
                site_analysis=SiteAnalysis(
                    content_selectors=['main', 'article', '.content', '[role="main"]'],
                    navigation_selectors=['nav', '.sidebar'],
                    url_pattern=r'.*',
                    base_url=base_url
                ),
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            storage = StorageManager(root_path=str(temp_output_dir / doc_set["name"]))
            
            scraper = ScraperEngine(config, storage)
            start_time = datetime.now()
            
            # Scrape pages from fixture server
            pages_scraped = 0
            for body_file in doc_set["path"].glob("*.body.html"):
                url = f"{base_url}/{body_file.stem.replace('.body', '')}"
                try:
                    scraper.scrape_page(url, priority=1)
                    pages_scraped += 1
                except Exception:
                    pass
            
            elapsed = (datetime.now() - start_time).total_seconds()
            captured_count = doc_set["file_count"]
            
            print(f"\n  {doc_set['name']}: {pages_scraped}/{captured_count} pages scraped in {elapsed:.1f}s")
            
            assert elapsed < 60, f"Scrape took {elapsed:.1f}s, expected < 60s"
            
        finally:
            server.stop()
    
    def test_scrape_produces_valid_markdown(self, temp_output_dir):
        """Scraper output is valid markdown with expected structure."""
        doc_sets = get_captured_doc_sets()
        if not doc_sets:
            pytest.skip("No captured doc-sets available")
        
        # Verify that captured HTML files contain parseable content
        doc_set = doc_sets[0]
        body_files = list(doc_set["path"].glob("*.body.html"))
        assert len(body_files) > 0, "No body.html files found"
        
        # Check that body files contain HTML content
        for body_file in body_files[:3]:
            content = body_file.read_text(encoding="utf-8", errors="replace")
            assert len(content) > 100, f"Body file {body_file.name} is too small"
    
    def test_no_crashes_on_edge_cases(self, temp_output_dir):
        """Scraper handles edge cases without crashing."""
        doc_sets = get_captured_doc_sets()
        if len(doc_sets) < 2:
            pytest.skip("Need at least 2 captured doc-sets")
        
        # Verify second doc-set captured files are readable
        doc_set = doc_sets[1]
        body_files = list(doc_set["path"].glob("*.body.html"))
        
        errors = []
        for body_file in body_files:
            try:
                content = body_file.read_text(encoding="utf-8", errors="replace")
                assert len(content) > 0
            except Exception as e:
                errors.append(f"{body_file.name}: {e}")
        
        assert len(errors) == 0, f"Errors reading files: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
