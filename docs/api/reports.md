# Report Generation API Reference

The Report Generation module provides professional Markdown formatting, automated report scheduling, and comprehensive report management capabilities.

## Installation

```python
from perplSDK.reports.formatter import MarkdownFormatter
from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency
```

## MarkdownFormatter Class

### Initialization

```python
formatter = MarkdownFormatter()
```

## Formatting Methods

### `format_research_report(project_name, results, metadata=None, include_sources=True, include_citations=True)`

Format research results as a comprehensive Markdown report.

**Parameters:**
- `project_name` (str): Name of the research project
- `results` (List[SearchResult]): List of search results
- `metadata` (Optional[Dict]): Additional metadata
  - `description`: Project description
  - `total_queries`: Number of queries
  - `analysis_type`: Type of analysis
- `include_sources` (bool): Whether to include sources section
- `include_citations` (bool): Whether to include citations

**Returns:**
- `str`: Formatted Markdown report

**Example:**

```python
report = formatter.format_research_report(
    project_name="EV Market Analysis",
    results=research_results,
    metadata={
        "description": "Q4 2024 EV market research",
        "analysis_type": "Market Research"
    }
)
```

### `format_trend_report(trends, report_title="Trend Analysis Report", include_detailed_analysis=True)`

Format trend analysis as a Markdown report.

**Parameters:**
- `trends` (List[Dict]): List of trend data
- `report_title` (str): Report title
- `include_detailed_analysis` (bool): Include detailed trend analysis

**Returns:**
- `str`: Formatted Markdown report

**Example:**

```python
report = formatter.format_trend_report(
    trends=detected_trends,
    report_title="EV Trend Analysis Q4 2024",
    include_detailed_analysis=True
)
```

### `format_market_intelligence_report(analysis_results, sector)`

Format market intelligence analysis as a report.

**Parameters:**
- `analysis_results` (Dict): Analysis results from MarketIntelligence
- `sector` (MarketSector): Market sector analyzed

**Returns:**
- `str`: Formatted Markdown report

**Example:**

```python
from perplSDK.research.market_intelligence import MarketSector

report = formatter.format_market_intelligence_report(
    analysis_results=analysis,
    sector=MarketSector.ELECTRIC_VEHICLES
)
```

### `save_report(content, filename, output_dir=None)`

Save a report to file.

**Parameters:**
- `content` (str): Report content
- `filename` (str): Output filename (without extension)
- `output_dir` (Optional[str]): Output directory (defaults to config)

**Returns:**
- `str`: Path to saved report file

**Example:**

```python
report_path = formatter.save_report(
    content=report,
    filename="ev_analysis_2024",
    output_dir="./reports"
)
print(f"Report saved to: {report_path}")
```

## ReportScheduler Class

### Initialization

```python
scheduler = ReportScheduler(config=None)
```

**Parameters:**
- `config` (Optional[Config]): Configuration object

## Report Types

```python
class ReportType(Enum):
    RESEARCH = "research"
    MARKET_INTELLIGENCE = "market_intelligence"
    TREND_ANALYSIS = "trend_analysis"
    CUSTOM = "custom"
```

## Report Frequency

```python
class ReportFrequency(Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"
```

## Scheduling Methods

### `schedule_report(name, report_type, frequency, config, custom_schedule=None, publish_to_github=False, github_config=None)`

Schedule a recurring report.

**Parameters:**
- `name` (str): Report name
- `report_type` (ReportType): Type of report
- `frequency` (ReportFrequency): Report frequency
- `config` (Dict): Report configuration
  - For research reports: `project_name`, `queries`
  - For market intelligence: `sector`, `analysis_type`
  - For trend analysis: `industry`, `min_confidence`
- `custom_schedule` (Optional[str]): Cron-style schedule for custom frequency
- `publish_to_github` (bool): Whether to publish to GitHub
- `github_config` (Optional[Dict]): GitHub publishing configuration

**Returns:**
- `str`: Report ID

**Example:**

```python
# Schedule weekly market intelligence report
report_id = scheduler.schedule_report(
    name="Weekly EV Market Report",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.WEEKLY,
    config={
        "sector": "electric_vehicles",
        "analysis_type": "comprehensive"
    },
    publish_to_github=True
)
```

### `start_scheduler()`

Start the report scheduler in a background thread.

**Example:**

```python
scheduler.start_scheduler()
print("Scheduler started")
```

### `stop_scheduler()`

Stop the report scheduler.

**Example:**

```python
scheduler.stop_scheduler()
print("Scheduler stopped")
```

## Report Management

### `list_scheduled_reports()`

List all scheduled reports.

**Returns:**
- `List[Dict]`: List of scheduled report details

**Example:**

```python
reports = scheduler.list_scheduled_reports()
for report in reports:
    print(f"{report['name']}: {report['frequency']}")
```

### `get_report_status(report_id)`

Get status of a specific report.

**Parameters:**
- `report_id` (str): Report ID

**Returns:**
- `Optional[Dict]`: Report status information

**Example:**

```python
status = scheduler.get_report_status(report_id)
print(f"Last run: {status['last_run']}")
print(f"Next run: {status['next_run']}")
```

