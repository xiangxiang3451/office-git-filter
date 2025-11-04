#!/usr/bin/env python3
"""
Set up Git configuration to use document filters
"""

import os
import subprocess
import sys


def setup_git_config():
    """Configure Git settings"""

    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    diff_wrapper = os.path.join(script_dir, "git_diff_wrapper.py")

    # Set Git attributes
    gitattributes = """
# Office document filter configuration
*.pdf diff=pdf
*.doc diff=doc
*.docx diff=docx
*.xls diff=xls
*.xlsx diff=xlsx
*.ppt diff=ppt
*.pptx diff=pptx
*.odt diff=odt
*.ods diff=ods
*.odp diff=odp
"""

    # Write .gitattributes file
    with open('.gitattributes', 'w') as f:
        f.write(gitattributes)

    # Configure Git diff settings
    subprocess.run([
        'git', 'config', 'diff.pdf.textconv',
        f'python "{diff_wrapper}"'
    ])
    subprocess.run([
        'git', 'config', 'diff.xlsx.textconv',
        f'python "{diff_wrapper}"'
    ])
    subprocess.run([
        'git', 'config', 'diff.pptx.textconv',
        f'python "{diff_wrapper}"'
    ])

    # Similar configuration for other formats...
    print("Git configuration completed!")
    print("Please make sure to add the .gitattributes file to version control")


if __name__ == "__main__":
    setup_git_config()