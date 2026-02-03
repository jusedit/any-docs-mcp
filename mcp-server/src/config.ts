import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';

export interface ServerConfig {
  activeDocs: string;
  storageRoot?: string;
  serverName?: string;
  refreshDays?: number;
}

export function loadConfig(): ServerConfig {
  const configPath = join(process.cwd(), 'config.json');
  
  if (existsSync(configPath)) {
    const configData = readFileSync(configPath, 'utf-8');
    const config = JSON.parse(configData);
    return {
      ...config,
      storageRoot: config.storageRoot || process.env.ANYDOCS_STORAGE_ROOT,
      refreshDays: config.refreshDays || parseInt(process.env.ANYDOCS_REFRESH_DAYS || '30', 10)
    };
  }
  
  const activeDocs = process.env.ANYDOCS_ACTIVE || '';
  
  return {
    activeDocs,
    storageRoot: process.env.ANYDOCS_STORAGE_ROOT,
    refreshDays: parseInt(process.env.ANYDOCS_REFRESH_DAYS || '30', 10)
  };
}

export function getStorageRoot(config: ServerConfig): string {
  if (config.storageRoot) {
    return resolve(config.storageRoot);
  }
  
  const appdata = process.env.APPDATA || join(process.env.HOME || '', '.local', 'share');
  return join(appdata, 'AnyDocsMCP', 'docs');
}

export function getDocsPath(config: ServerConfig): string | null {
  if (!config.activeDocs) {
    return null;
  }
  
  const storageRoot = getStorageRoot(config);
  const docName = config.activeDocs;
  
  const docDir = join(storageRoot, docName);
  if (!existsSync(docDir)) {
    return null;
  }
  
  const versions = readdirSync(docDir).filter((d: string) => d.startsWith('v') && 
    statSync(join(docDir, d)).isDirectory());
  
  if (versions.length === 0) {
    return null;
  }
  
  interface Version {
    name: string;
    num: number;
  }
  
  const latestVersion = versions
    .map((v: string): Version => ({ name: v, num: parseInt(v.substring(1)) }))
    .filter((v: Version) => !isNaN(v.num))
    .sort((a: Version, b: Version) => b.num - a.num)[0].name;
  
  return join(docDir, latestVersion);
}

export function listAllDocs(config: ServerConfig): string[] {
  const storageRoot = getStorageRoot(config);
  if (!existsSync(storageRoot)) {
    return [];
  }
  
  return readdirSync(storageRoot).filter((d: string) => {
    const docDir = join(storageRoot, d);
    const configPath = join(docDir, 'config.json');
    return statSync(docDir).isDirectory() && existsSync(configPath);
  });
}

interface DocMetadata {
  total_pages?: number;
  total_files?: number;
  last_scraped?: string;
  content_hash?: string;
  refresh_after?: string;
  content_changed?: boolean;
}

export function getDocMetadata(config: ServerConfig, docName: string): DocMetadata | null {
  const storageRoot = getStorageRoot(config);
  const metadataPath = join(storageRoot, docName, 'metadata.json');
  
  if (!existsSync(metadataPath)) {
    return null;
  }
  
  try {
    return JSON.parse(readFileSync(metadataPath, 'utf-8'));
  } catch {
    return null;
  }
}

interface DocConfig {
  display_name?: string;
  start_url?: string;
  [key: string]: unknown;
}

export function getDocConfig(config: ServerConfig, docName: string): DocConfig | null {
  const storageRoot = getStorageRoot(config);
  const configPath = join(storageRoot, docName, 'config.json');
  
  if (!existsSync(configPath)) {
    return null;
  }
  
  try {
    return JSON.parse(readFileSync(configPath, 'utf-8'));
  } catch {
    return null;
  }
}
