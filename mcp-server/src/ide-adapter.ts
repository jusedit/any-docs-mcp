/**
 * IDE Adapter interface + implementations.
 *
 * Each IDE has its own way of persisting "always-on" context rules.
 * The adapter handles:
 *   1. Copying docs into the project
 *   2. Injecting/removing the compact index into IDE-specific rules
 *
 * Supported IDEs:
 *   - windsurf:     .windsurf/rules/<name>.md (trigger: always_on)
 *   - cursor:       .cursor/rules/<name>.mdc (alwaysApply: true)
 *   - claude:       CLAUDE.md with markers
 *   - antigravity:  .agent/rules/<name>.md (Always On)
 *
 * Set via ANYDOCS_IDE env variable (default: "windsurf").
 */
import { existsSync, mkdirSync, writeFileSync, readFileSync, rmSync, cpSync, readdirSync } from 'fs';
import { join, basename } from 'path';

export type IdeType = 'windsurf' | 'cursor' | 'claude' | 'antigravity';

export interface IdeAdapter {
  readonly ideType: IdeType;
  addDocsToProject(projectRoot: string, docName: string, docsSourceDir: string, agentsIndex: string): AddResult;
  removeDocsFromProject(projectRoot: string, docName: string): RemoveResult;
  listProjectDocs(projectRoot: string): string[];
}

export interface AddResult {
  success: boolean;
  docsDir: string;
  rulesFile: string;
  message: string;
}

export interface RemoveResult {
  success: boolean;
  message: string;
}

// ---------------------------------------------------------------------------
// Windsurf Adapter
// ---------------------------------------------------------------------------

class WindsurfAdapter implements IdeAdapter {
  readonly ideType: IdeType = 'windsurf';

  addDocsToProject(projectRoot: string, docName: string, docsSourceDir: string, agentsIndex: string): AddResult {
    const docsDir = join(projectRoot, '.windsurf', 'docs', docName);
    const rulesDir = join(projectRoot, '.windsurf', 'rules');
    const rulesFile = join(rulesDir, `docs-${docName}.md`);

    // 1. Copy docs into project
    mkdirSync(docsDir, { recursive: true });
    cpSync(docsSourceDir, docsDir, { recursive: true });

    // 2. Create always-on rule file with the compact index
    mkdirSync(rulesDir, { recursive: true });

    // Rewrite root path to point to project-local docs
    const localRoot = `.windsurf/docs/${docName}`;
    const adjustedIndex = agentsIndex.replace(/\|root:\s*[^|]+/, `|root: ./${localRoot}`);

    const ruleContent = [
      '---',
      `trigger: always_on`,
      '---',
      '',
      adjustedIndex,
      '',
    ].join('\n');

    writeFileSync(rulesFile, ruleContent, 'utf-8');

    return {
      success: true,
      docsDir,
      rulesFile,
      message: `Added ${docName} docs to Windsurf project.\n` +
        `  Docs: ${docsDir}\n` +
        `  Rule: ${rulesFile} (always_on)`,
    };
  }

  removeDocsFromProject(projectRoot: string, docName: string): RemoveResult {
    const docsDir = join(projectRoot, '.windsurf', 'docs', docName);
    const rulesFile = join(projectRoot, '.windsurf', 'rules', `docs-${docName}.md`);

    let removed = false;

    if (existsSync(docsDir)) {
      rmSync(docsDir, { recursive: true, force: true });
      removed = true;
    }

    if (existsSync(rulesFile)) {
      rmSync(rulesFile, { force: true });
      removed = true;
    }

    if (!removed) {
      return { success: false, message: `Documentation "${docName}" not found in this project.` };
    }

    // Clean up empty dirs
    const docsParent = join(projectRoot, '.windsurf', 'docs');
    if (existsSync(docsParent) && readdirSync(docsParent).length === 0) {
      rmSync(docsParent, { recursive: true });
    }

    return {
      success: true,
      message: `Removed ${docName} docs from Windsurf project.`,
    };
  }

  listProjectDocs(projectRoot: string): string[] {
    const docsDir = join(projectRoot, '.windsurf', 'docs');
    if (!existsSync(docsDir)) return [];
    return readdirSync(docsDir).filter(d => {
      const rulesFile = join(projectRoot, '.windsurf', 'rules', `docs-${d}.md`);
      return existsSync(rulesFile);
    });
  }
}

// ---------------------------------------------------------------------------
// Cursor Adapter (placeholder for future)
// ---------------------------------------------------------------------------

class CursorAdapter implements IdeAdapter {
  readonly ideType: IdeType = 'cursor';

