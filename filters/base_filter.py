import os
import subprocess
import tempfile
from abc import ABC, abstractmethod
from typing import Optional


class BaseFilter(ABC):
    """基础过滤器抽象类"""

    def __init__(self):
        self.supported_formats = []

    @abstractmethod
    def to_text(self, file_path: str) -> Optional[str]:
        """将文件转换为纯文本"""
        pass

    def can_handle(self, file_path: str) -> bool:
        """检查是否支持该文件类型"""
        if not os.path.exists(file_path):
            return False

        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_formats

    def run_command(self, command: list) -> tuple:
        """运行外部命令"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout, None
        except subprocess.CalledProcessError as e:
            return None, f"Command failed: {e.stderr}"
        except FileNotFoundError:
            return None, "Command not found"