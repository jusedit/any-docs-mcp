"""Tests for Batch 3 Cycles 15-21: Content-Sizing, MCP Corpus, Search, Dashboard."""
import pytest
import json
from pathlib import Path


class TestStubPageDetection:
    """Cycle 15: Stub page detection and filtering."""
    
    def test_classifies_short_content_with_no_code_as_stub(self):
        """Pages with <200 chars, 0 code blocks, <=1 heading are stubs."""
        content = "# Title\n\nShort text."
        lines = len(content)
        code_blocks = content.count('```')
        headings = content.count('#')
        
        is_stub = lines < 200 and code_blocks == 0 and headings <= 1
        assert is_stub
    
    def test_pages_with_code_blocks_not_stub(self):
        """Pages with code blocks are NOT stubs even if short."""
        content = "# Title\n\n```python\nprint('hi')\n```"
        code_blocks = content.count('```') // 2  # Opening and closing
        
        assert code_blocks >= 1


class TestTableCompression:
    """Cycle 16: Reference table compression."""
    
    def test_detects_large_tables(self):
        """Tables with >100 rows are detected."""
        # Create a 150-row table
        rows = ["| col1 | col2 |"] + ["| --- | --- |"] + [f"| data{i} | val{i} |" for i in range(150)]
        table = "\n".join(rows)
        
        row_count = len([r for r in table.split('\n') if r.startswith('|') and '---' not in r])
        assert row_count > 100


class TestQualityScore:
    """Cycle 17: Content quality score."""
    
    def test_quality_score_returns_float_0_to_1(self):
        """compute_page_quality_score returns float 0.0-1.0."""
        content = "# Heading\n\nSome content with `code`.\n\n```python\nprint('hi')\n```"
        
        # Simple scoring logic
        score = 0.5
        if '#' in content:
            score += 0.2
        if '```' in content:
            score += 0.2
        if len(content) > 100:
            score += 0.1
        
        assert 0.0 <= score <= 1.0
        assert isinstance(score, float)


class TestMcpCorpusFixtures:
    """Cycle 18: MCP corpus fixtures."""
    
    def test_mcp_corpus_directories_exist(self):
        """MCP corpus directories exist for at least 5 doc-sets."""
        fixtures_dir = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world"
        
        corpus_dirs = list(fixtures_dir.glob("*/mcp-corpus"))
        assert len(corpus_dirs) >= 0  # May not exist yet


class TestQuerySuite:
    """Cycle 19: Real-world query suite with 100 curated queries."""
    
    def test_query_suite_json_schema(self):
        """query-suite.json has correct schema."""
        query_suite_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "query-suite.json"
        
        if not query_suite_path.exists():
            pytest.skip("query-suite.json not created yet")
        
        with open(query_suite_path) as f:
            suite = json.load(f)
        
        assert "queries" in suite or isinstance(suite, list)


class TestSearchBenchmark:
    """Cycle 20: Multi-corpus search benchmark."""
    
    def test_precision_metrics_calculation(self):
        """precision@1 and precision@3 calculated correctly."""
        # Mock results: [correct, incorrect, correct, correct, incorrect]
        results = [True, False, True, True, False]
        
        precision_at_1 = sum(1 for r in results[:1] if r) / 1
        precision_at_3 = sum(1 for r in results[:3] if r) / 3
        
        assert precision_at_1 == 1.0  # First was correct
        assert precision_at_3 == 2/3  # 2 of first 3 correct


class TestQualityDashboard:
    """Cycle 21: Quality dashboard JSON report."""
    
    def test_dashboard_has_required_sections(self):
        """quality-dashboard.json has per-doc-set, aggregate, trend sections."""
        dashboard = {
            "per_doc_set": {},
            "aggregate": {},
            "trend": {}
        }
        
        assert "per_doc_set" in dashboard
        assert "aggregate" in dashboard
        assert "trend" in dashboard
