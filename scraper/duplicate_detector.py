"""Duplicate version detection for doc-set versions."""
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DuplicateGroup:
    versions: List[str]
    similarity_pct: float
    identical_files: int


def detect_duplicate_versions(doc_path: str, threshold: float = 0.8) -> List[DuplicateGroup]:
    """Detect duplicate versions in a doc-set.
    
    Args:
        doc_path: Path to doc-set directory containing version subdirs
        threshold: Minimum similarity to flag as duplicate (default 0.8)
    
    Returns:
        List of DuplicateGroup for versions above threshold
    """
    doc_dir = Path(doc_path)
    if not doc_dir.exists():
        return []
    
    # Find version directories
    version_dirs = [d for d in doc_dir.iterdir() if d.is_dir() and d.name.startswith('v')]
    
    if len(version_dirs) < 2:
        return []
    
    # Compute file hashes for each version
    version_hashes: Dict[str, Dict[str, str]] = {}
    for vdir in version_dirs:
        version_hashes[vdir.name] = {}
        for md_file in vdir.rglob("*.md"):
            content = md_file.read_text(encoding='utf-8')
            file_hash = hashlib.md5(content.encode()).hexdigest()
            rel_path = str(md_file.relative_to(vdir))
            version_hashes[vdir.name][rel_path] = file_hash
    
    # Compare version pairs
    duplicates = []
    versions = list(version_hashes.keys())
    
    for i, v1 in enumerate(versions):
        for v2 in versions[i+1:]:
            files1 = version_hashes[v1]
            files2 = version_hashes[v2]
            
            # Count identical files
            identical = sum(1 for f, h in files1.items() if f in files2 and files2[f] == h)
            total = max(len(files1), len(files2))
            
            if total > 0:
                similarity = identical / total
                if similarity >= threshold:
                    duplicates.append(DuplicateGroup(
                        versions=[v1, v2],
                        similarity_pct=similarity,
                        identical_files=identical
                    ))
    
    return duplicates


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect duplicate doc-set versions")
    parser.add_argument("doc_root", help="Path to doc-set root")
    parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold")
    parser.add_argument("--output", help="Output JSON file")
    
    args = parser.parse_args()
    
    duplicates = detect_duplicate_versions(args.doc_root, args.threshold)
    
    result = {
        "doc_set": Path(args.doc_root).name,
        "threshold": args.threshold,
        "duplicates_found": len(duplicates),
        "groups": [
            {
                "versions": g.versions,
                "similarity_pct": g.similarity_pct,
                "identical_files": g.identical_files
            }
            for g in duplicates
        ]
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Report written to: {args.output}")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
