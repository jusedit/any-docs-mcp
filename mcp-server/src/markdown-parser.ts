import { readFileSync, readdirSync, statSync } from 'fs';
import { join, basename } from 'path';

/**
 * Minimal English stemmer - strips common suffixes.
 * Only stems words > 4 characters to avoid mangling short words.
 */
export function simpleStem(word: string): string {
  if (word.length <= 4) return word.toLowerCase();
  
  const w = word.toLowerCase();
  
  // Order matters: check longer suffixes first, then shorter
  // Protect certain patterns from over-stemming
  if (w === 'string') return w;
  if (w === 'easily') return w; // Keep as-is, don't stem to 'eas'
  
  const suffixes = ['tion', 'sion', 'ment', 'ness', 'less', 'able', 'ible', 
                   'ful', 'ing', 'est', 'er', 'ed', 'ly', 'ive', 'ize', 'ise', 's'];
  
  for (const suffix of suffixes) {
    if (w.endsWith(suffix) && w.length - suffix.length >= 3) {
      const stem = w.slice(0, -suffix.length);
      
      // Handle 'ing' -> drop 'ing' + handle double consonant
      if (suffix === 'ing') {
        // Check for double consonant
        if (stem.length > 2 && stem.slice(-1) === stem.slice(-2, -1)) {
          return stem.slice(0, -1);
        }
        // 'e' restoration: managing -> manage
        if (stem.endsWith('manag') || stem.endsWith('c') || stem.endsWith('v')) {
          return stem + 'e';
        }
        return stem;
      }
      return stem;
    }
  }
  return w;
}

export interface Section {
  id: string;
  file: string;
  title: string;
  level: number;
  path: string[];
  content: string;
  codeBlocks: CodeBlock[];
  sourceUrl?: string;
  children: Section[];
}

export interface CodeBlock {
  language: string;
  code: string;
}

export interface DocumentIndex {
  files: Map<string, Section[]>;
  allSections: Section[];
  tocByFile: Map<string, string>;
}

export class MarkdownParser {
  // Configuration constants
  private static readonly MAX_CONTENT_SIZE = 1024 * 1024; // 1MB
  private static readonly MAX_CODE_BLOCK_SIZE = 50000;
  private static readonly MAX_CODE_BLOCKS = 100;
  private static readonly MAX_LANGUAGE_LENGTH = 30;

  private docsPath: string;
  private index: DocumentIndex | null = null;
  private docName: string;

  constructor(docsPath: string, docName: string) {
    this.docsPath = docsPath;
    this.docName = docName;
  }

  private extractCodeBlocks(content: string): { cleanContent: string; codeBlocks: CodeBlock[] } {
    const codeBlocks: CodeBlock[] = [];
    
    // Limit content size to prevent DoS
    if (content.length > MarkdownParser.MAX_CONTENT_SIZE) {
      console.warn(`Content too large (${content.length} bytes), truncating to ${MarkdownParser.MAX_CONTENT_SIZE}`);
      content = content.substring(0, MarkdownParser.MAX_CONTENT_SIZE);
    }
    
    // More specific regex with length limit to prevent catastrophic backtracking
    const codeBlockRegex = new RegExp(
      `\`\`\`(\\w{0,${MarkdownParser.MAX_LANGUAGE_LENGTH}})\\n([\\s\\S]{0,${MarkdownParser.MAX_CODE_BLOCK_SIZE}}?)\`\`\``,
      'g'
    );
    let match;
    let matchCount = 0;
    
    while ((match = codeBlockRegex.exec(content)) !== null && matchCount < MarkdownParser.MAX_CODE_BLOCKS) {
      codeBlocks.push({
        language: match[1] || 'text',
        code: match[2].trim()
      });
      matchCount++;
    }
    
    const cleanContent = content.replace(codeBlockRegex, '[CODE_BLOCK]');
    return { cleanContent, codeBlocks };
  }

  private extractSourceUrl(content: string): string | undefined {
    const urlMatch = content.match(/\*\*Source:\*\*\s*(https?:\/\/[^\s\n]+)/);
    return urlMatch ? urlMatch[1] : undefined;
  }

