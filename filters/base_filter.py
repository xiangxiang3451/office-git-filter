import os
import subprocess
import tempfile
from abc import ABC, abstractmethod
from typing import Optional


class BaseFilter(ABC):
    """Base filter abstract class"""

    def __init__(self):
        self.supported_formats = []

    @abstractmethod
    def to_text(self, file_path: str) -> Optional[str]:
        """Convert file to plain text"""
        pass

    def can_handle(self, file_path: str) -> bool:
        """Check if the file type is supported"""
        if not os.path.exists(file_path):
            return False

        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_formats

    def run_command(self, command: list) -> tuple:
        """Execute external command"""
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