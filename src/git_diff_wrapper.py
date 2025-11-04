#!/usr/bin/env python3
"""
Git diff包装器，用于处理各种文档格式的差异比较
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filters.factory import FilterFactory


def main():
    if len(sys.argv) < 3:
        print("用法: git_diff_wrapper.py <旧文件> <新文件>")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]

    factory = FilterFactory()

    # 转换文件为文本
    old_text = factory.convert_to_text(old_file) if os.path.exists(old_file) else ""
    new_text = factory.convert_to_text(new_file) if os.path.exists(new_file) else ""

    # 输出差异（这里让git处理实际的diff）
    # 这个脚本主要用于git配置中的diff wrapper
    print(f"旧文件内容:\n{old_text}")
    print(f"\n新文件内容:\n{new_text}")


if __name__ == "__main__":
    main()