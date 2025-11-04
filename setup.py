from setuptools import setup, find_packages

setup(
    name="office-git-filter",
    version="1.0.0",
    description="Universal Git filter for office documents",
    packages=find_packages(),
    install_requires=[
        "pypdf2>=3.0.0",
        "python-docx>=0.8.11",
        "openpyxl>=3.0.0",
        "python-magic>=0.4.27",
        "chardet>=4.0.0"
    ],
    entry_points={
        'console_scripts': [
            'office-filter=scripts.git_diff_wrapper:main',
        ],
    },
    python_requires='>=3.6',
)