import os
import subprocess
import tempfile
from .base_filter import BaseFilter


class OfficeFilter(BaseFilter):
    """Office文档过滤器"""

    def __init__(self):
        super().__init__()
        self.supported_formats = [
            '.doc', '.docx', '.xls', '.xlsx',
            '.ppt', '.pptx', '.odt', '.ods', '.odp'
        ]

    def to_text(self, file_path: str) -> str:
        """转换Office文档为文本"""
        ext = os.path.splitext(file_path)[1].lower()

        # 尝试使用LibreOffice
        text = self._use_libreoffice(file_path)
        if text:
            return text

        # 特定格式的备用方法
        if ext == '.doc':
            return self._use_antiword(file_path)
        elif ext == '.docx':
            return self._use_docx_library(file_path)
        elif ext in ['.xls', '.xlsx']:
            return self._use_excel_library(file_path)

        return f"[Office文件: {os.path.basename(file_path)}]"

    def _use_libreoffice(self, file_path: str) -> str:
        """使用LibreOffice进行转换"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # 转换为文本
                result = subprocess.run([
                    'soffice', '--headless', '--convert-to', 'txt:Text',
                    '--outdir', temp_dir, file_path
                ], capture_output=True, check=True)

                # 读取转换后的文件
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                txt_file = os.path.join(temp_dir, f"{base_name}.txt")

                if os.path.exists(txt_file):
                    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read().strip()

            return ""
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def _use_antiword(self, file_path: str) -> str:
        """使用antiword处理.doc文件"""
        try:
            result = subprocess.run(
                ['antiword', file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return self._use_catdoc(file_path)

    def _use_catdoc(self, file_path: str) -> str:
        """使用catdoc处理.doc文件"""
        try:
            result = subprocess.run(
                ['catdoc', file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def _use_docx_library(self, file_path: str) -> str:
        """使用python-docx处理.docx文件"""
        try:
            import docx
            doc = docx.Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except ImportError:
            return ""

    def _use_excel_library(self, file_path: str) -> str:
        """使用openpyxl处理Excel文件"""
        try:
            import openpyxl
            wb = openpyxl.load_workbook(file_path, data_only=True)
            text = []

            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                text.append(f"工作表: {sheet_name}")

                for row in sheet.iter_rows(values_only=True):
                    row_data = [str(cell) if cell is not None else "" for cell in row]
                    text.append("\t".join(row_data))

                text.append("")  # 空行分隔

            return '\n'.join(text)
        except ImportError:
            return ""