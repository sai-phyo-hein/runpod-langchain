"""
Setup configuration for runpod-langchain package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="runpod-langchain",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="LangChain integration for RunPod serverless endpoints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/runpod-langchain",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain-core>=0.1.0",
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "python-dotenv>=1.0.0",
        ],
    },
    keywords="runpod langchain llm ai ml serverless",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/runpod-langchain/issues",
        "Source": "https://github.com/yourusername/runpod-langchain",
        "Documentation": "https://github.com/yourusername/runpod-langchain#readme",
    },
)