# Docs Api Reference

*Documentation: E2E Test Documentation*

---

## API Reference

**Source:** http://127.0.0.1:55271/docs/api-reference

# API Reference
Complete reference for all available API endpoints and data models.
## Search Endpoint
Search across indexed documentation using natural language queries.
```jsx
GET /api/v1/search?q=useState&maxResults=10
# Response:
{
  "results": [
    {"title": "Using State", "score": 0.95, "file": "hooks.md"},
    {"title": "State Management", "score": 0.82, "file": "patterns.md"}
  ],
  "total": 2,
  "query_time_ms": 12
}
```
## Index Management
Rebuild the search index after adding or updating documentation files.
```dockerfile
from anydocs import IndexManager
manager = IndexManager(docs_path="./docs")
result = manager.rebuild_index()
print(f"Indexed {result.total_sections} sections from {result.total_files} files")
print(f"Build time: {result.build_time_ms}ms")
```
## Data Models
### Section
Represents a single documentation section parsed from markdown files.
```typescript
interface Section {
  id: string;          // Unique section identifier
  file: string;        // Source file name
  title: string;       // Section heading
  level: number;       // Heading level (1-6)
  path: string[];      // Parent heading hierarchy
  content: string;     // Section text content
  codeBlocks: CodeBlock[];
  sourceUrl?: string;  // Original documentation URL
}
interface CodeBlock {
  language: string;    // Programming language
  code: string;        // Code content
}
```
### DocumentIndex
The complete search index containing all parsed sections.
```typescript
interface DocumentIndex {
  files: Map<string, Section[]>;
  allSections: Section[];
  tocByFile: Map<string, string>;
}
```
## Rate Limiting
The API enforces rate limits to ensure fair usage:
* **Search:** 100 requests per minute
* **Index rebuild:** 5 requests per hour
* **File operations:** 50 requests per minute
Rate limit headers are included in every response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 97
X-RateLimit-Reset: 1706900400
```

---

