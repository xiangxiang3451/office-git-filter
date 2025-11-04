import os
import chardet
from .base_filter import BaseFilter


class TextFilter(BaseFilter):
    """文本文件过滤器"""

    def __init__(self):
        super().__init__()
        self.supported_formats = [
            '.txt', '.md', '.rst', '.csv', '.json', '.xml',
            '.html', '.htm', '.py', '.js', '.java', '.cpp', '.c',
            '.h', '.php', '.rb', '.go', '.rs'
        ]

    def to_text(self, file_path: str) -> str:
        """读取文本文件内容"""
        try:
            # 检测文件编码
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'

            # 读取文件内容
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()

            return content
        except Exception as e:
            return f"[读取文本文件失败: {str(e)}]"