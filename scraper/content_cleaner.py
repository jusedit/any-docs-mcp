"""Content cleaner for post-processing scraped markdown.

Removes UI artifacts, fixes code blocks, encoding issues, and normalizes output.
Adapted from scraper v1 with improvements.
"""
import re
from typing import Dict, List


BAD_LANGUAGES = [
    "sp-pre-placeholder", "shiki", "index-module__DOXIJG__content",
    "language-undefined", "highlight", "code-block",
]

CSS_CLASS_TO_LANGUAGE = {
    "language-js": "javascript", "language-javascript": "javascript",
    "language-jsx": "jsx", "language-ts": "typescript",
    "language-typescript": "typescript", "language-tsx": "tsx",
    "language-py": "python", "language-python": "python",
    "language-python3": "python", "highlight-python": "python",
    "language-sh": "bash", "language-shell": "bash",
    "language-bash": "bash", "language-zsh": "bash",
    "language-console": "bash", "language-terminal": "bash",
    "language-html": "html", "language-xml": "xml",
    "language-css": "css", "language-scss": "scss",
    "language-json": "json", "language-yaml": "yaml",
    "language-yml": "yaml", "language-toml": "toml",
    "language-md": "markdown", "language-markdown": "markdown",
    "language-rs": "rust", "language-rust": "rust",
    "language-go": "go", "language-golang": "go",
    "language-c": "c", "language-cpp": "cpp", "language-c++": "cpp",
    "language-java": "java", "language-kt": "kotlin",
    "language-kotlin": "kotlin", "language-swift": "swift",
    "language-vue": "vue", "language-svelte": "svelte",
    "language-astro": "astro", "language-dockerfile": "dockerfile",
    "language-docker": "dockerfile", "language-sql": "sql",
    "language-graphql": "graphql", "language-diff": "diff",
}

UI_ARTIFACT_PATTERNS = [
    r"ReloadClear\[Fork\]\([^)]*\)",
    r"\[Fork\]\(https://codesandbox\.io[^)]*\)",
    r"\[Open in CodeSandbox\]\([^)]*\)",
    r"\[Open in StackBlitz\]\([^)]*\)",
    r"\[Try it\]\([^)]*\)",
    r"Copy to clipboard", r"Copy code", r"Copied!",
    r"TypeScriptCopy to clipboard", r"JavaScriptCopy to clipboard",
    r"ShellCopy to clipboard", r"BashCopy to clipboard",
    r"\[Previous[^\]]*\]\[Next[^\]]*\]",
    r"\[Previous[^\]]*\]\([^)]*\)\[Next[^\]]*\]\([^)]*\)",
    r"PreviousNext",
    r"Show more", r"Show less", r"Expand", r"Collapse",
    r"\[Edit this page[^\]]*\]\([^)]*\)",
    r"\[Edit on GitHub\]\([^)]*\)",
    r"\[View source\]\([^)]*\)",
    r"Was this page helpful\?",
    r"Was this helpful\?",
    r"\[Yes\]\([^)]*\)\s*\[No\]\([^)]*\)",
    r"We use cookies", r"Cookie Policy", r"Accept cookies", r"Cookie consent",
    r"Accept all cookies?", r"Manage cookies",
    r"On this page", r"Table of Contents",
    r"Skip to [Mm]ain [Cc]ontent", r"Skip to content",
    r"Report an issue", r"\[Report an issue\]\([^)]*\)",
    r"Give feedback", r"Send feedback",
    r"Subscribe\.?$", r"Newsletter\.?$",
    r"Sign in\.?$", r"Log in\.?$", r"Sign up\.?$",
    r"Download this Manual",
    r"Copyright ©.*$", r"Copyright Â©.*$",
    r"MIT License\.?$",
    r"^supported\.$", r"^Send$",
    r"Home\s*>\s*[^\n]+", r"\[Home\]\([^)]*\)\s*>",
    r"Version:\s*\[\d+\.\d+\]", r"Select version",
    r"Copy as Markdown", r"Open Markdown",
    r"Ask Docs AI", r"Open in Claude",
    r"`⌘K``Ctrl K`", r"`⌘K`", r"`Ctrl K`",
    r"^\d{2}\s*$",
    r"^Back$",
    r"^Terminal$",
    r"^\[Docs\]\([^)]*\)\[Blog\]\([^)]*\).*$",
    r"^v\d+\.\d+\s*$",
    r"^\[« Back to all guides\]\([^)]*\)",
    r"^\d+\s+minutes?\s*$",
    r"^\[\d+\]\([^)]*\)\s*$",
    r"^\[Â« Back[^\]]*\]\([^)]*\)",
    r"^Menu$",
    r"^\[.+ on X\]\([^)]*\)\[.+ on .+\]\([^)]*\).*$",
    r"\[\]\([^)]*\)",
    r"^\s*or\s*$",
]

