import os
import subprocess
from .base_filter import BaseFilter

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


class PDFFilter(BaseFilter):
    """PDF file filter"""

    def __init__(self):
        super().__init__()
        self.supported_formats = ['.pdf']

    def to_text(self, file_path: str) -> str:
        """Extract PDF text content"""
        text = ""

        # Method 1: Use pdftotext
        text = self._use_pdftotext(file_path)
        if text:
            return text

        # Method 2: Use PyPDF2
        if PyPDF2:
            text = self._use_pypdf2(file_path)

        return text or f"[PDF file: {os.path.basename(file_path)}]"

    def _use_pdftotext(self, file_path: str) -> str:
        """Use pdftotext tool"""
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', file_path, '-'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def _use_pypdf2(self, file_path: str) -> str:
        """Use PyPDF2 library"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception:
            return ""