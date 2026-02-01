# System Architecture

## Overview

AnyDocsMCP is a two-phase system that converts documentation websites into searchable, LLM-accessible knowledge bases.

```
┌─────────────────┐
│  Documentation  │
│     Website     │
└────────┬────────┘
         │
         │ Phase 1: Scraping
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Site Analyzer  │◄─────┤  LLM (Claude)    │
│  (LLM-assisted) │      │  via OpenRouter  │
└────────┬────────┘      └──────────────────┘
         │
         │ Extraction Rules
         ▼
┌─────────────────┐
│ Scraper Engine  │
│ (BeautifulSoup) │
└────────┬────────┘
         │
         │ Structured Markdown
         ▼
┌─────────────────┐
│ Storage Manager │
│  (Versioned)    │
└────────┬────────┘
         │
         │ Markdown Files
         ▼
┌─────────────────┐
│   %APPDATA%/    │
│  AnyDocsMCP/    │
│     docs/       │
└────────┬────────┘
         │
         │ Phase 2: MCP Serving
         ▼
┌─────────────────┐
│ Markdown Parser │
│   (Indexing)    │
└────────┬────────┘
         │
         │ Section Index
         ▼
┌─────────────────┐      ┌──────────────────┐
│   MCP Server    │◄─────┤ Windsurf/Claude  │
│   (Node.js)     │      │    Desktop       │
└────────┬────────┘      └──────────────────┘
         │
         │ Search Results
         ▼
    AI Assistant
```

## Components

### 1. Site Analyzer (`site_analyzer.py`)

**Purpose:** Use LLM to understand documentation site structure

**Process:**
1. Fetch sample HTML from the documentation site
2. Clean and truncate HTML (remove scripts, styles)
3. Send to Claude via OpenRouter with analysis prompt
4. LLM identifies:
   - Content container selectors (where docs are)
   - Navigation selectors (where links are)
   - Elements to exclude (headers, footers, etc.)
   - URL patterns (what URLs are valid docs)
   - Grouping strategy (how to organize files)
5. Return `SiteAnalysis` object with extraction rules

**Key Innovation:** Eliminates need for manual selector configuration for each site

### 2. Scraper Engine (`scraper_engine.py`)

**Purpose:** Extract and convert documentation pages

**Process:**
1. Use navigation selectors to find all doc links
2. For each page:
   - Fetch HTML
   - Apply content selectors to extract main content
   - Remove excluded elements (nav, footer, etc.)
   - Convert HTML to Markdown (via markdownify)
   - Extract metadata (title, source URL)
   - Determine group/file based on URL path
3. Write pages to grouped Markdown files
4. Maintain document structure and hierarchy

**Output Format:**
```markdown
# Category Name

*Documentation: Project Name*

---

## Page Title

**Source:** https://docs.example.com/page

[Content here with code blocks preserved]

---

## Another Page

...
```

### 3. Storage Manager (`storage.py`)

**Purpose:** Manage documentation storage with versioning

**Directory Structure:**
```
%APPDATA%\AnyDocsMCP\docs\
├── project-name/
│   ├── config.json          # Extraction configuration
│   ├── metadata.json        # Statistics and info
│   ├── v1/                  # First scrape
│   │   ├── getting-started.md
│   │   ├── api-reference.md
│   │   └── guides-advanced.md
│   ├── v2/                  # After update
│   │   └── ...
│   └── v3/                  # Latest version
│       └── ...
```

**Versioning:**
- Each scrape creates new version (v1, v2, v3...)
- Old versions preserved for comparison
- MCP server automatically uses latest version

### 4. Markdown Parser (`markdown-parser.ts`)

**Purpose:** Parse Markdown files and build searchable index

**Data Model:**
```typescript
Section {
  id: string              // Unique identifier
  file: string            // Source file name
  title: string           // Section heading
  level: number           // Heading level (1-6)
  path: string[]          // Hierarchical path
  content: string         // Text content (cleaned)
  codeBlocks: CodeBlock[] // Extracted code snippets
  sourceUrl?: string      // Original doc URL
  children: Section[]     // Nested sections
}
```