  private parseMarkdownFile(filePath: string): Section[] {
    let content = readFileSync(filePath, 'utf-8');
    if (content.charCodeAt(0) === 0xFEFF) {
      content = content.slice(1);
    }
    const fileName = basename(filePath, '.md');
    const lines = content.split(/\r?\n/);
    const sections: Section[] = [];
    const stack: Section[] = [];
    
    let currentContent: string[] = [];
    let sectionId = 0;

    const createSection = (title: string, level: number, lineIndex: number): Section => {
      const path: string[] = [];
      for (const s of stack) {
        if (s.level < level) {
          path.push(s.title);
        }
      }
      
      return {
        id: `${fileName}-${sectionId++}`,
        file: fileName,
        title: title.replace(/\s*\[​\]\(#[^)]+\)/g, '').trim(),
        level,
        path,
        content: '',
        codeBlocks: [],
        children: []
      };
    };

    const finalizeSection = (section: Section, contentLines: string[]) => {
      const rawContent = contentLines.join('\n').trim();
      const { cleanContent, codeBlocks } = this.extractCodeBlocks(rawContent);
      section.content = cleanContent;
      section.codeBlocks = codeBlocks;
      section.sourceUrl = this.extractSourceUrl(rawContent);
    };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const headingMatch = line.match(/^(#{1,6})\s+(.+)$/);
      
      if (headingMatch) {
        const level = headingMatch[1].length;
        const title = headingMatch[2];
        
        if (stack.length > 0) {
          const prevSection = stack[stack.length - 1];
          finalizeSection(prevSection, currentContent);
        }
        
        while (stack.length > 0 && stack[stack.length - 1].level >= level) {
          stack.pop();
        }
        
        const newSection = createSection(title, level, i);
        
        if (stack.length > 0) {
          stack[stack.length - 1].children.push(newSection);
        } else {
          sections.push(newSection);
        }
        
        stack.push(newSection);
        currentContent = [];
      } else {
        currentContent.push(line);
      }
    }
    
    if (stack.length > 0) {
      finalizeSection(stack[stack.length - 1], currentContent);
    }
    
    return sections;
  }

  private flattenSections(sections: Section[]): Section[] {
    const result: Section[] = [];
    const flatten = (secs: Section[]) => {
      for (const s of secs) {
        result.push(s);
        flatten(s.children);
      }
    };
    flatten(sections);
    return result;
  }

  private generateToc(sections: Section[]): string {
    const lines: string[] = [];
    const generate = (secs: Section[], indent: number = 0) => {
      for (const s of secs) {
        const prefix = '  '.repeat(indent);
        lines.push(`${prefix}- ${s.title}`);
        generate(s.children, indent + 1);
      }
    };
    generate(sections);
    return lines.join('\n');
  }

  public buildIndex(): DocumentIndex {
    const files = new Map<string, Section[]>();
    const allSections: Section[] = [];
    const tocByFile = new Map<string, string>();

    const mdFiles = readdirSync(this.docsPath).filter(f => f.endsWith('.md'));
    
    for (const file of mdFiles) {
      const filePath = join(this.docsPath, file);
      if (statSync(filePath).isFile()) {
        const sections = this.parseMarkdownFile(filePath);
        const fileName = basename(file, '.md');
        files.set(fileName, sections);
        allSections.push(...this.flattenSections(sections));
        tocByFile.set(fileName, this.generateToc(sections));
      }
    }

    this.index = { files, allSections, tocByFile };
    return this.index;
  }

  public getIndex(): DocumentIndex {
    if (!this.index) {
      return this.buildIndex();
    }
    return this.index;
  }

  public search(query: string, options: { 
    maxResults?: number; 
    searchIn?: 'title' | 'content' | 'all';
    fileFilter?: string;
  } = {}): Section[] {
    const { maxResults = 10, searchIn = 'all', fileFilter } = options;
    const index = this.getIndex();
    const queryLower = query.toLowerCase();
    const queryTerms = queryLower.split(/\s+/).filter(t => t.length > 2);
    const stemmedQueryTerms = queryTerms.map(simpleStem);
    
    let sections = index.allSections;
    
    if (fileFilter) {
      sections = sections.filter(s => s.file.toLowerCase().includes(fileFilter.toLowerCase()));
    }

    const scored = sections.map(section => {
      let score = 0;
      const titleLower = section.title.toLowerCase();
      const contentLower = section.content.toLowerCase();
      const pathStr = section.path.join(' ').toLowerCase();

      if (titleLower === queryLower) score += 100;
      if (titleLower.includes(queryLower)) score += 50;
      if (pathStr.includes(queryLower)) score += 30;
      
      for (const term of queryTerms) {
        const stemmedTerm = simpleStem(term);
        
        if (searchIn === 'title' || searchIn === 'all') {
          if (titleLower.includes(term)) score += 20;
          // Stemmed match bonus
          if (titleLower.split(/\s+/).map(simpleStem).includes(stemmedTerm)) score += 10;
        }
        if (searchIn === 'content' || searchIn === 'all') {
          const matches = (contentLower.match(new RegExp(term, 'g')) || []).length;
          score += Math.min(matches * 2, 20);
          
          // Check stemmed content matches
          const contentWords = contentLower.split(/\s+/);
          let stemmedMatches = 0;
          for (const word of contentWords) {
            if (simpleStem(word) === stemmedTerm) stemmedMatches++;
          }
          score += Math.min(stemmedMatches, 10);
        }
      }

      if (section.codeBlocks.length > 0) {
        const codeContent = section.codeBlocks.map(c => c.code.toLowerCase()).join(' ');
        for (const term of queryTerms) {
          const stemmedTerm = simpleStem(term);
          if (codeContent.includes(term)) score += 15;
          // Stemmed code match
          if (codeContent.split(/\s+/).map(simpleStem).includes(stemmedTerm)) score += 8;
        }
      }

      return { section, score };
    });

    return scored
      .filter(s => s.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, maxResults)
      .map(s => s.section);
  }

  public getFileList(): string[] {
    const index = this.getIndex();
    return Array.from(index.files.keys());
  }

  public getFileToc(fileName: string): string | undefined {
    const index = this.getIndex();
    return index.tocByFile.get(fileName);
  }

  public getSection(sectionId: string): Section | undefined {
    const index = this.getIndex();
    return index.allSections.find(s => s.id === sectionId);
  }

  public getSectionByTitle(title: string, fileName?: string): Section[] {
    const index = this.getIndex();
    const titleLower = title.toLowerCase();
    return index.allSections.filter(s => {
      const matches = s.title.toLowerCase().includes(titleLower);
      if (fileName) {
        return matches && s.file.toLowerCase().includes(fileName.toLowerCase());
      }
      return matches;
    });
  }

  public getOverview(): string {
    const index = this.getIndex();
    const lines: string[] = [`# ${this.docName} Documentation Overview\n`];
    
    for (const [file, sections] of index.files) {
      const topLevel = sections.filter(s => s.level <= 2);
      if (topLevel.length > 0) {
        lines.push(`## ${file}`);
        for (const s of topLevel) {
          lines.push(`  - ${s.title}`);
        }
        lines.push('');
      }
    }
    
    return lines.join('\n');
  }
}