MOJIBAKE_FIXES = [
    ("\u00c3\u00a9", "\u00e9"), ("\u00c3\u00a8", "\u00e8"),
    ("\u00c3\u00aa", "\u00ea"), ("\u00c3\u00ab", "\u00eb"),
    ("\u00c3\u00a0", "\u00e0"), ("\u00c3\u00a1", "\u00e1"),
    ("\u00c3\u00a2", "\u00e2"), ("\u00c3\u00a3", "\u00e3"),
    ("\u00c3\u00a4", "\u00e4"), ("\u00c3\u00a5", "\u00e5"),
    ("\u00c3\u00a7", "\u00e7"), ("\u00c3\u00b1", "\u00f1"),
    ("\u00c3\u00b6", "\u00f6"), ("\u00c3\u00bc", "\u00fc"),
    ("Â©", "©"), ("Â®", "®"), ("Â»", "»"), ("Â«", "«"),
]

MOJIBAKE_EMOJI_RE = re.compile(
    r"[\xc3\xc2][\x80-\xbf][\xc2-\xc3]?[\x80-\xbf]?"
    r"|ðŸ[^\s]{0,8}"
    r"|â[^\s]{0,4}"
    r"|Ã[^\s]{0,2}"
)

SMART_QUOTE_FIXES = [
    ("\u2019", "'"), ("\u2018", "'"),
    ("\u201c", '"'), ("\u201d", '"'),
    ("\u2013", "-"), ("\u2014", "--"),
    ("\u2026", "..."),
]