  addDocsToProject(projectRoot: string, docName: string, docsSourceDir: string, agentsIndex: string): AddResult {
    const docsDir = join(projectRoot, '.cursor', 'docs', docName);
    const rulesDir = join(projectRoot, '.cursor', 'rules');
    const rulesFile = join(rulesDir, `docs-${docName}.mdc`);

    mkdirSync(docsDir, { recursive: true });
    cpSync(docsSourceDir, docsDir, { recursive: true });

    mkdirSync(rulesDir, { recursive: true });

    const localRoot = `.cursor/docs/${docName}`;
    const adjustedIndex = agentsIndex.replace(/\|root:\s*[^|]+/, `|root: ./${localRoot}`);

    const ruleContent = [
      '---',
      `description: ${docName} documentation index`,
      `globs: **/*`,
      `alwaysApply: true`,
      '---',
      '',
      adjustedIndex,
      '',
    ].join('\n');

    writeFileSync(rulesFile, ruleContent, 'utf-8');

    return {
      success: true,
      docsDir,
      rulesFile,
      message: `Added ${docName} docs to Cursor project.\n` +
        `  Docs: ${docsDir}\n` +
        `  Rule: ${rulesFile} (alwaysApply)`,
    };
  }

  removeDocsFromProject(projectRoot: string, docName: string): RemoveResult {
    const docsDir = join(projectRoot, '.cursor', 'docs', docName);
    const rulesFile = join(projectRoot, '.cursor', 'rules', `docs-${docName}.mdc`);

    let removed = false;
    if (existsSync(docsDir)) { rmSync(docsDir, { recursive: true, force: true }); removed = true; }
    if (existsSync(rulesFile)) { rmSync(rulesFile, { force: true }); removed = true; }

    if (!removed) return { success: false, message: `Documentation "${docName}" not found in this project.` };

    const docsParent = join(projectRoot, '.cursor', 'docs');
    if (existsSync(docsParent) && readdirSync(docsParent).length === 0) {
      rmSync(docsParent, { recursive: true });
    }

    return { success: true, message: `Removed ${docName} docs from Cursor project.` };
  }

  listProjectDocs(projectRoot: string): string[] {
    const docsDir = join(projectRoot, '.cursor', 'docs');
    if (!existsSync(docsDir)) return [];
    return readdirSync(docsDir).filter(d => {
      const rulesFile = join(projectRoot, '.cursor', 'rules', `docs-${d}.mdc`);
      return existsSync(rulesFile);
    });
  }
}

// ---------------------------------------------------------------------------
// Claude Code Adapter (placeholder for future)
// ---------------------------------------------------------------------------

class ClaudeAdapter implements IdeAdapter {
  readonly ideType: IdeType = 'claude';

  private readonly START_MARKER = '<!-- ANYDOCS-START:';
  private readonly END_MARKER = '<!-- ANYDOCS-END:';

  addDocsToProject(projectRoot: string, docName: string, docsSourceDir: string, agentsIndex: string): AddResult {
    const docsDir = join(projectRoot, '.docs', docName);
    const claudeMdPath = join(projectRoot, 'CLAUDE.md');

    mkdirSync(docsDir, { recursive: true });
    cpSync(docsSourceDir, docsDir, { recursive: true });

    const localRoot = `.docs/${docName}`;
    const adjustedIndex = agentsIndex.replace(/\|root:\s*[^|]+/, `|root: ./${localRoot}`);

    const startTag = `${this.START_MARKER}${docName} -->`;
    const endTag = `${this.END_MARKER}${docName} -->`;
    const block = `${startTag}\n${adjustedIndex}\n${endTag}`;

    let content = '';
    if (existsSync(claudeMdPath)) {
      content = readFileSync(claudeMdPath, 'utf-8');
      // Replace existing block or append
      const startIdx = content.indexOf(startTag);
      const endIdx = content.indexOf(endTag);
      if (startIdx !== -1 && endIdx !== -1) {
        content = content.slice(0, startIdx) + block + content.slice(endIdx + endTag.length);
      } else {
        content = content.trimEnd() + '\n\n' + block + '\n';
      }
    } else {
      content = block + '\n';
    }

    writeFileSync(claudeMdPath, content, 'utf-8');

    return {
      success: true,
      docsDir,
      rulesFile: claudeMdPath,
      message: `Added ${docName} docs to Claude Code project.\n` +
        `  Docs: ${docsDir}\n` +
        `  Index: ${claudeMdPath}`,
    };
  }

