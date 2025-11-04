#!/usr/bin/env python3
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from filters.factory import FilterFactory
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Error: Exactly 1 argument required (file path)")
        print("Usage: git_diff_wrapper.py <file_path>")
        print(f"Arguments received: {sys.argv}")
        sys.exit(1)

    file_path = sys.argv[1]

    file_path = os.path.normpath(file_path)

    print(f"Processing file: {file_path}", file=sys.stderr)

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"[File does not exist: {file_path}]")
        sys.exit(0)

    factory = FilterFactory()

    try:
        text_content = factory.convert_to_text(file_path)
        # Output text content to stdout (Git will capture this output)
        print(text_content)
    except Exception as e:
        print(f"[Error processing file {file_path}: {str(e)}]")
        sys.exit(1)


if __name__ == "__main__":
    main()