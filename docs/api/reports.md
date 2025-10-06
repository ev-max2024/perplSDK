# Report Generation API

The Report Generation module provides tools for formatting research results, creating professional reports, and scheduling automated report generation.

## Overview

Report generation features:
- Multiple output formats (Markdown, HTML, PDF)
- Customizable report templates
- Research result formatting
- Market intelligence reports
- Trend analysis reports
- Automated report scheduling
- GitHub integration for publishing

## Installation

```python
from perplSDK.reports.formatter import MarkdownFormatter, HTMLFormatter
from perplSDK.reports.scheduler import ReportScheduler
```

## MarkdownFormatter

Format reports in Markdown format with rich formatting options.

### Initialization

```python
formatter = MarkdownFormatter()
```

### Methods

#### format_research_report()

Format research results into a comprehensive report.

```python
def format_research_report(
    project_name: str,
    results: List[SearchResult],
    metadata: Optional[Dict[str, Any]] = None,
    include_sources: bool = True,
    include_citations: bool = True
) -> str
```

**Parameters:**
- `project_name` (str): Name of the research project
- `results` (List[SearchResult]): Research results to format
- `metadata` (Dict, optional): Additional report metadata
- `include_sources` (bool): Include source URLs (default: True)
- `include_citations` (bool): Include detailed citations (default: True)

**Returns:**
- `str`: Formatted Markdown report

**Example:**
```python
from perplSDK.research.automation import ResearchAutomation
from perplSDK.reports.formatter import MarkdownFormatter

# Conduct research
research = ResearchAutomation()
project = research.create_project("EV Analysis")
project.add_query("Current EV market trends")
project = research.conduct_research(project.name)

# Format report
formatter = MarkdownFormatter()
report = formatter.format_research_report(
    project_name=project.name,
    results=project.results,
    metadata={
        "author": "EV MAX Research Team",
        "date": "2024-12-01",
        "version": "1.0"
    }
)

print(report)
```

#### format_market_intelligence_report()

Format market intelligence analysis into a report.

```python
def format_market_intelligence_report(
    analysis: Dict[str, Any],
    title: str = "Market Intelligence Report",
    include_recommendations: bool = True
) -> str
```

**Parameters:**
- `analysis` (Dict): Market intelligence analysis results
- `title` (str): Report title
- `include_recommendations` (bool): Include strategic recommendations

**Returns:**
- `str`: Formatted Markdown report

**Example:**
```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

market_intel = MarketIntelligence()
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive"
)

formatter = MarkdownFormatter()
report = formatter.format_market_intelligence_report(
    analysis=analysis,
    title="Q4 2024 EV Market Intelligence",
    include_recommendations=True
)
```

#### format_trend_report()

Format trend analysis into a report.

```python
def format_trend_report(
    trends: List[Dict[str, Any]],
    title: str = "Trend Analysis Report",
    include_momentum: bool = True
) -> str
```

**Parameters:**
- `trends` (List[Dict]): Trend analysis results
- `title` (str): Report title
- `include_momentum` (bool): Include momentum metrics

**Returns:**
- `str`: Formatted Markdown report

**Example:**
```python
from perplSDK.research.trend_monitor import TrendMonitor

trend_monitor = TrendMonitor()
trends = trend_monitor.detect_emerging_trends(
    search_domains=["electric vehicles", "battery technology"],
    time_window="month"
)

formatter = MarkdownFormatter()
report = formatter.format_trend_report(
    trends=trends,
    title="Monthly EV Technology Trends"
)
```

#### save_report()

Save a formatted report to a file.

```python
def save_report(
    report: str,
    filename: str,
    output_dir: Optional[str] = None
) -> str
```

**Parameters:**
- `report` (str): Formatted report content
- `filename` (str): Output filename (without extension)
- `output_dir` (str, optional): Output directory path

**Returns:**
- `str`: Path to saved report file

**Example:**
```python
report_path = formatter.save_report(
    report=report,
    filename="ev_market_analysis_2024",
    output_dir="./reports"
)
print(f"Report saved to: {report_path}")
```

### Formatting Utilities

#### create_table()

Create a formatted Markdown table.

```python
def create_table(
    headers: List[str],
    rows: List[List[str]],
    alignment: Optional[List[str]] = None
) -> str
```

**Example:**
```python
table = formatter.create_table(
    headers=["Company", "Market Share", "Growth Rate"],
    rows=[
        ["Tesla", "23%", "+15%"],
        ["BYD", "18%", "+25%"],
        ["Volkswagen", "12%", "+8%"]
    ],
    alignment=["left", "center", "center"]
)
print(table)
```

#### create_collapsible_section()

Create a collapsible section in Markdown.

```python
def create_collapsible_section(
    title: str,
    content: str
) -> str
```

