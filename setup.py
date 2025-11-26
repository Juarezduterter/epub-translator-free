"""
Setup script for ePub Translator
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="epub-translator-free",
    version="1.0.0",
    author="ePub Translator Contributors",
    description="Free and open-source ePub translation tool using HuggingFace models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/epub-translator-free",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "sentencepiece>=0.1.99",
        "sacremoses>=0.0.53",
        "protobuf>=3.20.0",
        "ebooklib>=0.18",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "tqdm>=4.65.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
        "accelerate>=0.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "epub-translate=translate:main",
        ],
    },
    keywords="epub translation huggingface marian nllb m2m100 ebook",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/epub-translator-free/issues",
        "Source": "https://github.com/yourusername/epub-translator-free",
    },
)
