"""Table compression for oversized reference documentation."""
import re
from typing import Optional


class TableCompressor:
    """Compresses large markdown tables by keeping representative rows."""
    
    def __init__(self, max_rows: int = 100, keep_rows: int = 10):
        self.max_rows = max_rows
        self.keep_rows = keep_rows
    
    def compress_table(self, table_text: str) -> str:
        """Compress a table if it exceeds max_rows.
        
        Keeps first keep_rows as examples, adds summary row.
        """
        lines = table_text.strip().split('\n')
        
        # Count data rows (exclude header and separator)
        data_rows = [l for l in lines if l.startswith('|') and '---' not in l]
        total_data_rows = len(data_rows)
        
        if total_data_rows <= self.max_rows:
            return table_text
        
        # Find header and separator
        header = next((l for l in lines if l.startswith('|')), '')
        separator = next((l for l in lines if '---' in l), '')
        
        # Keep first N rows + summary
        kept_rows = data_rows[:self.keep_rows]
        summary_row = f"| ... ({total_data_rows - self.keep_rows} more rows) | ... |"
        
        result = [header, separator] + kept_rows + [summary_row]
        return '\n'.join(result)
