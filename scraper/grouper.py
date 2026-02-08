"""FR5: Compact AGENTS.md index generation.

Inspired by next-agents-md: generates a minimal, token-efficient index
that points to individual raw documentation files. No LLM grouping,
no file merging — the agent reads files on-demand.

Format: Single-line pipe-separated index with directory-grouped file lists.
Example:
  [Doc Name]|root: ./md/raw|IMPORTANT: ...|dir/:{file1.md,file2.md}|other/:{f.md}

This minimizes context window usage (~200-500 bytes) while giving the agent
a complete map of available documentation files.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from models import Manifest, ManifestEntry


class Grouper:
    def __init__(self, **kwargs):
        pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def group_and_package(self, manifest: Manifest, output_dir: str, doc_name: str) -> Path:
        """Generate compact AGENTS.md index and write manifest.

        No file merging — raw files stay as-is for on-demand retrieval.
        Returns path to generated AGENTS.md.
        """
        output = Path(output_dir)

        # 1. Generate compact AGENTS.md
        agents_path = output / "AGENTS.md"
        self._generate_compact_index(manifest, agents_path, doc_name)
        size = agents_path.stat().st_size
        print(f"  [index] Generated AGENTS.md ({size} bytes, {manifest.total_pages} files indexed)", file=sys.stderr)

        # 2. Write manifest
        manifest_path = output / "manifest.json"
        manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")

        return agents_path

    # ------------------------------------------------------------------
    # Compact index generation
    # ------------------------------------------------------------------

    def _generate_compact_index(self, manifest: Manifest, out_path: Path, doc_name: str):
        """Generate a compact pipe-separated AGENTS.md index.

        Format mirrors next-agents-md:
          [Name]|root: ./md/raw|instruction|dir/:{file1,file2}|dir2/:{f3}
        """
        parts: List[str] = []

        # Preamble
        parts.append(f"[{doc_name} Docs Index]")
        parts.append("root: ./md/raw")
        parts.append("IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.")
        parts.append(f"source: {manifest.start_url}")

        # Group files by directory
        dir_files: Dict[str, List[str]] = defaultdict(list)
        for entry in sorted(manifest.entries, key=lambda e: e.md_raw_path):
            path = entry.md_raw_path.replace("\\", "/")
            last_slash = path.rfind("/")
            if last_slash == -1:
                dir_name = "."
                file_name = path
            else:
                dir_name = path[:last_slash]
                file_name = path[last_slash + 1:]
            dir_files[dir_name].append(file_name)

        # Format: dir/:{file1,file2,file3}
        for dir_name in sorted(dir_files.keys()):
            files = dir_files[dir_name]
            files_str = ",".join(files)
            parts.append(f"{dir_name}/:{{{files_str}}}")

        index_line = "|".join(parts)
        out_path.write_text(index_line + "\n", encoding="utf-8")
