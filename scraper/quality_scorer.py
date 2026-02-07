"""Content quality scoring for scraped pages."""
import re
from typing import Dict


class QualityScorer:
    """Evaluates quality of cleaned markdown pages."""
    
    def compute_score(self, content: str) -> float:
        """Compute quality score from 0.0 to 1.0.
        
        Factors:
        - Heading structure (0.2)
        - Code block presence (0.2)
        - Content density (0.2)
        - Artifact residue penalty (-0.2)
        - Length factor (0.4 max)
        """
        if not content or len(content) < 50:
            return 0.0
        
        score = 0.0
        
        # Heading structure
        headings = re.findall(r'^#{1,6}\s', content, re.MULTILINE)
        if headings:
            score += 0.2
        
        # Code blocks
        if '```' in content:
            score += 0.2
        
        # Content length (up to 0.4)
        length_factor = min(len(content) / 2000, 1.0) * 0.4
        score += length_factor
        
        # Density (ratio of text to total)
        lines = content.split('\n')
        non_empty = [l for l in lines if l.strip()]
        if lines:
            density = len(non_empty) / len(lines)
            score += density * 0.2
        
        return min(1.0, max(0.0, score))
