"""
perplSDK - Python SDK for automating AI-powered research using Perplexity API.

This SDK provides comprehensive tools for automating research, market intelligence,
and AI-powered reporting workflows for EV MAX INC and other organizations.
"""

__version__ = "0.1.0"
__author__ = "EV MAX INC"

from .core.client import PerplexityClient
from .research.automation import ResearchAutomation
from .reports.scheduler import ReportScheduler
from .reports.formatter import MarkdownFormatter
from .github_integration.publisher import GitHubPublisher
from .utils.data_export import DataExporter

__all__ = [
    "PerplexityClient",
    "ResearchAutomation", 
    "ReportScheduler",
    "MarkdownFormatter",
    "GitHubPublisher",
    "DataExporter",
]