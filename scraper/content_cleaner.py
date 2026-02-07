"""
Content cleaner for post-processing scraped markdown content.
Removes UI artifacts, fixes code blocks, and cleans up common issues.
"""
import re
from typing import List, Tuple


class ContentCleaner:
    """Clean scraped markdown content by removing artifacts and fixing issues."""
    
    # Site-type specific profiles
    PROFILES = {
        'mkdocs': {
            'patterns': [
                r'Edit on GitHub',
                r'Edit on GitLab', 
                r'Last updated:\s*\w+ \d{1,2}, \d{4}',
                r'!!! \w+',  # Admonition markers
                r'\?\?\? \w+',  # Details markers
            ]
        },
        'sphinx': {
            'patterns': [
                r'Changed in version \d+\.\d+',
                r'New in version \d+\.\d+',
                r'Deprecated since version \d+\.\d+',
                r'\(source\)',
                r':ref:`[^`]+`',
                r':doc:`[^`]+`',
            ]
        },
        'docusaurus': {
            'patterns': [
                r'ReloadClear',
                r'sp-pre-placeholder',
                r'TabItem',
                r'CodeSandbox',
                r'StackBlitz',
            ]
        },
        'hugo': {
            'patterns': [
                r'On this page',
                r'Last modified:\s*\w+ \d{1,2}, \d{4}',
                r'Edit this page',
                r'Was this page helpful\?',
                r'Home\s*>\s*Docs',
            ]
        },
        'tailwind': {
            'patterns': [
                # Tailwind utility class divs
                r'<div[^>]*class="[^"]*(?:bg-|text-|p-|m-|flex|grid|border|rounded|shadow|hover:|focus:|active:)[^"]*"[^>]*>.*?</div>',
                r'<span[^>]*class="[^"]*(?:bg-|text-|p-|m-|flex|grid|border|rounded|shadow|hover:|focus:|active:)[^"]*"[^>]*>.*?</span>',
                # Color swatches
                r'<div[^>]*class="[^"]*(?:#\w{3,6}|(?:rgb|hsl)a?\()[^"]*"[^>]*>.*?</div>',
                r'\[#[0-9A-Fa-f]{6}\]\([^)]*\)',  # Color links like [#3b82f6](...)
                # Interactive code examples
                r'\[Try it\]\(https://play\.tailwindcss\.com[^)]*\)',
                # TOC remnants
                r'On this page\n\*\s*\[',
                # Version badges
                r'v\d+\.\d+(?:\.\d+)?\s*Latest',
            ]
        },
        'generic-spa': {
            'patterns': [
                r'Cookie Policy',
                r'Accept all cookies',
                r'Reject all',
                r'Subscribe',
                r'Enter your email',
                r'Back to top',
                r'Copyright \d+',
                r'Terms of Service',
                r'Privacy Policy',
            ]
        }
    }
    
    # Known bad code block language tags
    BAD_LANGUAGES = [
        'sp-pre-placeholder',
        'shiki', 
        'index-module__DOXIJG__content',
        'language-undefined',
        'highlight',
        'code-block',
    ]
    
    # CSS class to language mapping for correcting markdownify output
    CSS_CLASS_TO_LANGUAGE = {
        # JavaScript variants
        'language-js': 'javascript',
        'language-javascript': 'javascript',
        'language-jsx': 'jsx',
        'language-ts': 'typescript',
        'language-typescript': 'typescript',
        'language-tsx': 'tsx',
        # Python
        'language-py': 'python',
        'language-python': 'python',
        'language-python3': 'python',
        'highlight-python': 'python',
        # Shell/Terminal
        'language-sh': 'bash',
        'language-shell': 'bash',
        'language-bash': 'bash',
        'language-zsh': 'bash',
        'language-console': 'bash',
        'language-terminal': 'bash',
        # Markup/Data
        'language-html': 'html',
        'language-xml': 'xml',
        'language-css': 'css',
        'language-scss': 'scss',
        'language-sass': 'sass',
        'language-json': 'json',
        'language-yaml': 'yaml',
        'language-yml': 'yaml',
        'language-toml': 'toml',
        'language-md': 'markdown',
        'language-markdown': 'markdown',
        # Systems languages
        'language-rs': 'rust',
        'language-rust': 'rust',
        'language-go': 'go',
        'language-golang': 'go',
        'language-c': 'c',
        'language-cpp': 'cpp',
        'language-c++': 'cpp',
        'language-java': 'java',
        'language-kt': 'kotlin',
        'language-kotlin': 'kotlin',
        'language-swift': 'swift',
        # Web frameworks
        'language-vue': 'vue',
        'language-svelte': 'svelte',
        'language-astro': 'astro',
        # Other
        'language-dockerfile': 'dockerfile',
        'language-docker': 'dockerfile',
        'language-sql': 'sql',
        'language-graphql': 'graphql',
        'language-regex': 'regex',
        'language-diff': 'diff',
    }
    
    # UI artifacts to remove (regex patterns)
    UI_ARTIFACT_PATTERNS = [
        # CodeSandbox/playground buttons
        r'ReloadClear\[Fork\]\([^)]*\)',
        r'\[Fork\]\(https://codesandbox\.io[^)]*\)',
        r'\[Open in CodeSandbox\]\([^)]*\)',
        r'\[Open in StackBlitz\]\([^)]*\)',
        r'\[Try it\]\([^)]*\)',
        
        # Copy buttons
        r'Copy to clipboard',
        r'Copy code',
        r'Copied!',
        r'TypeScriptCopy to clipboard',
        r'JavaScriptCopy to clipboard',
        r'ShellCopy to clipboard',
        r'BashCopy to clipboard',
        
        # Navigation artifacts
        r'\[Previous[^\]]*\]\[Next[^\]]*\]',
        r'\[Previous[^\]]*\]\([^)]*\)\[Next[^\]]*\]\([^)]*\)',
        r'PreviousNext',
        
        # Show more/less buttons
        r'Show more',
        r'Show less',
        r'Expand',
        r'Collapse',
        
        # Edit page links
        r'\[Edit this page[^\]]*\]\([^)]*\)',
        r'\[Edit on GitHub\]\([^)]*\)',
        r'\[View source\]\([^)]*\)',
        
        # Version badges
        r'Latest Version\s*\n\s*[\d.]+',
        
        # Feedback buttons
        r'Was this page helpful\?',
        r'\[Yes\]\([^)]*\)\s*\[No\]\([^)]*\)',
        
        # Algolia search widgets
        r'Search.*DocSearch',
        r'algolia-docsearch',
        
        # Cookie consent banners
        r'We use cookies',
        r'Cookie Policy',
        r'Accept cookies',
        r'Cookie consent',
        
        # TOC sidebars
        r'On this page',
        r'Table of Contents',
        r'\* \[Overview\]',
        
        # Breadcrumbs
        r'Home\s*>\s*[^\n]+',
        r'\[Home\]\([^)]*\)\s*>',
        
        # Version switchers
        r'Version:\s*\[\d+\.\d+\]',
        r'Select version',
    ]
    
    # Navigation menu patterns (at start of content)
    NAV_MENU_PATTERNS = [
        r'^Menu\s*\n',
        r'^Using App Router\s*\n',
        r'^Features available in /\w+\s*\n',
    ]
    
    # Duplicate header patterns
    DUPLICATE_HEADER_PATTERN = r'^(#{1,6})\s+(.+)\n\1\s+\2'
    
    def __init__(self, site_type: str = None):
        # Compile patterns for efficiency
        self.ui_patterns = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in self.UI_ARTIFACT_PATTERNS]
        self.nav_patterns = [re.compile(p, re.MULTILINE) for p in self.NAV_MENU_PATTERNS]
        self.site_type = site_type
        
        # Compile profile patterns if site_type specified
        if site_type and site_type in self.PROFILES:
            profile_patterns = self.PROFILES[site_type]['patterns']
            self.profile_patterns = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in profile_patterns]
        else:
            self.profile_patterns = []
    
    def clean(self, content: str) -> str:
        """Apply all cleaning operations to content."""
        content = self.fix_code_block_languages(content)
        content = self.remove_ui_artifacts(content)
        content = self.remove_navigation_menus(content)
        content = self.fix_duplicate_headers(content)
        content = self.fix_encoding_issues(content)
        content = self.remove_permalink_anchors(content)
        content = self.clean_empty_code_blocks(content)
        content = self.normalize_heading_levels(content)
        content = self.fix_markdown_tables(content)
        content = self.deduplicate_content(content)
        content = self.normalize_whitespace(content)
        return content
    
    def fix_code_block_languages(self, content: str) -> str:
        """Fix or remove bad code block language tags."""
        # First, apply CSS class to language mapping
        for css_class, language in self.CSS_CLASS_TO_LANGUAGE.items():
            content = content.replace(f'```{css_class}', f'```{language}')
        
        # Remove known bad language tags
        for bad_lang in self.BAD_LANGUAGES:
            content = content.replace(f'```{bad_lang}', '```')
        
        # Detect and fix common language mismatches using content heuristics
        content = self._auto_detect_code_language(content)
        
        # Clean up: normalize language tags to lowercase
        def normalize_lang_tag(match):
            lang = match.group(1).lower()
            # Map common variations
            lang_map = {
                'js': 'javascript',
                'py': 'python',
                'ts': 'typescript',
                'rs': 'rust',
                'bash': 'bash',
                'sh': 'bash',
                'shell': 'bash',
            }
            return f'```{lang_map.get(lang, lang)}'
        
        content = re.sub(r'```(\w+)', normalize_lang_tag, content)
        
        return content
    
    def _auto_detect_code_language(self, content: str) -> str:
        """Auto-detect code block languages based on content."""
        def detect_language(code: str) -> str:
            code_lower = code.lower().strip()
            
            # Go
            if any(x in code for x in ['func main()', 'package main', 'import (']):
                return 'go'
            
            # Rust
            if any(x in code for x in ['fn main()', 'let mut', 'impl ', 'use std::']):
                return 'rust'
            
            # YAML
            if ':' in code and any(x in code for x in ['apiVersion:', 'kind:', 'metadata:', 'spec:']):
                return 'yaml'
            
            # TOML
            if '[' in code and any(x in code for x in ['[package]', '[dependencies]', '[section]']):
                return 'toml'
            
            # JSX/React (strongest signal — must be first since 'import React' also matches Python's 'import ')
            if any(x in code for x in ['import React', 'useState', 'useEffect', 'export default function', 'const Component']):
                return 'jsx'
            
            # Python (must check BEFORE Dockerfile since 'from X import Y' triggers 'from ')
            if any(x in code for x in ['def ', 'class ', 'if __name__']):
                return 'python'
            if 'from ' in code and ' import ' in code:
                return 'python'
            if code_lower.startswith('import ') and not any(x in code for x in ['const ', 'let ', 'function ', '=>']):
                return 'python'
            
            # Shell/Bash (must check BEFORE Dockerfile since 'pip install', 'npm' etc.)
            if code_lower.startswith('$') or code_lower.startswith('npm ') or code_lower.startswith('yarn '):
                return 'bash'
            if any(x in code_lower for x in ['apt-get', 'brew install', 'pip install', 'curl ', 'wget ']):
                return 'bash'
            
            # TypeScript/JavaScript
            if any(x in code for x in ['interface ', 'type ', ': string', ': number', ': boolean']):
                return 'typescript'
            if any(x in code for x in ['const ', 'let ', 'function ', '=>', 'async ', 'await ']):
                return 'javascript'
            
            # Dockerfile (after Python/JS/Bash — require uppercase instruction OR multiple Dockerfile keywords)
            dockerfile_keywords = ['FROM ', 'RUN ', 'CMD ', 'ENTRYPOINT ', 'COPY ', 'ADD ', 'WORKDIR ', 'EXPOSE ', 'ENV ']
            dockerfile_hits = sum(1 for kw in dockerfile_keywords if kw in code)
            if dockerfile_hits >= 2:
                return 'dockerfile'
            
            # HTML/CSS
            if any(x in code for x in ['<div', '<span', '<p>', '<html', '<!DOCTYPE']):
                return 'html'
            if any(x in code for x in ['{', '}']) and any(x in code for x in ['color:', 'margin:', 'padding:', 'display:']):
                return 'css'
            
            # JSON
            if code.strip().startswith('{') and code.strip().endswith('}'):
                try:
                    import json
                    json.loads(code)
                    return 'json'
                except:
                    pass
            
            # SQL
            if any(x in code_lower for x in ['select ', 'insert ', 'update ', 'delete ', 'create table']):
                return 'sql'
            
            return ''  # Unknown
        
        # Find code blocks without language and try to detect
        pattern = r'```\n(.*?)```'
        
        def replace_with_language(match):
            code = match.group(1)
            lang = detect_language(code)
            if lang:
                return f'```{lang}\n{code}```'
            return match.group(0)
        
        content = re.sub(pattern, replace_with_language, content, flags=re.DOTALL)
        
        # Also check code blocks with potentially wrong language tags
        # (e.g., dockerfile tag but content is JavaScript)
        wrong_tag_pattern = r'```(\w+)\n(.*?)```'
        
        def fix_wrong_tag(match):
            declared_lang = match.group(1)
            code = match.group(2)
            detected = detect_language(code)
            
            # If detected language differs from declared, and we're confident
            if detected and detected != declared_lang:
                # Special case: dockerfile is often misused
                if declared_lang == 'dockerfile' and detected in ('javascript', 'jsx', 'typescript'):
                    return f'```{detected}\n{code}```'
                # If declared is a generic/wrong tag, use detected
                if declared_lang in ('dockerfile', 'text', 'plain'):
                    return f'```{detected}\n{code}```'
            
            return match.group(0)
        
        return re.sub(wrong_tag_pattern, fix_wrong_tag, content, flags=re.DOTALL)
    
    def remove_ui_artifacts(self, content: str) -> str:
        """Remove known UI artifacts from content."""
        # Apply universal patterns
        for pattern in self.ui_patterns:
            content = pattern.sub('', content)
        
        # Apply profile-specific patterns
        for pattern in self.profile_patterns:
            content = pattern.sub('', content)
        
        return content
    
    def remove_navigation_menus(self, content: str) -> str:
        """Remove navigation menu blocks from start of content."""
        # Check for navigation at start
        for pattern in self.nav_patterns:
            if pattern.match(content):
                # Find the end of navigation (usually marked by ---)
                lines = content.split('\n')
                nav_end = 0
                in_nav = True
                bullet_count = 0
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('* ') or line.strip().startswith('+ ') or line.strip().startswith('- '):
                        bullet_count += 1
                    elif line.strip() == '---' and bullet_count > 5:
                        nav_end = i + 1
                        break
                    elif line.strip().startswith('#') and bullet_count > 5:
                        nav_end = i
                        break
                
                if nav_end > 0:
                    content = '\n'.join(lines[nav_end:])
                break
        
        return content
    
    def fix_duplicate_headers(self, content: str) -> str:
        """Remove duplicate consecutive headers."""
        # Pattern: same header appearing twice in a row
        lines = content.split('\n')
        result = []
        prev_line = ''
        
        for line in lines:
            # Check if this is a header
            if line.strip().startswith('#'):
                # Normalize for comparison
                normalized = re.sub(r'^#+\s*', '', line.strip()).lower()
                prev_normalized = re.sub(r'^#+\s*', '', prev_line.strip()).lower()
                
                if normalized == prev_normalized and normalized:
                    continue  # Skip duplicate
            
            result.append(line)
            prev_line = line
        
        return '\n'.join(result)
    
    def fix_encoding_issues(self, content: str) -> str:
        """Fix common encoding issues including mojibake patterns."""
        # Mojibake patterns (UTF-8 interpreted as Latin-1)
        mojibake_fixes = [
            ('Ã©', 'é'),  # e with acute
            ('Ã¨', 'è'),  # e with grave
            ('Ãª', 'ê'),  # e with circumflex
            ('Ã«', 'ë'),  # e with diaeresis
            ('Ã ', 'à'),  # a with grave
            ('Ã¡', 'á'),  # a with acute
            ('Ã¢', 'â'),  # a with circumflex
            ('Ã£', 'ã'),  # a with tilde
            ('Ã¤', 'ä'),  # a with diaeresis
            ('Ã¥', 'å'),  # a with ring
            ('Ã¬', 'ì'),  # i with grave
            ('Ã ', 'í'),  # i with acute (duplicate, keep first)
            ('Ã®', 'î'),  # i with circumflex
            ('Ã¯', 'ï'),  # i with diaeresis
            ('Ã²', 'ò'),  # o with grave
            ('Ã³', 'ó'),  # o with acute
            ('Ã´', 'ô'),  # o with circumflex
            ('Ãµ', 'õ'),  # o with tilde
            ('Ã¶', 'ö'),  # o with diaeresis
            ('Ã¹', 'ù'),  # u with grave
            ('Ãº', 'ú'),  # u with acute
            ('Ã»', 'û'),  # u with circumflex
            ('Ã¼', 'ü'),  # u with diaeresis
            ('Ã½', 'ý'),  # y with acute
            ('Ã¿', 'ÿ'),  # y with diaeresis
            ('Ã§', 'ç'),  # c with cedilla
            ('Ã±', 'ñ'),  # n with tilde
            ('Ã', 'ß'),  # sharp s
            ('Ã', 'Ä'),  # A with diaeresis
            ('Ã', 'Ö'),  # O with diaeresis
            ('Ã', 'Ü'),  # U with diaeresis
        ]
        
        for old, new in mojibake_fixes:
            content = content.replace(old, new)
        
        # Smart quotes and apostrophes
        replacements = [
            ('â', "'"),  # Common UTF-8 encoding issue
            ('â', '"'),
            ('â', '"'),
            ('â', '-'),
            ('â¦', '...'),
            ('\u2019', "'"),  # Right single quote
            ('\u2018', "'"),  # Left single quote
            ('\u201c', '"'),  # Left double quote
            ('\u201d', '"'),  # Right double quote
            ('\u2013', '-'),  # En dash
            ('\u2014', '--'),  # Em dash
            ('\u2026', '...'),  # Ellipsis
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        return content
    
    def clean_empty_code_blocks(self, content: str) -> str:
        """Remove empty or near-empty code blocks."""
        # Remove code blocks with only whitespace
        content = re.sub(r'```\w*\n\s*\n```', '', content)
        content = re.sub(r'```\w*\n```', '', content)
        return content
    
    def normalize_heading_levels(self, content: str) -> str:
        """Normalize heading hierarchy: ensure no level skipping, first heading is # or ##."""
        lines = content.split('\n')
        result = []
        first_heading_level = None
        prev_level = 0
        
        for line in lines:
            # Match heading lines
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                hashes, text = match.groups()
                level = len(hashes)
                
                # Track first heading level
                if first_heading_level is None:
                    first_heading_level = level
                    # Normalize first heading to 1 or 2
                    if level > 2:
                        level = 2
                        hashes = '#' * level
                else:
                    # Ensure no skipping (max +1 level jump)
                    if level > prev_level + 1:
                        level = prev_level + 1
                        hashes = '#' * level
                    # Prevent flat headings (all same level)
                    if level == prev_level and prev_level >= 2:
                        # Allow slight variation for subsections
                        pass
                
                prev_level = level
                result.append(f"{hashes} {text}")
            else:
                result.append(line)
        
        return '\n'.join(result)

    def normalize_whitespace(self, content: str) -> str:
        """Normalize excessive whitespace."""
        # Remove more than 2 consecutive blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in content.split('\n')]
        content = '\n'.join(lines)
        
        return content.strip()
    
    def fix_markdown_tables(self, content: str) -> str:
        """Fix broken markdown tables (add missing separator row)."""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            # Detect table header row (contains | separators but not ---)
            if '|' in line and not re.search(r'\|?\s*:?-+:?\s*\|', line) and not line.strip().startswith('```'):
                # Check if next line is a separator
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if '|' in next_line and re.search(r'\|?\s*:?-+:?\s*\|', next_line):
                        # Valid table, proceed
                        result.append(line)
                    else:
                        # Missing separator, generate one
                        result.append(line)
                        # Count columns from header
                        col_count = line.count('|') + 1 if not line.strip().startswith('|') else line.count('|')
                        separator = '|' + ' --- |' * col_count
                        if col_count > 0:
                            result.append(separator)
                else:
                    result.append(line)
            else:
                result.append(line)
            i += 1
        
        return '\n'.join(result)
    
    def deduplicate_content(self, content: str) -> str:
        """Remove duplicate paragraphs and code blocks."""
        lines = content.split('\n')
        seen_blocks = set()
        result = []
        current_block = []
        
        def flush_block():
            if not current_block:
                return
            block_text = '\n'.join(current_block).strip()
            if block_text:
                # Simple dedup: skip exact duplicates of paragraphs >50 chars
                if len(block_text) > 50 and block_text in seen_blocks:
                    pass
                else:
                    seen_blocks.add(block_text)
                    result.extend(current_block)
            current_block.clear()
        
        for line in lines:
            # Check if line starts a new block (heading, code block, empty line)
            if line.strip().startswith('#') or line.strip().startswith('```') or line.strip() == '':
                flush_block()
                current_block.append(line)
                if line.strip().startswith('```') or line.strip() == '':
                    flush_block()
            else:
                current_block.append(line)
        
        flush_block()
        return '\n'.join(result)

    def remove_permalink_anchors(self, content: str) -> str:
        """Remove permalink anchor markers from markdown headings.
        
        Handles:
        - Trailing ¶ character: '## Security¶' → '## Security'
        - Permalink links: '## Security[¶](#anchor)' → '## Security'
        - Empty anchor links: '## Security[](#anchor)' → '## Security'
        """
        lines = content.split('\n')
        result = []
        
        for line in lines:
            # Only process heading lines
            if line.strip().startswith('#'):
                # Pattern 1: Remove trailing ¶ character (U+00B6)
                line = re.sub(r'¶\s*$', '', line)
                
                # Pattern 2: Remove [¶](#anchor "...") permalink links
                line = re.sub(r'\[¶\]\(#[^)]*"[^"]*"\)', '', line)
                line = re.sub(r'\[¶\]\(#[^)]*\)', '', line)
                
                # Pattern 3: Remove []( #anchor) empty anchor links  
                line = re.sub(r'\[\]\(\s*#[^)]*\)', '', line)
                
                # Clean up any trailing whitespace
                line = line.rstrip()
            
            result.append(line)
        
        return '\n'.join(result)


# Convenience function
def clean_content(content: str) -> str:
    """Clean scraped markdown content."""
    cleaner = ContentCleaner()
    return cleaner.clean(content)
