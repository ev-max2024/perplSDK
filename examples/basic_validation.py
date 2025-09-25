#!/usr/bin/env python3
"""
Basic validation script to test perplSDK functionality without API keys.

This script validates the SDK structure and basic operations that don't
require external API calls.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from perplSDK.core.config import Config
from perplSDK.research.automation import ResearchAutomation, ResearchProject
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector
from perplSDK.research.trend_monitor import TrendMonitor
from perplSDK.reports.formatter import MarkdownFormatter
from perplSDK.reports.scheduler import ReportScheduler
from perplSDK.utils.templates import ResearchTemplate
from perplSDK.utils.formatters import TextFormatter


def test_configuration():
    """Test configuration management."""
    print("🔧 Testing Configuration Management...")
    
    # Test basic config creation
    config = Config(
        perplexity_api_key="test-key",
        github_token="test-github-token",
        github_repo="test/repo"
    )
    
    assert config.perplexity_api_key == "test-key"
    assert config.github_token == "test-github-token"
    assert config.api_rate_limit == 60  # Default value
    
    print("   ✅ Configuration creation and defaults work")
    
    # Test validation
    try:
        config.validate_required_fields()
        print("   ✅ Configuration validation passes")
    except Exception as e:
        print(f"   ❌ Configuration validation failed: {e}")
        return False
    
    return True


def test_research_automation():
    """Test research automation without API calls."""
    print("📚 Testing Research Automation...")
    
    config = Config(perplexity_api_key="test-key")
    research = ResearchAutomation(config)
    
    # Test project creation
    project = research.create_project("Test Project", "Test description")
    assert project.name == "Test Project"
    assert project.description == "Test description"
    print("   ✅ Project creation works")
    
    # Test query addition
    project.add_query("Test query 1", category="test")
    project.add_query("Test query 2", category="test", priority=2)
    assert len(project.queries) == 2
    print("   ✅ Query addition works")
    
    # Test project retrieval
    retrieved = research.get_project("Test Project")
    assert retrieved is not None
    assert retrieved.name == "Test Project"
    print("   ✅ Project retrieval works")
    
    # Test research plan generation
    queries = research.generate_research_plan("electric vehicles")
    assert isinstance(queries, list)
    assert len(queries) > 0
    print(f"   ✅ Research plan generation works ({len(queries)} queries)")
    
    return True


def test_market_intelligence():
    """Test market intelligence structure."""
    print("📊 Testing Market Intelligence...")
    
    config = Config(perplexity_api_key="test-key")
    market_intel = MarketIntelligence(config)
    
    # Test sector enum
    assert MarketSector.ELECTRIC_VEHICLES.value == "electric_vehicles"
    assert MarketSector.BATTERY_TECHNOLOGY.value == "battery_technology"
    print("   ✅ Market sectors defined correctly")
    
    # Test query generation
    queries = market_intel.generate_market_queries(
        MarketSector.ELECTRIC_VEHICLES,
        analysis_type="trends",
        geographic_focus="north_america"
    )
    assert isinstance(queries, list)
    assert len(queries) > 0
    print(f"   ✅ Market query generation works ({len(queries)} queries)")
    
    # Test EV MAX focus areas
    assert len(market_intel.ev_max_focus_areas) > 0
    print(f"   ✅ EV MAX focus areas defined ({len(market_intel.ev_max_focus_areas)} areas)")
    
    return True


def test_trend_monitoring():
    """Test trend monitoring structure."""
    print("📈 Testing Trend Monitoring...")
    
    config = Config(perplexity_api_key="test-key")
    trend_monitor = TrendMonitor(config)
    
    # Test trend categories
    assert len(trend_monitor.ev_trend_categories) > 0
    print(f"   ✅ EV trend categories defined ({len(trend_monitor.ev_trend_categories)} categories)")
    
    # Test trend addition
    trend_monitor.add_trend_to_monitor("solid-state batteries", "battery_technology")
    assert len(trend_monitor.tracked_trends) == 1
    print("   ✅ Trend monitoring setup works")
    
    return True


def test_report_formatting():
    """Test report formatting capabilities."""
    print("📝 Testing Report Formatting...")
    
    formatter = MarkdownFormatter()
    
    # Test markdown table creation
    headers = ["Column 1", "Column 2", "Column 3"]
    rows = [
        ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
        ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
    ]
    
    table = formatter.create_table(headers, rows)
    assert "| Column 1 | Column 2 | Column 3 |" in table
    assert "| Row 1 Col 1 | Row 1 Col 2 | Row 1 Col 3 |" in table
    print("   ✅ Markdown table generation works")
    
    # Test collapsible section
    collapsible = formatter.create_collapsible_section("Test Title", "Test content")
    assert "<details>" in collapsible
    assert "<summary>Test Title</summary>" in collapsible
    assert "Test content" in collapsible
    print("   ✅ Collapsible section generation works")
    
    return True


def test_utilities():
    """Test utility functions."""
    print("🛠️ Testing Utilities...")
    
    # Test text formatter
    text_formatter = TextFormatter()
    
    # Test text cleaning
    dirty_text = "  This   is   a   test   text   with   extra   spaces  "
    clean_text = text_formatter.clean_content(dirty_text)
    assert clean_text == "This is a test text with extra spaces"
    print("   ✅ Text cleaning works")
    
    # Test key point extraction
    sample_text = "This is important information. This is significant data. This is critical analysis. Regular sentence here."
    key_points = text_formatter.extract_key_points(sample_text, max_points=2)
    assert len(key_points) <= 2
    print(f"   ✅ Key point extraction works ({len(key_points)} points)")
    
    # Test research templates
    template = ResearchTemplate()
    queries = template.generate_queries("electric vehicles", "comprehensive")
    assert isinstance(queries, list)
    assert len(queries) > 0
    print(f"   ✅ Research template generation works ({len(queries)} queries)")
    
    return True


def test_scheduler_structure():
    """Test report scheduler structure."""
    print("⏰ Testing Report Scheduler...")
    
    config = Config(perplexity_api_key="test-key")
    scheduler = ReportScheduler(config)
    
    # Test initial state
    reports = scheduler.list_scheduled_reports()
    assert isinstance(reports, list)
    assert len(reports) == 0
    print("   ✅ Scheduler initialization works")
    
    return True


def main():
    """Run basic validation tests."""
    print("🎯 perplSDK Basic Validation")
    print("=" * 50)
    print("Testing SDK functionality without external API calls...")
    print()
    
    tests = [
        ("Configuration", test_configuration),
        ("Research Automation", test_research_automation),
        ("Market Intelligence", test_market_intelligence),
        ("Trend Monitoring", test_trend_monitoring),
        ("Report Formatting", test_report_formatting),
        ("Utilities", test_utilities),
        ("Scheduler Structure", test_scheduler_structure),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} - ERROR: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All basic validation tests passed!")
        print("✅ perplSDK is ready for use with proper API keys")
        
        print("\n📋 Next Steps:")
        print("1. Set your PERPLEXITY_API_KEY environment variable")
        print("2. Optionally set GITHUB_TOKEN and GITHUB_REPO for GitHub integration")
        print("3. Run examples/comprehensive_demo.py for full functionality test")
        print("4. Explore examples/ev_max_market_intelligence.py for EV MAX INC workflows")
        
        return 0
    else:
        print("❌ Some validation tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())