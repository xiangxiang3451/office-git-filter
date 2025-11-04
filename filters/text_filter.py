import os
import chardet
from .base_filter import BaseFilter


class TextFilter(BaseFilter):
    """Text file filter"""

    def __init__(self):
        super().__init__()
        self.supported_formats = [
            '.txt', '.md', '.rst', '.csv', '.json', '.xml',
            '.html', '.htm', '.py', '.js', '.java', '.cpp', '.c',
            '.h', '.php', '.rb', '.go', '.rs'
        ]

    def to_text(self, file_path: str) -> str:
        """Read text file content"""
        try:
            # Detect file encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'

            # Read file content
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()

            return content
        except Exception as e:
            return f"[Failed to read text file: {str(e)}]"