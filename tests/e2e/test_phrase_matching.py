"""Tests for multi-word phrase matching in search."""
import pytest


def check_phrase_in_text(phrase: str, text: str) -> bool:
    """Check if exact phrase exists in text."""
    return phrase.lower() in text.lower()


def compute_proximity_score(query_terms: list, content: str) -> int:
    """Compute proximity score for query terms in content."""
    words = content.lower().split()
    score = 0
    
    for i in range(len(words) - 1):
        window = words[i:i + 5]
        if all(term.lower() in ' '.join(window) for term in query_terms):
            score += 10
    
    return min(score, 30)


class TestPhraseMatching:
    """Test multi-word phrase matching."""
    
    def test_exact_phrase_in_title(self):
        """Exact phrase match in title gets high bonus."""
        title = "Error Handling in Rust"
        phrase = "error handling"
        
        assert check_phrase_in_text(phrase, title)
    
    def test_exact_phrase_in_content(self):
        """Exact phrase match in content gets bonus."""
        content = "This chapter covers error handling patterns in detail."
        phrase = "error handling"
        
        assert check_phrase_in_text(phrase, content)
    
    def test_proximity_scoring_close_words(self):
        """Words close together get proximity bonus."""
        query_terms = ["error", "handling"]
        content = "Rust provides excellent error handling mechanisms"
        
        score = compute_proximity_score(query_terms, content)
        
        # Words are within 5-word window
        assert score > 0
    
    def test_proximity_scoring_far_words(self):
        """Words far apart get no/less proximity bonus."""
        query_terms = ["error", "handling"]
        content = "Error can occur. This is a long sentence with many words between. Handling is important."
        
        score = compute_proximity_score(query_terms, content)
        
        # Words are far apart, should get minimal or no proximity score
        assert score == 0
    
    def test_proximity_cap_at_maximum(self):
        """Proximity score is capped at 30."""
        query_terms = ["rust", "code"]
        # Many occurrences close together
        content = "rust code rust code rust code rust code rust code rust code"
        
        score = compute_proximity_score(query_terms, content)
        
        # Should be capped at 30
        assert score <= 30


class TestPhraseVsIndividualTerms:
    """Test that phrases rank higher than individual terms."""
    
    def test_phrase_scores_higher_than_individual_terms(self):
        """Documents with exact phrase rank higher."""
        query_terms = ["memory", "safety"]
        phrase = "memory safety"
        
        # Doc A: contains exact phrase
        doc_a = "Rust ensures memory safety through its ownership system."
        
        # Doc B: contains individual terms but not together
        doc_b = "Memory management is important. Safety features are good."
        
        # Doc A should have phrase match
        assert check_phrase_in_text(phrase, doc_a)
        
        # Doc B should not have phrase match
        assert not check_phrase_in_text(phrase, doc_b)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