**Example:**
```python
section = formatter.create_collapsible_section(
    title="Detailed Data",
    content="This section contains detailed analysis..."
)
```

#### add_executive_summary()

Add an executive summary section to a report.

```python
def add_executive_summary(
    report: str,
    key_points: List[str]
) -> str
```

**Example:**
```python
key_points = [
    "EV market grew 35% year-over-year",
    "Battery costs decreased by 15%",
    "Charging infrastructure expanded by 40%"
]

report = formatter.add_executive_summary(report, key_points)
```

## ReportScheduler

Schedule automated report generation and distribution.

### Initialization

```python
from perplSDK.core.config import Config

config = Config.from_env()
scheduler = ReportScheduler(config)
```

### Methods

#### schedule_report()

Schedule a recurring report.

```python
def schedule_report(
    name: str,
    report_type: str,
    frequency: str,
    config: Dict[str, Any],
    output_dir: Optional[str] = None,
    publish_to_github: bool = False
) -> str
```

**Parameters:**
- `name` (str): Report name
- `report_type` (str): Type of report ("research", "market_intelligence", "trend_analysis")
- `frequency` (str): How often to generate ("daily", "weekly", "monthly")
- `config` (Dict): Report configuration
- `output_dir` (str, optional): Output directory
- `publish_to_github` (bool): Automatically publish to GitHub

**Returns:**
- `str`: Report ID

**Example:**
```python
report_id = scheduler.schedule_report(
    name="Weekly EV Trends",
    report_type="trend_analysis",
    frequency="weekly",
    config={
        "domains": ["electric vehicles", "battery technology"],
        "time_window": "week",
        "min_momentum": 0.6
    },
    publish_to_github=True
)
```

#### start_scheduler()

Start the report scheduler.

```python
def start_scheduler():
    """Start executing scheduled reports."""
```

**Example:**
```python
# Schedule multiple reports
scheduler.schedule_report(...)
scheduler.schedule_report(...)

# Start the scheduler (runs in background)
scheduler.start_scheduler()
```

#### list_scheduled_reports()

List all scheduled reports.

```python
def list_scheduled_reports() -> List[Dict[str, Any]]
```

**Example:**
```python
reports = scheduler.list_scheduled_reports()
for report in reports:
    print(f"{report['name']}: {report['frequency']}")
```

#### cancel_report()

Cancel a scheduled report.

```python
def cancel_report(report_id: str) -> bool
```

**Example:**
```python
success = scheduler.cancel_report(report_id)
if success:
    print("Report cancelled")
```

## Complete Workflow Examples

### Basic Report Generation

```python
from perplSDK.research.automation import ResearchAutomation
from perplSDK.reports.formatter import MarkdownFormatter

# Conduct research
research = ResearchAutomation()
project = research.create_project("EV Technology Analysis")
project.add_query("Latest EV battery innovations")
project.add_query("EV charging infrastructure developments")
project = research.conduct_research(project.name)

# Format and save report
formatter = MarkdownFormatter()
report = formatter.format_research_report(
    project_name=project.name,
    results=project.results,
    metadata={
        "author": "Research Team",
        "department": "Technology Analysis"
    }
)

report_path = formatter.save_report(report, "ev_tech_analysis")
print(f"Report saved: {report_path}")
```

### Market Intelligence Report

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector
from perplSDK.reports.formatter import MarkdownFormatter

# Conduct market analysis
market_intel = MarketIntelligence()
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive",
    geographic_focus="north_america"
)

# Create formatted report
formatter = MarkdownFormatter()
report = formatter.format_market_intelligence_report(
    analysis=analysis,
    title="North America EV Market Intelligence - Q4 2024"
)

# Add executive summary
key_findings = [
    "Market size reached $X billion with 35% YoY growth",
    "Tesla maintains leadership at 23% market share",
    "Charging infrastructure investment increased 40%",
    "Battery costs decreased 15% year-over-year"
]
report = formatter.add_executive_summary(report, key_findings)

# Save report
formatter.save_report(report, "na_ev_market_q4_2024")
```

### Automated Scheduled Reports

```python
from perplSDK.reports.scheduler import ReportScheduler
from perplSDK.core.config import Config

# Initialize scheduler
config = Config.from_env()
scheduler = ReportScheduler(config)

# Schedule daily trend report
daily_trends = scheduler.schedule_report(
    name="Daily EV Trends",
    report_type="trend_analysis",
    frequency="daily",
    config={
        "domains": ["electric vehicles"],
        "time_window": "day"
    },
    output_dir="./reports/daily"
)

# Schedule weekly market intelligence
weekly_market = scheduler.schedule_report(
    name="Weekly Market Intelligence",
    report_type="market_intelligence",
    frequency="weekly",
    config={
        "sector": "electric_vehicles",
        "analysis_type": "quick"
    },
    publish_to_github=True
)

