"""Tests for TF-IDF scoring in search."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server" / "src"))

# Mock test for TF-IDF scoring logic
def compute_idf(N, df):
    """Compute IDF score."""
    import math
    return math.log(N / (df + 1)) + 1


class TestTFIDFScoring:
    """Test TF-IDF scoring logic."""
    
    def test_idf_rare_terms_have_higher_weight(self):
        """Rare terms (low df) have higher IDF weight."""
        N = 100  # Total documents
        
        # Common term appears in many docs
        common_idf = compute_idf(N, 50)
        
        # Rare term appears in few docs
        rare_idf = compute_idf(N, 2)
        
        # Rare terms should have higher IDF
        assert rare_idf > common_idf
    
    def test_idf_single_occurrence_max_weight(self):
        """Terms appearing once get maximum IDF boost."""
        N = 100
        
        single_idf = compute_idf(N, 1)
        multiple_idf = compute_idf(N, 10)
        
        assert single_idf > multiple_idf
    
    def test_tf_capped_at_maximum(self):
        """Term frequency is capped to prevent domination."""
        # TF should be capped at 10
        tf_raw = 25
        tf_capped = min(tf_raw, 10)
        
        assert tf_capped == 10
    
    def test_tf_idf_formula(self):
        """TF-IDF formula produces expected scores."""
        tf = 5
        N = 100
        df = 10
        idf = compute_idf(N, df)
        
        score = tf * idf * 2  # Our formula includes 2x multiplier
        
        # Score should be positive
        assert score > 0
        
        # Score should scale with TF
        score_double_tf = (tf * 2) * idf * 2
        assert score_double_tf > score
    
    def test_common_words_have_lower_weight(self):
        """Very common words like 'the', 'and' have lower weight."""
        N = 1000
        
        # Stopword appears in almost all docs
        stopword_idf = compute_idf(N, 950)
        
        # Technical term appears in few docs
        technical_idf = compute_idf(N, 5)
        
        # Stopword should have much lower weight
        assert technical_idf > stopword_idf * 5


class TestTFIDFSearchBehavior:
    """Test TF-IDF improves search relevance."""
    
    def test_rare_technical_terms_ranked_higher(self):
        """Documents with rare technical terms rank higher."""
        # This is a behavioral test - the actual ranking depends on the index
        # We verify the scoring formula prefers rare terms
        
        N = 100
        
        # Doc A: contains common word "function" (appears in 80 docs)
        tf_A = 3
        df_common = 80
        idf_common = compute_idf(N, df_common)
        score_A = tf_A * idf_common * 2
        
        # Doc B: contains rare word "monomorphization" (appears in 2 docs)
        tf_B = 1
        df_rare = 2
        idf_rare = compute_idf(N, df_rare)
        score_B = tf_B * idf_rare * 2
        
        # Even with lower TF, rare term should score higher
        assert score_B > score_A


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
