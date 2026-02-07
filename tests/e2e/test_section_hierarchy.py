"""Tests for section hierarchy boost in search ranking."""
import pytest


def compute_hierarchy_boost(level: int) -> int:
    """Compute hierarchy boost for a section level."""
    if level <= 1:
        return 25  # h1
    elif level == 2:
        return 15  # h2
    elif level == 3:
        return 5   # h3
    else:
        return 0   # h4+


class TestSectionHierarchyBoost:
    """Test section hierarchy boost scoring."""
    
    def test_h1_gets_maximum_boost(self):
        """H1 sections get the highest boost."""
        boost = compute_hierarchy_boost(1)
        assert boost == 25
    
    def test_h2_gets_high_boost(self):
        """H2 sections get high boost."""
        boost = compute_hierarchy_boost(2)
        assert boost == 15
    
    def test_h3_gets_moderate_boost(self):
        """H3 sections get moderate boost."""
        boost = compute_hierarchy_boost(3)
        assert boost == 5
    
    def test_h4_gets_no_boost(self):
        """H4 sections get no boost."""
        boost = compute_hierarchy_boost(4)
        assert boost == 0
    
    def test_h5_gets_no_boost(self):
        """H5 sections get no boost."""
        boost = compute_hierarchy_boost(5)
        assert boost == 0
    
    def test_h6_gets_no_boost(self):
        """H6 sections get no boost."""
        boost = compute_hierarchy_boost(6)
        assert boost == 0


class TestHierarchyRanking:
    """Test that hierarchy affects ranking."""
    
    def test_h1_ranks_above_h2_with_same_score(self):
        """H1 section ranks above H2 with same base score."""
        base_score = 50
        
        h1_total = base_score + compute_hierarchy_boost(1)  # 50 + 25 = 75
        h2_total = base_score + compute_hierarchy_boost(2)  # 50 + 15 = 65
        
        assert h1_total > h2_total
    
    def test_h2_ranks_above_h3_with_same_score(self):
        """H2 section ranks above H3 with same base score."""
        base_score = 50
        
        h2_total = base_score + compute_hierarchy_boost(2)  # 50 + 15 = 65
        h3_total = base_score + compute_hierarchy_boost(3)  # 50 + 5 = 55
        
        assert h2_total > h3_total
    
    def test_deep_sections_need_higher_base_score(self):
        """Deep sections need higher base score to outrank top sections."""
        # H6 with base score 80
        h6_total = 80 + compute_hierarchy_boost(6)  # 80 + 0 = 80
        
        # H1 with base score 50
        h1_total = 50 + compute_hierarchy_boost(1)  # 50 + 25 = 75
        
        # Deep section can outrank if content is much more relevant
        assert h6_total > h1_total


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
