import os
from .base_filter import BaseFilter
from .pdf_filter import PDFFilter
from .office_filter import OfficeFilter
from .text_filter import TextFilter


class FilterFactory:
    """过滤器工厂类"""

    def __init__(self):
        self.filters = [
            PDFFilter(),
            OfficeFilter(),
            TextFilter()
        ]

    def get_filter(self, file_path: str) -> BaseFilter:
        """获取适合文件的过滤器"""
        for filter_obj in self.filters:
            if filter_obj.can_handle(file_path):
                return filter_obj

        # 默认返回文本过滤器
        return TextFilter()

    def convert_to_text(self, file_path: str) -> str:
        """转换文件为文本"""
        if not os.path.exists(file_path):
            return f"[文件不存在: {file_path}]"

        filter_obj = self.get_filter(file_path)
        return filter_obj.to_text(file_path)