"""Tests for data export functionality."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from perplSDK.utils.data_export import (
    DataExporter,
    EXCEL_AVAILABLE,
    PDF_AVAILABLE,
    DOCX_AVAILABLE
)


@pytest.fixture
def exporter():
    """Create a DataExporter with a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield DataExporter(output_dir=tmpdir)


@pytest.fixture
def sample_data():
    """Sample data for testing exports."""
    return [
        {
            "title": "Test Insight 1",
            "content": "This is the first test insight with some content.",
            "impact_level": "high",
            "confidence_score": 0.85,
            "tags": ["technology", "innovation"]
        },
        {
            "title": "Test Insight 2",
            "content": "This is the second test insight.",
            "impact_level": "medium",
            "confidence_score": 0.72,
            "tags": ["market", "trends"]
        },
        {
            "title": "Test Insight 3",
            "content": "Third insight for testing purposes.",
            "impact_level": "low",
            "confidence_score": 0.65,
            "tags": ["research"]
        }
    ]


class TestDataExporter:
    """Test cases for DataExporter class."""

    def test_init_creates_output_dir(self):
        """Test that initialization creates the output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            export_dir = os.path.join(tmpdir, "exports")
            exporter = DataExporter(output_dir=export_dir)
            assert os.path.exists(export_dir)

    def test_get_available_formats(self, exporter):
        """Test getting available export formats."""
        formats = exporter.get_available_formats()
        
        assert "excel" in formats
        assert "pdf" in formats
        assert "docx" in formats
        assert "csv" in formats
        assert "json" in formats
        
        # CSV and JSON should always be available
        assert formats["csv"] is True
        assert formats["json"] is True


class TestCSVExport:
    """Test cases for CSV export functionality."""

    def test_export_to_csv_basic(self, exporter, sample_data):
        """Test basic CSV export."""
        filepath = exporter.export_to_csv(sample_data, "test_export")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".csv")
        
        # Verify content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "title" in content
            assert "Test Insight 1" in content

    def test_export_to_csv_empty_data(self, exporter):
        """Test CSV export with empty data."""
        filepath = exporter.export_to_csv([], "empty_export")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".csv")

    def test_export_to_csv_single_dict(self, exporter, sample_data):
        """Test CSV export with single dictionary."""
        filepath = exporter.export_to_csv(sample_data[0], "single_export")
        
        assert os.path.exists(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test Insight 1" in content

    def test_export_to_csv_custom_delimiter(self, exporter, sample_data):
        """Test CSV export with custom delimiter."""
        filepath = exporter.export_to_csv(
            sample_data, "custom_delimiter", delimiter=";"
        )
        
        assert os.path.exists(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            assert ";" in content

    def test_export_to_csv_no_header(self, exporter, sample_data):
        """Test CSV export without header."""
        filepath = exporter.export_to_csv(
            sample_data, "no_header", include_header=False
        )
        
        assert os.path.exists(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # First line should be data, not header
            assert "title" not in lines[0] or "Test Insight" in lines[0]


class TestJSONExport:
    """Test cases for JSON export functionality."""

    def test_export_to_json_basic(self, exporter, sample_data):
        """Test basic JSON export."""
        filepath = exporter.export_to_json(sample_data, "test_export")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".json")
        
        # Verify content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)
            assert "metadata" in content
            assert "data" in content
            assert len(content["data"]) == 3

    def test_export_to_json_without_metadata(self, exporter, sample_data):
        """Test JSON export without metadata wrapper."""
        filepath = exporter.export_to_json(
            sample_data, "no_metadata", include_metadata=False
        )
        
        assert os.path.exists(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)
            # Should be the data directly, not wrapped
            assert isinstance(content, list)
            assert len(content) == 3

    def test_export_to_json_single_dict(self, exporter, sample_data):
        """Test JSON export with single dictionary."""
        filepath = exporter.export_to_json(sample_data[0], "single_export")
        
        assert os.path.exists(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)
            assert "data" in content
            assert content["data"]["title"] == "Test Insight 1"


class TestExportInsights:
    """Test cases for export_insights method."""

    def test_export_insights_csv(self, exporter, sample_data):
        """Test exporting insights to CSV format."""
        filepath = exporter.export_insights(sample_data, "csv", "insights_csv")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".csv")

    def test_export_insights_json(self, exporter, sample_data):
        """Test exporting insights to JSON format."""
        filepath = exporter.export_insights(sample_data, "json", "insights_json")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".json")

    def test_export_insights_unsupported_format(self, exporter, sample_data):
        """Test exporting insights with unsupported format."""
        with pytest.raises(ValueError) as exc_info:
            exporter.export_insights(sample_data, "unsupported", "test")
        
        assert "Unsupported export format" in str(exc_info.value)


@pytest.mark.skipif(not EXCEL_AVAILABLE, reason="openpyxl not installed")
class TestExcelExport:
    """Test cases for Excel export functionality."""

    def test_export_to_excel_basic(self, exporter, sample_data):
        """Test basic Excel export."""
        filepath = exporter.export_to_excel(sample_data, "test_export")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".xlsx")

    def test_export_to_excel_without_metadata(self, exporter, sample_data):
        """Test Excel export without metadata sheet."""
        filepath = exporter.export_to_excel(
            sample_data, "no_metadata", include_metadata=False
        )
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".xlsx")

    def test_export_to_excel_custom_sheet_name(self, exporter, sample_data):
        """Test Excel export with custom sheet name."""
        filepath = exporter.export_to_excel(
            sample_data, "custom_sheet", sheet_name="Insights"
        )
        
        assert os.path.exists(filepath)


@pytest.mark.skipif(not PDF_AVAILABLE, reason="reportlab not installed")
class TestPDFExport:
    """Test cases for PDF export functionality."""

    def test_export_to_pdf_basic(self, exporter, sample_data):
        """Test basic PDF export."""
        filepath = exporter.export_to_pdf(sample_data, "test_export")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".pdf")

    def test_export_to_pdf_custom_title(self, exporter, sample_data):
        """Test PDF export with custom title."""
        filepath = exporter.export_to_pdf(
            sample_data, "custom_title", title="Custom Report Title"
        )
        
        assert os.path.exists(filepath)


@pytest.mark.skipif(not DOCX_AVAILABLE, reason="python-docx not installed")
class TestDOCXExport:
    """Test cases for DOCX export functionality."""

    def test_export_to_docx_basic(self, exporter, sample_data):
        """Test basic DOCX export."""
        filepath = exporter.export_to_docx(sample_data, "test_export")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".docx")

    def test_export_to_docx_custom_title(self, exporter, sample_data):
        """Test DOCX export with custom title."""
        filepath = exporter.export_to_docx(
            sample_data, "custom_title", title="Custom Report Title"
        )
        
        assert os.path.exists(filepath)


class TestExportResearchResults:
    """Test cases for exporting research results."""

    def test_export_research_results_dicts(self, exporter, sample_data):
        """Test exporting research results from dictionaries."""
        filepath = exporter.export_research_results(
            sample_data, "json", "research_results"
        )
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".json")

    def test_export_research_results_empty(self, exporter):
        """Test exporting empty research results."""
        filepath = exporter.export_research_results([], "csv", "empty_results")
        
        assert os.path.exists(filepath)
