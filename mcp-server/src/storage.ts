/**
 * Storage layer for managing scraped documentation in AppData.
 *
 * Layout:
 *   %APPDATA%/AnyDocsMCP/v2/
 *     windsurf-docs/
 *       AGENTS.md
 *       manifest.json
 *       md/raw/...
 *     tailwind-docs/
 *       ...
 */
import { existsSync, readdirSync, statSync, readFileSync, rmSync, mkdirSync } from 'fs';
import { join, resolve } from 'path';

export interface DocSetInfo {
  name: string;
  agentsIndex: string;
  totalPages: number;
  sourceUrl: string;
  sizeBytes: number;
  scrapedAt: string;
}

export function getStorageRoot(): string {
  const override = process.env.ANYDOCS_STORAGE_ROOT;
  if (override) return resolve(override);

  const appdata = process.env.APPDATA || join(process.env.HOME || '', '.local', 'share');
  return join(appdata, 'AnyDocsMCP', 'v2');
}

export function ensureStorageRoot(): string {
  const root = getStorageRoot();
  if (!existsSync(root)) {
    mkdirSync(root, { recursive: true });
  }
  return root;
}

export function listDocSets(): DocSetInfo[] {
  const root = getStorageRoot();
  if (!existsSync(root)) return [];

  const dirs = readdirSync(root).filter(d =>
    statSync(join(root, d)).isDirectory()
  );

  const results: DocSetInfo[] = [];
  for (const name of dirs) {
    const info = getDocSetInfo(name);
    if (info) results.push(info);
  }
  return results;
}

export function getDocSetInfo(name: string): DocSetInfo | null {
  const root = getStorageRoot();
  const docDir = join(root, name);

  const agentsPath = join(docDir, 'AGENTS.md');
  const manifestPath = join(docDir, 'manifest.json');

  if (!existsSync(agentsPath)) return null;

  let agentsIndex = '';
  try {
    agentsIndex = readFileSync(agentsPath, 'utf-8').trim();
  } catch {
    return null;
  }

  let totalPages = 0;
  let sourceUrl = '';
  let scrapedAt = '';
  try {
    const manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
    totalPages = manifest.total_pages || 0;
    sourceUrl = manifest.start_url || '';
    scrapedAt = manifest.scraped_at || '';
  } catch {
    // manifest optional
  }

  // Parse source from AGENTS.md index if not in manifest
  if (!sourceUrl) {
    const sourceMatch = agentsIndex.match(/\|source:\s*([^|]+)/);
    if (sourceMatch) sourceUrl = sourceMatch[1].trim();
  }

  const sizeBytes = getDirSize(docDir);

  return { name, agentsIndex, totalPages, sourceUrl, sizeBytes, scrapedAt };
}

export function getDocSetPath(name: string): string | null {
  const root = getStorageRoot();
  const docDir = join(root, name);
  if (!existsSync(docDir)) return null;
  return docDir;
}

export function getDocRawDir(name: string): string | null {
  const docDir = getDocSetPath(name);
  if (!docDir) return null;
  const rawDir = join(docDir, 'md', 'raw');
  if (!existsSync(rawDir)) return null;
  return rawDir;
}

export function deleteDocSet(name: string): boolean {
  const docDir = getDocSetPath(name);
  if (!docDir) return false;
  rmSync(docDir, { recursive: true, force: true });
  return true;
}

function getDirSize(dir: string): number {
  let size = 0;
  try {
    const entries = readdirSync(dir);
    for (const entry of entries) {
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);
      if (stat.isDirectory()) {
        size += getDirSize(fullPath);
      } else {
        size += stat.size;
      }
    }
  } catch {
    // ignore errors
  }
  return size;
}
