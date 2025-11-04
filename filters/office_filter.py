import os
import subprocess
import tempfile
from .base_filter import BaseFilter
import sys

class OfficeFilter(BaseFilter):
    """Office document filter"""

    def __init__(self):
        super().__init__()
        self.supported_formats = [
            '.docx', '.xlsx','.pptx'
        ]

    def to_text(self, file_path: str) -> str:
        """Convert Office document to text"""
        ext = os.path.splitext(file_path)[1].lower()

        # Try using LibreOffice first
        text = self._use_libreoffice(file_path)
        if text:
            return text

        # Fallback methods for specific formats
        if ext == '.docx':
            return self._use_docx_library(file_path)
        elif ext == '.xlsx':
            return self._use_excel_library(file_path)
        elif ext == '.pptx':
            return self._use_pptx_library(file_path)

        return f"[Office file: {os.path.basename(file_path)}]"

    def _use_libreoffice(self, file_path: str) -> str:
        """Convert using LibreOffice"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Convert to text
                result = subprocess.run([
                    'soffice', '--headless', '--convert-to', 'txt:Text',
                    '--outdir', temp_dir, file_path
                ], capture_output=True, check=True)

                # Read converted file
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                txt_file = os.path.join(temp_dir, f"{base_name}.txt")

                if os.path.exists(txt_file):
                    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read().strip()

            return ""
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def _use_docx_library(self, file_path: str) -> str:
        """Process .docx files using python-docx"""
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
        """Process Excel files using openpyxl"""
        try:
            import openpyxl
            wb = openpyxl.load_workbook(file_path, data_only=True)
            text = []

            print(f"Debug: Processing Excel file {file_path}", file=sys.stderr)

            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                text.append(f"=== Worksheet: {sheet_name} ===")

                has_content = False
                for row_num, row in enumerate(sheet.iter_rows(values_only=True), 1):
                    # Filter None values and convert to strings
                    row_data = []
                    for cell in row:
                        if cell is not None:
                            cell_str = str(cell).strip()
                            if cell_str:  # Only add non-empty strings
                                row_data.append(cell_str)

                    if row_data:  # Only add non-empty rows
                        text.append(f"Row{row_num}: {' | '.join(row_data)}")
                        has_content = True

                if not has_content:
                    text.append("(Empty worksheet)")
                text.append("")  # Empty line separator

            result = '\n'.join(text)
            print(f"Debug: Excel conversion result length {len(result)}", file=sys.stderr)
            return result if result.strip() else f"[Excel file has no text content: {os.path.basename(file_path)}]"

        except ImportError:
            return f"[openpyxl library not installed: {os.path.basename(file_path)}]"
        except Exception as e:
            return f"[Failed to process Excel file: {str(e)}]"

    def _use_pptx_library(self, file_path: str) -> str:
        """Process PPTX files using python-pptx"""
        try:
            import pptx
            presentation = pptx.Presentation(file_path)
            text = []

            print(f"Debug: Processing PPTX file {file_path}", file=sys.stderr)

            for slide_num, slide in enumerate(presentation.slides, 1):
                text.append(f"=== Slide {slide_num} ===")

                has_content = False

                # Extract slide title
                if slide.shapes.title and slide.shapes.title.text.strip():
                    text.append(f"Title: {slide.shapes.title.text.strip()}")
                    has_content = True

                # Extract text from all shapes
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        # Skip title (already processed)
                        if shape != slide.shapes.title:
                            text.append(f"Content: {shape.text.strip()}")
                            has_content = True

                if not has_content:
                    text.append("(Empty slide)")
                text.append("")  # Empty line separator

            result = '\n'.join(text)
            print(f"Debug: PPTX conversion result length {len(result)}", file=sys.stderr)
            return result if result.strip() else f"[PPTX file has no text content: {os.path.basename(file_path)}]"

        except ImportError:
            return f"[python-pptx library not installed: {os.path.basename(file_path)}]"
        except Exception as e:
            return f"[Failed to process PPTX file: {str(e)}]"