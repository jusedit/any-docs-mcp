"""Stub page detection for filtering low-quality content."""
import re
from typing import Tuple, Optional


class StubDetector:
    """Detects and filters stub pages from scraped output."""
    
    def __init__(self, min_content_chars: int = 200):
        self.min_content_chars = min_content_chars
    
    def is_stub(self, content: str) -> Tuple[bool, dict]:
        """Check if content qualifies as a stub page.
        
        Returns:
            Tuple of (is_stub, metadata_dict)
        """
        char_count = len(content)
        code_blocks = len(re.findall(r'```[\w]*', content))
        headings = len(re.findall(r'^#{1,6}\s', content, re.MULTILINE))
        
        is_stub = (
            char_count < self.min_content_chars and
            code_blocks == 0 and
            headings <= 1
        )
        
        return is_stub, {
            'char_count': char_count,
            'code_blocks': code_blocks,
            'headings': headings
        }
