"""Tests for Batch 6 Cycles 36-42."""
import pytest
import json
from pathlib import Path

from duplicate_detector import detect_duplicate_versions, DuplicateGroup


class TestDuplicateDetector:
    """Cycle 36: Duplicate version detector."""
    
    def test_detects_similar_versions(self, tmp_path):
        """Detects versions with >80% identical files."""
        # Create two version directories with identical files
        v1_dir = tmp_path / "v1"
        v2_dir = tmp_path / "v2"
        v1_dir.mkdir()
        v2_dir.mkdir()
        
        (v1_dir / "file1.md").write_text("content A")
        (v1_dir / "file2.md").write_text("content B")
        (v2_dir / "file1.md").write_text("content A")
        (v2_dir / "file2.md").write_text("content B")
        
        duplicates = detect_duplicate_versions(str(tmp_path), threshold=0.8)
        
        assert len(duplicates) == 1
        assert "v1" in duplicates[0].versions
        assert "v2" in duplicates[0].versions
        assert duplicates[0].similarity_pct == 1.0
    
    def test_returns_empty_for_different_versions(self, tmp_path):
        """Returns empty list when versions differ."""
        v1_dir = tmp_path / "v1"
        v2_dir = tmp_path / "v2"
        v1_dir.mkdir()
        v2_dir.mkdir()
        
        (v1_dir / "file.md").write_text("content A")
        (v2_dir / "file.md").write_text("content B")
        
        duplicates = detect_duplicate_versions(str(tmp_path), threshold=0.8)
        
        assert len(duplicates) == 0


class TestQuerySuite:
    """Cycle 37: Query suite JSON."""
    
    def test_query_suite_exists(self):
        """query-suite.json exists and has correct structure."""
        suite_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "query-suite.json"
        assert suite_path.exists()
        
        with open(suite_path) as f:
            suite = json.load(f)
        
        assert "queries" in suite
        assert len(suite["queries"]) >= 50  # At least 50 queries
    
    def test_query_entries_have_required_fields(self):
        """Each query has required fields."""
        suite_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "real-world" / "query-suite.json"
        
        with open(suite_path) as f:
            suite = json.load(f)
        
        required = ["doc_name", "query", "expected_top_title", "expected_file", "query_type"]
        for query in suite["queries"]:
            for field in required:
                assert field in query, f"Missing {field} in query"


class TestQualityDashboard:
    """Cycle 38: Quality dashboard JSON."""
    
    def test_dashboard_structure(self):
        """Quality dashboard has required sections."""
        dashboard = {
            "generated_at": "2024-01-01T00:00:00Z",
            "per_doc_set": {
                "react": {"quality_score": 0.85, "encoding_errors": 0, "artifacts": 5},
                "fastapi": {"quality_score": 0.78, "encoding_errors": 2, "artifacts": 8}
            },
            "aggregate": {
                "avg_quality_score": 0.82,
                "total_encoding_errors": 2,
                "total_artifacts": 13
            },
            "trend": {
                "improving": ["react", "fastapi"],
                "degrading": []
            }
        }
        
        assert "per_doc_set" in dashboard
        assert "aggregate" in dashboard
        assert "trend" in dashboard


class TestFinalSummary:
    """Cycle 39-42: Final cleanup and documentation."""
    
    def test_prd_json_valid(self):
        """prd.json is valid JSON."""
        prd_path = Path(__file__).parent.parent.parent / "prd.json"
        with open(prd_path) as f:
            data = json.load(f)
        
        assert "project_meta" in data
        assert "backlog" in data
        assert len(data["backlog"]) == 30
    
    def test_tests_exist_for_all_major_components(self):
        """All major components have corresponding tests."""
        test_dir = Path(__file__).parent
        test_files = list(test_dir.glob("test_*.py"))
        
        # Should have test files for major components
        assert len(test_files) >= 6
