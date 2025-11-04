#!/usr/bin/env python3
"""
Git diff包装器，用于处理各种文档格式的差异比较
Git textconv 只传递一个参数：当前文件路径
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from filters.factory import FilterFactory
except ImportError as e:
    print(f"导入错误: {e}")
    print("请安装依赖: pip install -r requirements.txt")
    sys.exit(1)


def main():
    # Git textconv 只传递一个参数：要转换的文件路径
    if len(sys.argv) != 2:
        print("错误: 需要 exactly 1 个参数 (文件路径)")
        print("用法: git_diff_wrapper.py <文件路径>")
        print(f"接收到参数: {sys.argv}")
        sys.exit(1)

    file_path = sys.argv[1]

    # 规范化Windows路径
    file_path = os.path.normpath(file_path)

    print(f"处理文件: {file_path}", file=sys.stderr)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"[文件不存在: {file_path}]")
        sys.exit(0)

    factory = FilterFactory()

    try:
        text_content = factory.convert_to_text(file_path)
        # 输出文本内容到stdout（Git会捕获这个输出）
        print(text_content)
    except Exception as e:
        print(f"[错误处理文件 {file_path}: {str(e)}]")
        sys.exit(1)


if __name__ == "__main__":
    main()