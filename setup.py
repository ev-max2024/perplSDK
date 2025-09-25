"""Setup script for perplSDK - Python SDK for Perplexity API automation."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="perplSDK",
    version="0.1.0",
    author="EV MAX INC",
    author_email="dev@evmax.com",
    description="A Python SDK for automating research, market intelligence, and AI-powered reporting using Perplexity API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ev-max2024/perplSDK",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "schedule>=1.2.0",
        "PyGithub>=1.59.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "aiohttp>=3.9.4",
        "markdown>=3.5.0",
        "jinja2>=3.1.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "perpl-research=perplSDK.cli:main",
        ],
    },
)