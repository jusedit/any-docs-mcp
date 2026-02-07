"""Tests for code block language tag correction."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from content_cleaner import ContentCleaner


class TestCodeBlockLanguageCorrection:
    """Test code block language correction."""
    
    def test_css_class_mapping(self):
        """CSS classes are mapped to correct languages."""
        cleaner = ContentCleaner()
        content = '```language-js\nconst x = 1;\n```'
        
        cleaned = cleaner.clean(content)
        
        assert '```javascript' in cleaned
        assert '```language-js' not in cleaned
    
    def test_python_class_mapping(self):
        """Python CSS classes are mapped correctly."""
        cleaner = ContentCleaner()
        content = '```language-py\ndef hello():\n    pass\n```'
        
        cleaned = cleaner.clean(content)
        
        assert '```python' in cleaned
        assert '```language-py' not in cleaned
    
    def test_bad_languages_removed(self):
        """Bad language tags are removed."""
        cleaner = ContentCleaner()
        content = '```sp-pre-placeholder\ncode\n```'
        
        cleaned = cleaner.clean(content)
        
        assert '```sp-pre-placeholder' not in cleaned
        assert '\ncode\n' in cleaned
    
    def test_auto_detect_javascript(self):
        """JavaScript is auto-detected from content."""
        cleaner = ContentCleaner()
        content = '```\nconst x = 1;\nlet y = "hello";\nfunction test() { return x; }\n```'
        
        cleaned = cleaner.clean(content)
        
        assert '```javascript' in cleaned
    
    def test_auto_detect_python(self):
        """Python is auto-detected from content."""
        cleaner = ContentCleaner()
        content = '```\ndef hello():\n    return "world"\nimport os\n```'
        
        cleaned = cleaner.clean(content)
        
        assert '```python' in cleaned
    
    def test_auto_detect_go(self):
        """Go is auto-detected from content."""
        cleaner = ContentCleaner()
        content = '```\nfunc main() {\n    fmt.Println("hello")\n}\npackage main\n```'
        
        cleaned = cleaner.clean(content)
        
        assert '```go' in cleaned
    
    def test_normalization_short_forms(self):
        """Short language forms are normalized."""
        cleaner = ContentCleaner()
        content = '```js\nvar x = 1;\n```'
        
        cleaned = cleaner.clean(content)
        
        assert '```javascript' in cleaned
        assert '```js' not in cleaned
    
    def test_dockerfile_misclassification_fixed(self):
        """Content wrongly tagged as dockerfile is corrected."""
        cleaner = ContentCleaner()
        # This looks like JavaScript but was misclassified as dockerfile
        content = '```dockerfile\nimport React from "react";\nconst App = () => { return <div />; };\n```'
        
        cleaned = cleaner.fix_code_block_languages(content)
        
        # Should detect JavaScript from content
        assert '```javascript' in cleaned or '```jsx' in cleaned


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