  removeDocsFromProject(projectRoot: string, docName: string): RemoveResult {
    const docsDir = join(projectRoot, '.docs', docName);
    const claudeMdPath = join(projectRoot, 'CLAUDE.md');

    let removed = false;
    if (existsSync(docsDir)) { rmSync(docsDir, { recursive: true, force: true }); removed = true; }

    if (existsSync(claudeMdPath)) {
      const startTag = `${this.START_MARKER}${docName} -->`;
      const endTag = `${this.END_MARKER}${docName} -->`;
      let content = readFileSync(claudeMdPath, 'utf-8');
      const startIdx = content.indexOf(startTag);
      const endIdx = content.indexOf(endTag);
      if (startIdx !== -1 && endIdx !== -1) {
        content = content.slice(0, startIdx) + content.slice(endIdx + endTag.length);
        content = content.replace(/\n{3,}/g, '\n\n').trim() + '\n';
        writeFileSync(claudeMdPath, content, 'utf-8');
        removed = true;
      }
    }

    if (!removed) return { success: false, message: `Documentation "${docName}" not found in this project.` };

    const docsParent = join(projectRoot, '.docs');
    if (existsSync(docsParent) && readdirSync(docsParent).length === 0) {
      rmSync(docsParent, { recursive: true });
    }

    return { success: true, message: `Removed ${docName} docs from Claude Code project.` };
  }

  listProjectDocs(projectRoot: string): string[] {
    const docsDir = join(projectRoot, '.docs');
    if (!existsSync(docsDir)) return [];
    return readdirSync(docsDir);
  }
}

// ---------------------------------------------------------------------------
// Antigravity Adapter (Jules / Gemini)
// ---------------------------------------------------------------------------

class AntigravityAdapter implements IdeAdapter {
  readonly ideType: IdeType = 'antigravity';

  addDocsToProject(projectRoot: string, docName: string, docsSourceDir: string, agentsIndex: string): AddResult {
    const docsDir = join(projectRoot, '.agent', 'docs', docName);
    const rulesDir = join(projectRoot, '.agent', 'rules');
    const rulesFile = join(rulesDir, `docs-${docName}.md`);

    // 1. Copy docs into project
    mkdirSync(docsDir, { recursive: true });
    cpSync(docsSourceDir, docsDir, { recursive: true });

    // 2. Create always-on rule file with the compact index
    mkdirSync(rulesDir, { recursive: true });

    const localRoot = `.agent/docs/${docName}`;
    const adjustedIndex = agentsIndex.replace(/\|root:\s*[^|]+/, `|root: ./${localRoot}`);

    // Antigravity rules are plain markdown. The "Always On" activation
    // is configured in the IDE UI, but we add a clear header.
    const ruleContent = [
      `# ${docName} Documentation Index`,
      '',
      `> Activation: Always On`,
      '',
      adjustedIndex,
      '',
    ].join('\n');

    writeFileSync(rulesFile, ruleContent, 'utf-8');

    return {
      success: true,
      docsDir,
      rulesFile,
      message: `Added ${docName} docs to Antigravity project.\n` +
        `  Docs: ${docsDir}\n` +
        `  Rule: ${rulesFile} (Always On)\n` +
        `  Note: Set rule activation to "Always On" in Antigravity's Customizations panel.`,
    };
  }

  removeDocsFromProject(projectRoot: string, docName: string): RemoveResult {
    const docsDir = join(projectRoot, '.agent', 'docs', docName);
    const rulesFile = join(projectRoot, '.agent', 'rules', `docs-${docName}.md`);

    let removed = false;
    if (existsSync(docsDir)) { rmSync(docsDir, { recursive: true, force: true }); removed = true; }
    if (existsSync(rulesFile)) { rmSync(rulesFile, { force: true }); removed = true; }

    if (!removed) return { success: false, message: `Documentation "${docName}" not found in this project.` };

    const docsParent = join(projectRoot, '.agent', 'docs');
    if (existsSync(docsParent) && readdirSync(docsParent).length === 0) {
      rmSync(docsParent, { recursive: true });
    }

    return { success: true, message: `Removed ${docName} docs from Antigravity project.` };
  }

  listProjectDocs(projectRoot: string): string[] {
    const docsDir = join(projectRoot, '.agent', 'docs');
    if (!existsSync(docsDir)) return [];
    return readdirSync(docsDir).filter(d => {
      const rulesFile = join(projectRoot, '.agent', 'rules', `docs-${d}.md`);
      return existsSync(rulesFile);
    });
  }
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

export function getIdeType(): IdeType {
  const ide = (process.env.ANYDOCS_IDE || 'windsurf').toLowerCase();
  if (ide === 'cursor' || ide === 'claude' || ide === 'antigravity') return ide as IdeType;
  return 'windsurf';
}

export function createAdapter(ideType?: IdeType): IdeAdapter {
  const type = ideType || getIdeType();
  switch (type) {
    case 'cursor': return new CursorAdapter();
    case 'claude': return new ClaudeAdapter();
    case 'antigravity': return new AntigravityAdapter();
    default: return new WindsurfAdapter();
  }
}
