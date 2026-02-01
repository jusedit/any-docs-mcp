import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from models import DocumentationConfig


class StorageManager:
    def __init__(self, root_path: Optional[str] = None):
        if root_path:
            self.root = Path(root_path)
        else:
            appdata = os.getenv('APPDATA') or os.path.expanduser('~/.local/share')
            self.root = Path(appdata) / 'AnyDocsMCP' / 'docs'
        
        self.root.mkdir(parents=True, exist_ok=True)
    
    def get_docs_path(self, doc_name: str, version: Optional[str] = None) -> Path:
        doc_dir = self.root / doc_name
        if version:
            return doc_dir / version
        return doc_dir / self.get_latest_version(doc_name)
    
    def get_config_path(self, doc_name: str) -> Path:
        return self.root / doc_name / 'config.json'
    
    def get_metadata_path(self, doc_name: str) -> Path:
        return self.root / doc_name / 'metadata.json'
    
    def save_config(self, config: DocumentationConfig):
        config_path = self.get_config_path(config.name)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config.model_dump(), f, indent=2)
    
    def load_config(self, doc_name: str) -> Optional[DocumentationConfig]:
        config_path = self.get_config_path(doc_name)
        if not config_path.exists():
            return None
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return DocumentationConfig(**data)
    
    def create_version(self, doc_name: str) -> str:
        doc_dir = self.root / doc_name
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        existing_versions = [d.name for d in doc_dir.iterdir() if d.is_dir() and d.name.startswith('v')]
        
        if not existing_versions:
            version = 'v1'
        else:
            version_numbers = []
            for v in existing_versions:
                try:
                    version_numbers.append(int(v[1:]))
                except ValueError:
                    pass
            next_num = max(version_numbers) + 1 if version_numbers else 1
            version = f'v{next_num}'
        
        version_dir = doc_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)
        
        return version
    
    def get_latest_version(self, doc_name: str) -> str:
        doc_dir = self.root / doc_name
        if not doc_dir.exists():
            return 'v1'
        
        versions = [d.name for d in doc_dir.iterdir() if d.is_dir() and d.name.startswith('v')]
        if not versions:
            return 'v1'
        
        version_numbers = []
        for v in versions:
            try:
                version_numbers.append((int(v[1:]), v))
            except ValueError:
                pass
        
        if not version_numbers:
            return 'v1'
        
        return max(version_numbers)[1]
    
    def list_documentation_sets(self) -> list[str]:
        if not self.root.exists():
            return []
        
        return [d.name for d in self.root.iterdir() if d.is_dir() and (d / 'config.json').exists()]
    
    def save_metadata(self, doc_name: str, metadata: dict):
        metadata_path = self.get_metadata_path(doc_name)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def load_metadata(self, doc_name: str) -> dict:
        metadata_path = self.get_metadata_path(doc_name)
        if not metadata_path.exists():
            return {}
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_output_file_path(self, doc_name: str, version: str, filename: str) -> Path:
        version_dir = self.root / doc_name / version
        version_dir.mkdir(parents=True, exist_ok=True)
        return version_dir / f"{filename}.md"
