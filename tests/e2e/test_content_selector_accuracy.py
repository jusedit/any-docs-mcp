"""Tests for content selector accuracy per site-type."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scraper"))

from bs4 import BeautifulSoup


class TestContentSelectorAccuracy:
    """Test content selector extraction accuracy."""
    
    def extract_content(self, html: str, selectors: list, exclude_selectors: list = None) -> str:
        """Extract content using CSS selectors."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove excluded elements first
        if exclude_selectors:
            for selector in exclude_selectors:
                for elem in soup.select(selector):
                    elem.decompose()
        
        # Try each content selector in order
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                return '\n'.join(str(elem) for elem in elements)
        
        return ''
    
    def test_mkdocs_content_extraction(self):
        """MkDocs sites extract main content correctly."""
        # Simulated MkDocs HTML structure
        html = '''
        <html>
        <body>
            <nav class="md-nav">Navigation Menu</nav>
            <main class="md-content">
                <h1>Getting Started</h1>
                <p>Welcome to the documentation. This guide will help you.</p>
                <pre><code>pip install package</code></pre>
            </main>
            <footer>Copyright 2024</footer>
        </body>
        </html>
        '''
        
        selectors = ['main.md-content', 'article', '.content']
        exclude = ['nav.md-nav', 'footer']
        
        content = self.extract_content(html, selectors, exclude)
        
        # Must contain expected content
        assert 'Getting Started' in content
        assert 'Welcome to the documentation' in content
        assert 'pip install package' in content
        
        # Must NOT contain navigation/footer
        assert 'Navigation Menu' not in content
        assert 'Copyright' not in content
    
    def test_docusaurus_content_extraction(self):
        """Docusaurus sites extract main content correctly."""
        html = '''
        <html>
        <body>
            <div class="theme-doc-sidebar-container">Sidebar Nav</div>
            <div class="theme-doc-markdown">
                <h1>Installation</h1>
                <p>To install the package, run the command below.</p>
                <div class="codeBlockContent">npm install</div>
            </div>
            <div class="pagination-nav">Next Page</div>
        </body>
        </html>
        '''
        
        selectors = ['.theme-doc-markdown', 'article', 'main']
        exclude = ['.theme-doc-sidebar-container', '.pagination-nav']
        
        content = self.extract_content(html, selectors, exclude)
        
        assert 'Installation' in content
        assert 'npm install' in content
        assert 'Sidebar Nav' not in content
        assert 'Next Page' not in content
    
    def test_hugo_content_extraction(self):
        """Hugo sites extract main content correctly."""
        html = '''
        <html>
        <body>
            <nav class="td-navbar">Main Navigation</nav>
            <div class="td-sidebar">Side Menu</div>
            <main class="td-main">
                <div class="td-content">
                    <h1>Overview</h1>
                    <p>This is the overview section of the documentation.</p>
                    <div class="highlight"><pre>go run main.go</pre></div>
                </div>
            </main>
            <footer class="td-footer">Footer</footer>
        </body>
        </html>
        '''
        
        selectors = ['.td-content', 'main', 'article']
        exclude = ['.td-navbar', '.td-sidebar', '.td-footer']
        
        content = self.extract_content(html, selectors, exclude)
        
        assert 'Overview' in content
        assert 'go run main.go' in content
        assert 'Main Navigation' not in content
        assert 'Side Menu' not in content
    
    def test_sphinx_content_extraction(self):
        """Sphinx sites extract main content correctly."""
        html = '''
        <html>
        <body class="wy-body-for-nav">
            <nav class="wy-nav-side">Sphinx Nav</nav>
            <section class="wy-nav-content-wrap">
                <main class="wy-nav-content">
                    <div class="document">
                        <h1>API Reference</h1>
                        <p>The API provides the following endpoints.</p>
                        <div class="highlight-python"><pre>def api(): pass</pre></div>
                    </div>
                </main>
            </section>
            <footer>Footer content</footer>
        </body>
        </html>
        '''
        
        selectors = ['.document', 'main.wy-nav-content', 'article']
        exclude = ['.wy-nav-side', 'footer']
        
        content = self.extract_content(html, selectors, exclude)
        
        assert 'API Reference' in content
        assert 'def api(): pass' in content
        assert 'Sphinx Nav' not in content
    
    def test_custom_content_extraction(self):
        """Custom sites extract main content correctly."""
        html = '''
        <html>
        <body>
            <header>Site Header</header>
            <aside class="sidebar">Table of Contents</aside>
            <div class="doc-content">
                <h1>Introduction</h1>
                <p>This is a custom documentation site.</p>
                <code>import module</code>
            </div>
            <div class="footer-links">Footer</div>
        </body>
        </html>
        '''
        
        selectors = ['.doc-content', '.content', 'main', 'article']
        exclude = ['.sidebar', 'header', '.footer-links']
        
        content = self.extract_content(html, selectors, exclude)
        
        assert 'Introduction' in content
        assert 'import module' in content
        assert 'Table of Contents' not in content
    
    def test_code_blocks_preserved(self):
        """Code blocks are preserved in content extraction."""
        html = '''
        <main>
            <h1>Tutorial</h1>
            <p>Follow this example:</p>
            <pre class="language-python"><code>def hello():
    return "world"</code></pre>
            <p>More text after code.</p>
        </main>
        '''
        
        selectors = ['main']
        content = self.extract_content(html, selectors)
        
        assert 'def hello():' in content
        assert 'return "world"' in content
    
    def test_nested_content_extraction(self):
        """Nested content structures are handled correctly."""
        html = '''
        <article>
            <header>Article Header (should be removed)</header>
            <div class="content">
                <h1>Main Title</h1>
                <p>Main content paragraph.</p>
                <section>
                    <h2>Subsection</h2>
                    <p>Nested content.</p>
                </section>
            </div>
            <footer>Article Footer</footer>
        </article>
        '''
        
        selectors = ['.content', 'article']
        exclude = ['header', 'footer']
        
        content = self.extract_content(html, selectors, exclude)
        
        assert 'Main Title' in content
        assert 'Main content paragraph' in content
        assert 'Subsection' in content
        assert 'Nested content' in content
        assert 'Article Header' not in content
        assert 'Article Footer' not in content


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
