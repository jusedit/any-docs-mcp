import { describe, it, expect } from 'vitest';
import { MarkdownParser } from '../markdown-parser.js';
import { loadConfig } from '../config.js';

describe('Module Imports', () => {
  it('MarkdownParser imports successfully', () => {
    expect(MarkdownParser).toBeDefined();
    expect(typeof MarkdownParser).toBe('function');
  });

  it('loadConfig imports successfully', () => {
    expect(loadConfig).toBeDefined();
    expect(typeof loadConfig).toBe('function');
  });
});