### `enable_report(report_id)`

Enable a scheduled report.

**Parameters:**
- `report_id` (str): Report ID

**Returns:**
- `bool`: Success status

### `disable_report(report_id)`

Disable a scheduled report.

**Parameters:**
- `report_id` (str): Report ID

**Returns:**
- `bool`: Success status

### `delete_report(report_id)`

Delete a scheduled report.

**Parameters:**
- `report_id` (str): Report ID

**Returns:**
- `bool`: Success status

### `run_report_now(report_id)`

Execute a report immediately.

**Parameters:**
- `report_id` (str): Report ID

**Returns:**
- `Dict[str, Any]`: Execution results

**Example:**

```python
result = scheduler.run_report_now(report_id)
print(f"Report generated: {result['report_path']}")
```

## Advanced Features

### Custom Schedule

```python
# Schedule report with custom cron expression
report_id = scheduler.schedule_report(
    name="Custom Report",
    report_type=ReportType.RESEARCH,
    frequency=ReportFrequency.CUSTOM,
    custom_schedule="0 9 * * MON",  # Every Monday at 9 AM
    config={"project_name": "Weekly Research"}
)
```

### GitHub Integration

```python
# Schedule with GitHub publishing
report_id = scheduler.schedule_report(
    name="Weekly EV Report",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.WEEKLY,
    config={"sector": "electric_vehicles"},
    publish_to_github=True,
    github_config={
        "file_path": "reports/weekly_ev_report.md",
        "commit_message": "Weekly EV market report",
        "create_pr": False
    }
)
```

### Report Templates

```python
# Research report template
research_config = {
    "project_name": "EV Research",
    "queries": [
        "EV market trends",
        "Battery innovations",
        "Charging infrastructure"
    ]
}

# Market intelligence template
market_config = {
    "sector": "electric_vehicles",
    "analysis_type": "comprehensive",
    "time_frame": "current",
    "geographic_focus": "global"
}

# Trend analysis template
trend_config = {
    "industry": "electric_vehicles",
    "time_period": "quarterly",
    "min_confidence": 0.7
}
```

## Best Practices

1. **Descriptive Names**: Use clear, descriptive report names
2. **Appropriate Frequency**: Choose frequency based on data volatility
3. **Enable Persistence**: Save scheduler state for recovery
4. **Monitor Execution**: Check report status regularly
5. **GitHub Publishing**: Use for team collaboration
6. **Error Handling**: Implement error handling for scheduled reports

## Examples

### Complete Report Generation Workflow

```python
from perplSDK import ResearchAutomation
from perplSDK.reports.formatter import MarkdownFormatter

# Conduct research
research = ResearchAutomation()
project = research.create_project("EV Analysis")
project.add_query("Latest EV trends")
research.conduct_research(project.name)

# Format report
formatter = MarkdownFormatter()
report = formatter.format_research_report(
    project_name=project.name,
    results=project.results,
    metadata={"total_queries": len(project.queries)}
)

# Save report
report_path = formatter.save_report(report, "ev_analysis")
print(f"Report saved to: {report_path}")
```

### Automated Report Scheduling

```python
from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency

# Initialize scheduler
scheduler = ReportScheduler()

# Schedule daily trend analysis
trend_report = scheduler.schedule_report(
    name="Daily EV Trends",
    report_type=ReportType.TREND_ANALYSIS,
    frequency=ReportFrequency.DAILY,
    config={
        "industry": "electric_vehicles",
        "time_period": "current",
        "min_confidence": 0.7
    }
)

# Schedule weekly market intelligence
market_report = scheduler.schedule_report(
    name="Weekly Market Report",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.WEEKLY,
    config={
        "sector": "electric_vehicles",
        "analysis_type": "comprehensive"
    },
    publish_to_github=True
)

# Start scheduler
scheduler.start_scheduler()

# Check status
status = scheduler.get_report_status(market_report)
print(f"Next run: {status['next_run']}")
```

### Multi-Report Dashboard

```python
# Schedule multiple reports
reports = [
    {
        "name": "Daily Trends",
        "type": ReportType.TREND_ANALYSIS,
        "frequency": ReportFrequency.DAILY
    },
    {
        "name": "Weekly Market",
        "type": ReportType.MARKET_INTELLIGENCE,
        "frequency": ReportFrequency.WEEKLY
    },
    {
        "name": "Monthly Research",
        "type": ReportType.RESEARCH,
        "frequency": ReportFrequency.MONTHLY
    }
]

for report_def in reports:
    report_id = scheduler.schedule_report(
        name=report_def["name"],
        report_type=report_def["type"],
        frequency=report_def["frequency"],
        config={"sector": "electric_vehicles"}
    )
    print(f"Scheduled: {report_def['name']} ({report_id})")

# Start scheduler
scheduler.start_scheduler()

# Monitor all reports
all_reports = scheduler.list_scheduled_reports()
for report in all_reports:
    print(f"{report['name']}: {report['enabled']}")
```

## See Also

- [PerplexityClient API](client.md)
- [Research Automation](research.md)
- [GitHub Integration](github.md)
- [Configuration Guide](../guides/configuration.md)