**Index Building:**
1. Read all .md files in version directory
2. Parse each file:
   - Split by headings (# ## ### etc.)
   - Build hierarchical structure
   - Extract code blocks separately
   - Preserve source URLs
3. Flatten hierarchy for searching
4. Generate table of contents per file

**Search Algorithm:**
- Tokenize query into terms
- Score each section by:
  - Exact title match: +100
  - Title contains query: +50
  - Path contains query: +30
  - Term frequency in content: +2 per match (max 20)
  - Code block matches: +15 per term
- Sort by score, return top N results

### 5. MCP Server (`index.ts`)

**Purpose:** Expose documentation via Model Context Protocol

**Tools Provided:**

| Tool | Purpose | Key Parameters |
|------|---------|---------------|
| `search` | Full-text search | query, maxResults, fileFilter |
| `get_overview` | High-level structure | none |
| `list_files` | List all files | none |
| `get_file_toc` | File TOC | fileName |
| `get_section` | Specific section | title, fileName |
| `find_code_examples` | Code search | query, language |

**Configuration:**
- `activeDocs`: Which documentation to serve
- `storageRoot`: Custom storage location (optional)
- `serverName`: MCP server identifier

**Multi-Doc Support:**
- Run multiple server instances with different `activeDocs`
- Each serves different documentation set
- Can run simultaneously in same IDE

## Data Flow

### Scraping Flow

```
User runs CLI
    ↓
CLI → Site Analyzer
    ↓
Site Analyzer → OpenRouter API (Claude)
    ↓
Claude analyzes HTML → Returns selectors
    ↓
CLI → Storage Manager (create version)
    ↓
CLI → Scraper Engine
    ↓
Scraper Engine → Website (fetch pages)
    ↓
Scraper Engine → BeautifulSoup (parse)
    ↓
Scraper Engine → Markdownify (convert)
    ↓
Scraper Engine → Storage Manager (write files)
    ↓
Storage Manager → Disk (%APPDATA%/AnyDocsMCP/docs/)
```

### MCP Query Flow

```
AI Assistant (Windsurf/Claude)
    ↓
MCP Protocol Request
    ↓
MCP Server → Config (load settings)
    ↓
MCP Server → Markdown Parser (build index if needed)
    ↓
Markdown Parser → Disk (read .md files)
    ↓
Markdown Parser → Index (in-memory)
    ↓
MCP Server → Tool Handler (search/get_section/etc)
    ↓
Tool Handler → Index (query)
    ↓
Tool Handler → Format Results
    ↓
MCP Protocol Response
    ↓
AI Assistant (use in response)
```

## Key Design Decisions

### 1. LLM-Assisted Configuration

**Why:** Every documentation site is different. Manual configuration would require:
- Inspecting HTML for each site
- Trial and error with selectors
- Understanding site-specific patterns

**How:** Claude analyzes sample pages and generates extraction rules automatically.

**Trade-offs:**
- ✅ Works with most documentation sites out-of-box
- ✅ Saves significant setup time
- ❌ Requires API key and costs ~$0.01 per site
- ❌ May fail on very unusual site structures

### 2. Markdown as Storage Format

**Why:**
- Human-readable (can verify/edit manually)
- Preserves structure (headings, code blocks)
- Compact (smaller than HTML)
- Easy to parse (regex/simple parsing)
- Portable (move between systems)

**Alternative Considered:** Database (SQLite)
- Would be faster to query
- But harder to inspect/debug
- And requires migrations for schema changes

### 3. Grouped Files (Not Single File or Page-Per-File)

**Why:**
- Single file: Too large for LLMs (>100K tokens)
- Page-per-file: Too many files (>500 for large docs)
- Grouped: Balance (10-50 files, 1-10K tokens each)

**Strategy:** Group by URL path depth
- `path_depth_2`: `/guides/getting-started` → `guides.md`
- `path_depth_3`: `/guides/advanced/hooks` → `guides-advanced.md`

### 4. Versioning

**Why:**
- Documentation changes over time
- May want to compare versions
- Safe to re-scrape without losing old data

**How:**
- Each scrape creates new version (v1, v2, v3...)
- MCP server uses latest automatically
- Old versions retained (can be manually deleted if needed)

### 5. Separate Scraper (Python) and Server (TypeScript)

**Why:**
- Scraping: Python ecosystem better (BeautifulSoup, requests)
- MCP: Node.js required (MCP SDK only in JS/TS)
- Separation of concerns (scrape once, serve many times)

**Trade-offs:**
- ✅ Best tools for each job
- ✅ Can update server without re-scraping
- ❌ Two dependency sets to maintain
- ❌ Two languages to understand

## Extension Points

### Adding New Scraping Strategies

1. Add to `models.py`:
   ```python
   grouping_strategy: Literal["path_depth_2", "path_depth_3", "single_file", "by_category"]
   ```

2. Implement in `scraper_engine.py`:
   ```python
   def get_url_group(self, url: str) -> str:
       if strategy == "by_category":
           # Custom logic
   ```

### Adding New MCP Tools

1. Add tool definition in `index.ts`:
   ```typescript
   {
     name: 'new_tool',
     description: '...',
     inputSchema: { ... }
   }
   ```

2. Add handler in CallToolRequestSchema:
   ```typescript
   case 'new_tool': {
     // Implementation
   }
   ```

### Supporting Non-HTML Documentation

Currently supports HTML documentation sites. Could extend to:

- **PDF documentation**: Add PDF parser before Markdown conversion
- **GitHub Markdown**: Direct Markdown-to-Markdown (skip HTML step)
- **API specs (OpenAPI/Swagger)**: Custom parser for API docs

## Performance Characteristics

### Scraping

- **Time:** O(n) where n = number of pages
  - ~0.2s per page (network + parsing)
  - Typical docs: 2-10 minutes
  - Large docs (500+ pages): 15-30 minutes

- **Space:** ~10-20KB per page in Markdown
  - 100 pages → 1-2 MB
  - 500 pages → 5-10 MB

### MCP Server

- **Index build:** O(n) where n = total sections
  - Typical: 1-5 seconds on startup
  - Cached in memory afterward

- **Search:** O(n) linear scan with early termination
  - Typical: <100ms for 1000s of sections
  - Could optimize with inverted index if needed

- **Memory:** ~1-5 MB per 100 pages indexed

## Security Considerations

1. **API Key Storage**
   - Stored in environment variable
   - Not in config files
   - Not committed to git

2. **Web Scraping**
   - Respects robots.txt (user should verify)
   - Rate limiting via delay between requests
   - Only scrapes public documentation

3. **MCP Server**
   - Runs locally (stdio transport)
   - No network exposure
   - Reads only from designated docs directory

## Future Improvements

### Short Term
- Add progress bars for scraping
- Better error recovery (retry failed pages)
- Validation step (verify scraped content)
- Diff tool (compare versions)

### Medium Term
- Support for authentication (private docs)
- Incremental updates (only changed pages)
- Multi-language support (i18n docs)
- Custom extractors for common frameworks

### Long Term
- GUI for configuration
- Automatic scheduling (keep docs fresh)
- Collaborative sharing (doc corpus library)
- Advanced search (semantic, not just keyword)