# Schedule monthly comprehensive report
monthly_comprehensive = scheduler.schedule_report(
    name="Monthly Comprehensive Analysis",
    report_type="market_intelligence",
    frequency="monthly",
    config={
        "sector": "electric_vehicles",
        "analysis_type": "comprehensive",
        "geographic_focus": "global"
    },
    publish_to_github=True
)

# Start scheduler
scheduler.start_scheduler()
print("Scheduler started. Reports will be generated automatically.")
```

### Multi-Format Reports

```python
from perplSDK.reports.formatter import MarkdownFormatter, HTMLFormatter

# Generate Markdown version
md_formatter = MarkdownFormatter()
md_report = md_formatter.format_research_report(
    project_name="EV Analysis",
    results=results
)
md_formatter.save_report(md_report, "report_markdown")

# Generate HTML version
html_formatter = HTMLFormatter()
html_report = html_formatter.format_research_report(
    project_name="EV Analysis",
    results=results
)
html_formatter.save_report(html_report, "report_html")
```

### Custom Report Template

```python
from perplSDK.reports.formatter import MarkdownFormatter

formatter = MarkdownFormatter()

# Custom report structure
report = f"""# Custom Research Report

## Executive Summary
{executive_summary}

## Methodology
{methodology}

## Key Findings
{findings}

## Detailed Analysis
{analysis}

## Recommendations
{recommendations}

## Appendix
{appendix}
"""

formatter.save_report(report, "custom_report")
```

## Advanced Features

### Report Templates

```python
# Use custom template
template = """
# {title}

**Date:** {date}
**Author:** {author}

## Overview
{overview}

## Analysis
{analysis}

## Conclusions
{conclusions}
"""

report = template.format(
    title="EV Market Analysis",
    date="2024-12-01",
    author="Research Team",
    overview=overview_text,
    analysis=analysis_text,
    conclusions=conclusions_text
)
```

### Conditional Content

```python
# Include sections based on conditions
report = formatter.format_research_report(
    project_name="Analysis",
    results=results,
    include_sources=True if len(results) < 10 else False,
    include_citations=detailed_mode
)
```

### Report Aggregation

```python
# Combine multiple reports
daily_reports = []
for day in range(7):
    report = generate_daily_report(day)
    daily_reports.append(report)

weekly_summary = formatter.aggregate_reports(
    reports=daily_reports,
    title="Weekly Summary"
)
```

## Integration with GitHub

### Automatic Publishing

```python
from perplSDK.github_integration.publisher import GitHubPublisher
from perplSDK.reports.formatter import MarkdownFormatter

# Generate report
formatter = MarkdownFormatter()
report = formatter.format_research_report(...)
report_path = formatter.save_report(report, "latest_analysis")

# Publish to GitHub
github = GitHubPublisher()
result = github.publish_file(
    local_file_path=report_path,
    github_file_path="reports/latest_analysis.md",
    commit_message="Update latest analysis report"
)
```

### Scheduled GitHub Publishing

```python
# Schedule with automatic GitHub publishing
scheduler.schedule_report(
    name="Weekly Report",
    report_type="market_intelligence",
    frequency="weekly",
    config={...},
    publish_to_github=True
)
```

## Best Practices

### 1. Use Appropriate Report Types

```python
# Quick updates - trend reports
trend_report = formatter.format_trend_report(trends)

# Strategic planning - market intelligence reports
market_report = formatter.format_market_intelligence_report(analysis)

# Detailed research - research reports
research_report = formatter.format_research_report(project.name, results)
```

### 2. Include Metadata

```python
metadata = {
    "author": "Research Team",
    "department": "Market Intelligence",
    "version": "2.1",
    "classification": "Internal",
    "date": datetime.now().isoformat(),
    "stakeholders": ["Engineering", "Marketing", "Executive"]
}

report = formatter.format_research_report(
    project_name="Analysis",
    results=results,
    metadata=metadata
)
```

### 3. Structure Reports Consistently

```python
# Follow consistent structure
# 1. Title and metadata
# 2. Executive summary
# 3. Main content
# 4. Recommendations
# 5. Appendix/sources
```

### 4. Optimize for Different Audiences

```python
# Executive summary for leadership
exec_report = formatter.format_executive_summary(analysis)

# Detailed technical report for teams
technical_report = formatter.format_research_report(
    project.name,
    results,
    include_sources=True,
    include_citations=True
)
```

## See Also

- [Research Automation](research.md)
- [Market Intelligence](market_intelligence.md)
- [GitHub Integration](github.md)
- [Automated Workflows Guide](../guides/automation.md)
