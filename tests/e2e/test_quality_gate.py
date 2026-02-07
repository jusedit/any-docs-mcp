"""Tests for run_quality_gate.py."""
import pytest
import sys
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))

from run_quality_gate import check_thresholds, generate_dashboard, THRESHOLDS


class TestQualityThresholds:
    """Test quality threshold checking."""
    
    def test_all_thresholds_met_returns_passed(self):
        """All scores above thresholds returns passed."""
        dashboard = {
            "quality_scores": {
                "avg_markdown_score": 0.85,  # Above 0.80
                "avg_search_score": 0.60,    # Above 0.50
                "avg_overall_score": 0.70,   # Above 0.65
            }
        }
        
        passed, violations = check_thresholds(dashboard)
        
        assert passed is True
        assert len(violations) == 0
    
    def test_markdown_score_below_threshold_fails(self):
        """Markdown score below 0.80 fails gate."""
        dashboard = {
            "quality_scores": {
                "avg_markdown_score": 0.75,  # Below 0.80
                "avg_search_score": 0.60,
                "avg_overall_score": 0.70,
            }
        }
        
        passed, violations = check_thresholds(dashboard)
        
        assert passed is False
        assert any("avg_markdown_score" in v for v in violations)
    
    def test_search_score_below_threshold_fails(self):
        """Search score below 0.50 fails gate."""
        dashboard = {
            "quality_scores": {
                "avg_markdown_score": 0.85,
                "avg_search_score": 0.45,    # Below 0.50
                "avg_overall_score": 0.70,
            }
        }
        
        passed, violations = check_thresholds(dashboard)
        
        assert passed is False
        assert any("avg_search_score" in v for v in violations)
    
    def test_overall_score_below_threshold_fails(self):
        """Overall score below 0.65 fails gate."""
        dashboard = {
            "quality_scores": {
                "avg_markdown_score": 0.85,
                "avg_search_score": 0.60,
                "avg_overall_score": 0.60,   # Below 0.65
            }
        }
        
        passed, violations = check_thresholds(dashboard)
        
        assert passed is False
        assert any("avg_overall_score" in v for v in violations)
    
    def test_exact_threshold_values_pass(self):
        """Exact threshold values pass the gate."""
        dashboard = {
            "quality_scores": {
                "avg_markdown_score": 0.80,  # Exactly threshold
                "avg_search_score": 0.50,    # Exactly threshold
                "avg_overall_score": 0.65,   # Exactly threshold
            }
        }
        
        passed, violations = check_thresholds(dashboard)
        
        # Exact values should pass (not strictly less than)
        assert passed is True


class TestDashboardGeneration:
    """Test quality dashboard generation."""
    
    def test_dashboard_has_required_fields(self):
        """Dashboard contains all required fields."""
        dashboard = generate_dashboard()
        
        assert "timestamp" in dashboard
        assert "test_results" in dashboard
        assert "quality_scores" in dashboard
        assert "thresholds" in dashboard
        assert "gate_status" in dashboard
    
    def test_test_results_structure(self):
        """Test results have correct structure."""
        dashboard = generate_dashboard()
        
        tr = dashboard["test_results"]
        assert "total_tests" in tr
        assert "passed" in tr
        assert "failed" in tr
        assert "skipped" in tr
    
    def test_quality_scores_match_thresholds(self):
        """Quality scores match threshold keys."""
        dashboard = generate_dashboard()
        
        for metric in THRESHOLDS.keys():
            assert metric in dashboard["quality_scores"]


class TestScriptExecution:
    """Test script execution modes."""
    
    def test_help_flag_works(self):
        """--help flag shows usage."""
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "run_quality_gate.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        assert result.returncode == 0
        assert "Quality Gate Runner" in result.stdout
    
    def test_thresholds_flag_shows_values(self):
        """--thresholds flag shows threshold values."""
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "run_quality_gate.py"), "--thresholds"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        assert result.returncode == 0
        assert "Quality Thresholds" in result.stdout or "avg_markdown_score" in result.stdout
    
    def test_json_flag_outputs_valid_json(self):
        """--json flag outputs valid JSON."""
        import json
        
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "run_quality_gate.py"), "--json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        # Should parse as JSON
        data = json.loads(result.stdout)
        assert "test_results" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
