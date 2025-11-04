import os
from .base_filter import BaseFilter
from .pdf_filter import PDFFilter
from .office_filter import OfficeFilter
from .text_filter import TextFilter


class FilterFactory:
    """Filter factory class"""

    def __init__(self):
        self.filters = [
            PDFFilter(),
            OfficeFilter(),
            TextFilter()
        ]

    def get_filter(self, file_path: str) -> BaseFilter:
        """Get appropriate filter for the file"""
        for filter_obj in self.filters:
            if filter_obj.can_handle(file_path):
                return filter_obj

        # Return text filter by default
        return TextFilter()

    def convert_to_text(self, file_path: str) -> str:
        """Convert file to text"""
        if not os.path.exists(file_path):
            return f"[File does not exist: {file_path}]"

        filter_obj = self.get_filter(file_path)
        return filter_obj.to_text(file_path)