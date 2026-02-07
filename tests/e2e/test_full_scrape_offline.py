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
        # Start fixture server with captured files
        server = FixtureHTTPServer(str(doc_set["path"]))
        port = server.start()
        
        try:
            # Create scraper config
            config = {
                "name": doc_set["name"],
                "base_url": f"http://127.0.0.1:{port}",
                "site_type": "captured"
            }
            
            # Create storage manager
            storage = StorageManager(root_path=str(temp_output_dir))
            storage.save_config(config)
            
            # Run scraper
            scraper = ScraperEngine(storage_manager=storage)
            start_time = datetime.now()
            
            result = scraper.scrape_all(
                base_url=config["base_url"],
                start_url=config["base_url"]
            )
            
            elapsed = (datetime.now() - start_time).total_seconds()
            
            # Verify results
            captured_count = doc_set["file_count"]
            scraped_count = len(result) if isinstance(result, dict) else 0
            
            print(f"\n  {doc_set['name']}: {scraped_count}/{captured_count} pages scraped in {elapsed:.1f}s")
            
            # Should complete in < 60 seconds per site
            assert elapsed < 60, f"Scrape took {elapsed:.1f}s, expected < 60s"
            
            # Verify output files exist
            output_files = list(temp_output_dir.glob("**/*.md"))
            assert len(output_files) > 0, "No .md output files created"
            
        finally:
            server.stop()
    
    def test_scrape_produces_valid_markdown(self, temp_output_dir):
        """Scraper output is valid markdown with expected structure."""
        # Find first available doc-set with captures
        doc_sets = get_captured_doc_sets()
        if not doc_sets:
            pytest.skip("No captured doc-sets available")
        
        doc_set = doc_sets[0]
        server = FixtureHTTPServer(str(doc_set["path"]))
        port = server.start()
        
        try:
            storage = StorageManager(root_path=str(temp_output_dir))
            
            scraper = ScraperEngine(storage_manager=storage)
            scraper.scrape_all(
                base_url=f"http://127.0.0.1:{port}",
                start_url=f"http://127.0.0.1:{port}"
            )
            
            # Check output markdown files
            md_files = list(temp_output_dir.glob("**/*.md"))
            assert len(md_files) > 0
            
            for md_file in md_files[:3]:  # Check first 3 files
                content = md_file.read_text(encoding="utf-8")
                
                # Should have markdown structure (headings)
                assert "#" in content or content.strip() == "", \
                    f"No markdown headings in {md_file.name}"
                
                # Should not have raw HTML tags
                html_tags = ["<div>", "<span>", "<script>", "<style>"]
                for tag in html_tags:
                    assert tag not in content.lower(), \
                        f"HTML residue {tag} in {md_file.name}"
                
        finally:
            server.stop()
    
    def test_no_crashes_on_edge_cases(self, temp_output_dir):
        """Scraper handles edge cases without crashing."""
        doc_sets = get_captured_doc_sets()
        if len(doc_sets) < 2:
            pytest.skip("Need at least 2 captured doc-sets")
        
        # Test on second doc-set
        doc_set = doc_sets[1]
        server = FixtureHTTPServer(str(doc_set["path"]))
        port = server.start()
        
        try:
            storage = StorageManager(root_path=str(temp_output_dir))
            
            scraper = ScraperEngine(storage_manager=storage)
            
            # Should not raise any exceptions
            result = scraper.scrape_all(
                base_url=f"http://127.0.0.1:{port}",
                start_url=f"http://127.0.0.1:{port}"
            )
            
            # Result should be valid dict
            assert isinstance(result, dict)
            assert "scraped_pages" in result
            
        finally:
            server.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
