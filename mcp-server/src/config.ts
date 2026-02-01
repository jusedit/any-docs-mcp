import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';

export interface ServerConfig {
  activeDocs: string;
  storageRoot?: string;
  serverName?: string;
}

export function loadConfig(): ServerConfig {
  const configPath = join(process.cwd(), 'config.json');
  
  if (existsSync(configPath)) {
    const configData = readFileSync(configPath, 'utf-8');
    return JSON.parse(configData);
  }
  
  const activeDocs = process.env.ANYDOCS_ACTIVE || '';
  if (!activeDocs) {
    throw new Error('No configuration found. Create config.json or set ANYDOCS_ACTIVE environment variable.');
  }
  
  return {
    activeDocs,
    storageRoot: process.env.ANYDOCS_STORAGE_ROOT
  };
}

export function getStorageRoot(config: ServerConfig): string {
  if (config.storageRoot) {
    return resolve(config.storageRoot);
  }
  
  const appdata = process.env.APPDATA || join(process.env.HOME || '', '.local', 'share');
  return join(appdata, 'AnyDocsMCP', 'docs');
}

export function getDocsPath(config: ServerConfig): string {
  const storageRoot = getStorageRoot(config);
  const docName = config.activeDocs;
  
  const docDir = join(storageRoot, docName);
  const versions = existsSync(docDir) ? 
    readdirSync(docDir).filter((d: string) => d.startsWith('v') && 
      statSync(join(docDir, d)).isDirectory()) : [];
  
  if (versions.length === 0) {
    throw new Error(`No versions found for documentation: ${docName}`);
  }
  
  const latestVersion = versions
    .map((v: string) => ({ name: v, num: parseInt(v.substring(1)) }))
    .filter((v: any) => !isNaN(v.num))
    .sort((a: any, b: any) => b.num - a.num)[0].name;
  
  return join(docDir, latestVersion);
}