class ContentCleaner:
    def __init__(self):
        self._ui_patterns = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in UI_ARTIFACT_PATTERNS]

    def clean(self, content: str) -> str:
        content = self._strip_nav_header(content)
        content = self._fix_duplicate_headers(content)
        content = self._remove_permalink_anchors(content)
        content = self._strip_toc_after_heading(content)
        content = self._fix_code_block_languages(content)
        content = self._remove_ui_artifacts(content)
        content = self._fix_encoding(content)
        content = self._strip_footer(content)
        content = self._clean_empty_code_blocks(content)
        content = self._deduplicate_content(content)
        content = self._normalize_whitespace(content)
        return content

    # ------------------------------------------------------------------

    def _strip_nav_header(self, content: str) -> str:
        """Remove navigation/header residue before the first real heading.

        Many sites leak nav bar, keyboard shortcuts, breadcrumbs, and
        section indicators into the main content. This strips everything
        before the first markdown heading (# ...) that looks like nav residue.
        """
        lines = content.split("\n")
        first_heading_idx = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("# ") and not stripped.startswith("##"):
                first_heading_idx = i
                break

        if first_heading_idx is None or first_heading_idx < 2:
            return content

        # Check if lines before the heading look like nav residue
        pre_heading = lines[:first_heading_idx]
        nav_signals = 0
        for line in pre_heading:
            s = line.strip()
            if not s:
                continue
            # Nav-like patterns
            if re.match(r"^\d+\.\s+\w", s):  # "1. Getting Started"
                nav_signals += 1
            elif re.match(r"^`[^`]+`\[", s):  # "`⌘K`[Docs]..."
                nav_signals += 1
            elif re.match(r"^\[.+\]\(.+\)\[.+\]\(.+\)", s):  # "[Docs](/docs)[Blog](/blog)"
                nav_signals += 1
            elif re.match(r"^\[.+\]\(https?://[^)]+\)$", s):  # standalone link
                nav_signals += 1
            elif re.match(r"^v\d+\.\d+", s):  # "v4.1"
                nav_signals += 1
            elif s in ("Back", "Claude", "Light", "Dark", "/"):  # single-word UI
                nav_signals += 1
            elif re.match(r"^\d+\s+minutes?$", s):
                nav_signals += 1
            elif s == "/" or s == ">":  # breadcrumb separators
                nav_signals += 1

        # If most pre-heading lines look like nav, strip them
        non_empty = sum(1 for l in pre_heading if l.strip())
        if non_empty > 0 and nav_signals / non_empty >= 0.3:
            return "\n".join(lines[first_heading_idx:])

        return content

    def _strip_toc_after_heading(self, content: str) -> str:
        """Remove TOC-like bullet lists right after the first H1 heading.

        Pattern: # Heading\\n(optional single word like 'Claude')\\n* [Link](#anchor)\\n...
        These are 'on this page' TOCs that leak into content.
        """
        lines = content.split("\n")
        h1_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("# ") and not line.strip().startswith("##"):
                h1_idx = i
                break

        if h1_idx is None:
            return content

        # Scan lines after H1 for TOC pattern
        toc_start = None
        toc_end = None
        i = h1_idx + 1

        # Skip blank lines and single-word lines (like "Claude")
        while i < len(lines):
            s = lines[i].strip()
            if not s or (len(s.split()) <= 1 and not s.startswith("#") and not s.startswith("```")):
                i += 1
                continue
            break

        # Check if we hit a TOC-like bullet list
        if i < len(lines) and re.match(r"^[\*\-\+]\s+\[.+\]\(#", lines[i].strip()):
            toc_start = h1_idx + 1
            # Find end of TOC block
            while i < len(lines):
                s = lines[i].strip()
                if re.match(r"^[\*\-\+]\s+\[.+\]\(#", s):
                    i += 1
                elif s == "" or s.startswith("---"):
                    i += 1
                    # Skip trailing separator
                    if s.startswith("---"):
                        toc_end = i
                        break
                else:
                    break
            if toc_end is None:
                toc_end = i

            # Remove the TOC block
            return "\n".join(lines[:h1_idx + 1] + lines[toc_end:])

        return content

    def _fix_code_block_languages(self, content: str) -> str:
        for css_class, lang in CSS_CLASS_TO_LANGUAGE.items():
            content = content.replace(f"```{css_class}", f"```{lang}")
        for bad in BAD_LANGUAGES:
            content = content.replace(f"```{bad}", "```")

        def normalize_tag(m):
            lang = m.group(1).lower()
            lang_map = {"js": "javascript", "py": "python", "ts": "typescript",
                        "rs": "rust", "sh": "bash", "shell": "bash"}
            return f"```{lang_map.get(lang, lang)}"

        content = re.sub(r"```(\w+)", normalize_tag, content)
        return content

    def _remove_ui_artifacts(self, content: str) -> str:
        for pat in self._ui_patterns:
            content = pat.sub("", content)
        return content

    def _fix_encoding(self, content: str) -> str:
        for old, new in MOJIBAKE_FIXES:
            content = content.replace(old, new)
        for old, new in SMART_QUOTE_FIXES:
            content = content.replace(old, new)
        content = MOJIBAKE_EMOJI_RE.sub("", content)
        return content

    def _strip_footer(self, content: str) -> str:
        """Remove footer residue from the end of content.

        Detects common footer patterns: social links, copyright notices,
        feedback widgets, newsletter signups, and strips them.
        """
        lines = content.split("\n")
        if len(lines) < 5:
            return content

        footer_patterns = [
            re.compile(r"copyright", re.IGNORECASE),
            re.compile(r"MIT License", re.IGNORECASE),
            re.compile(r"^\[.+ on (X|GitHub|Discord|Twitter|BlueSky|LinkedIn)\]", re.IGNORECASE),
            re.compile(r"^(Was this helpful|Give feedback|Send feedback)", re.IGNORECASE),
            re.compile(r"^(Subscribe|Newsletter|Sign up for)", re.IGNORECASE),
            re.compile(r"^Menu$"),
            re.compile(r"^supported\.$"),
            re.compile(r"^Send$"),
        ]

        # Scan from the end, count consecutive footer-like lines
        cut_idx = len(lines)
        blank_run = 0
        for i in range(len(lines) - 1, max(len(lines) - 30, 0), -1):
            s = lines[i].strip()
            if not s:
                blank_run += 1
                continue
            is_footer = any(p.search(s) for p in footer_patterns)
            if is_footer:
                cut_idx = i
                blank_run = 0
            elif blank_run <= 2 and cut_idx < len(lines):
                # Allow up to 2 blank lines between footer fragments
                continue
            else:
                break

        if cut_idx < len(lines):
            return "\n".join(lines[:cut_idx])
        return content

    def _remove_permalink_anchors(self, content: str) -> str:
        lines = content.split("\n")
        result = []
        for line in lines:
            if line.strip().startswith("#"):
                line = re.sub(r"\u00b6\s*$", "", line)
                line = re.sub(r"\[\u00b6\]\(#[^)]*\)", "", line)
                line = re.sub(r"\[\]\(\s*#[^)]*\)", "", line)
                # Convert ## [Text](#anchor) → ## Text (keep heading text)
                line = re.sub(r"(#+\s*)\[([^\]]+)\]\(#[^)]*\)", r"\1\2", line)
                line = line.rstrip()
            result.append(line)
        # Remove empty headings (## with no text)
        result = [l for l in result if not re.match(r"^#{1,6}\s*$", l.strip())]
        return "\n".join(result)

    def _clean_empty_code_blocks(self, content: str) -> str:
        content = re.sub(r"```\w*\n\s*\n```", "", content)
        content = re.sub(r"```\w*\n```", "", content)
        return content

    def _fix_duplicate_headers(self, content: str) -> str:
        lines = content.split("\n")
        result = []
        seen_headings: Dict[str, str] = {}  # level+norm → first occurrence
        for line in lines:
            if line.strip().startswith("#"):
                m = re.match(r"^(#+)\s*(.*)", line.strip())
                if m:
                    level = m.group(1)
                    norm = m.group(2).strip().lower()
                    key = f"{level}:{norm}"
                    if norm and key in seen_headings:
                        continue
                    if norm:
                        seen_headings[key] = line
            result.append(line)
        return "\n".join(result)

    def _deduplicate_content(self, content: str) -> str:
        lines = content.split("\n")
        seen: set = set()
        result: List[str] = []
        block: List[str] = []

        def flush():
            if not block:
                return
            text = "\n".join(block).strip()
            if text and (len(text) <= 50 or text not in seen):
                seen.add(text)
                result.extend(block)
            block.clear()

        for line in lines:
            if line.strip().startswith("#") or line.strip().startswith("```") or line.strip() == "":
                flush()
                block.append(line)
                if line.strip().startswith("```") or line.strip() == "":
                    flush()
            else:
                block.append(line)
        flush()
        return "\n".join(result)

    def _normalize_whitespace(self, content: str) -> str:
        content = re.sub(r"\n{4,}", "\n\n\n", content)
        lines = [line.rstrip() for line in content.split("\n")]
        return "\n".join(lines).strip()
