# Contributing to AnyDocsMCP

## How to Contribute

### Reporting Issues

If you encounter a documentation site that doesn't work:

1. Create an issue with:
   - Site URL
   - Error message
   - Generated config.json (if created)
   - Sample of the HTML structure

### Adding Site-Specific Extractors

For common documentation frameworks, you can add pre-configured extractors:

1. Create file `scraper/extractors/<framework>.py`
2. Define extractor class:
   ```python
   class VitePressExtractor:
       @staticmethod
       def detect(url: str, html: str) -> bool:
           # Return True if this is a VitePress site
           pass
       
       @staticmethod
       def get_analysis() -> SiteAnalysis:
           # Return pre-configured selectors
           pass
   ```

3. Register in `site_analyzer.py`

### Improving LLM Analysis Prompts

The prompt in `site_analyzer.py` can be improved for better accuracy.

Guidelines:
- Be specific about what to look for
- Provide examples of good selectors
- Include common patterns to avoid

### Adding New MCP Tools

To add new search/retrieval capabilities:

1. Add tool definition in `mcp-server/src/index.ts`
2. Implement handler in `CallToolRequestSchema`
3. Update tests
4. Document in README.md

### Code Style

**Python:**
- Follow PEP 8
- Type hints for function signatures
- Docstrings for public functions

**TypeScript:**
- ESLint configuration provided
- Explicit types preferred
- JSDoc for public methods

## Development Setup

### Running Tests

```bash
# Python scraper tests
cd scraper
python -m pytest tests/

# TypeScript MCP tests
cd mcp-server
npm test
```

### Local Testing

Test your changes with a small documentation site before submitting:

```bash
python cli.py add --url https://vitepress.dev/ --name test-docs
```

## Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open Pull Request

## License

By contributing, you agree to license your contributions under the MIT License.
