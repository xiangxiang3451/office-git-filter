#!/usr/bin/env python3
"""
设置Git配置以使用文档过滤器
"""

import os
import subprocess
import sys


def setup_git_config():
    """设置Git配置"""

    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    diff_wrapper = os.path.join(script_dir, "git_diff_wrapper.py")

    # 设置Git属性
    gitattributes = """
# Office文档过滤器配置
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

    # 写入.gitattributes文件
    with open('.gitattributes', 'w') as f:
        f.write(gitattributes)

    # 设置Git diff配置
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

    # 类似的配置其他格式...
    print("Git配置已完成！")
    print("请确保将.gitattributes文件添加到版本控制中")


if __name__ == "__main__":
    setup_git_config()