# Automated Workflows Guide

This guide covers setting up and managing automated research workflows, scheduled reports, and continuous monitoring with perplSDK.

## Overview

perplSDK provides comprehensive automation capabilities including:
- Scheduled report generation
- Continuous trend monitoring
- Automated GitHub publishing
- Workflow orchestration
- Custom scheduling

## Report Scheduling

### Basic Scheduling

```python
from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency

scheduler = ReportScheduler()

# Schedule daily report
report_id = scheduler.schedule_report(
    name="Daily EV Trends",
    report_type=ReportType.TREND_ANALYSIS,
    frequency=ReportFrequency.DAILY,
    config={
        "industry": "electric_vehicles",
        "time_period": "current",
        "min_confidence": 0.7
    }
)

# Start scheduler
scheduler.start_scheduler()
print(f"Scheduled report: {report_id}")
```

### Report Frequencies

```python
# Hourly reports (for high-frequency monitoring)
ReportFrequency.HOURLY

# Daily reports (morning briefings, daily digests)
ReportFrequency.DAILY

# Weekly reports (comprehensive market updates)
ReportFrequency.WEEKLY

# Monthly reports (in-depth analysis)
ReportFrequency.MONTHLY

# Custom schedule (using cron expressions)
ReportFrequency.CUSTOM
```

### Custom Schedules

Use cron expressions for precise scheduling:

```python
# Every Monday at 9 AM
scheduler.schedule_report(
    name="Weekly Market Report",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.CUSTOM,
    custom_schedule="0 9 * * MON",
    config={"sector": "electric_vehicles"}
)

# Every weekday at 6 AM
scheduler.schedule_report(
    name="Weekday Brief",
    report_type=ReportType.RESEARCH,
    frequency=ReportFrequency.CUSTOM,
    custom_schedule="0 6 * * MON-FRI",
    config={"project_name": "Daily Research"}
)

# First day of month at midnight
scheduler.schedule_report(
    name="Monthly Analysis",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.CUSTOM,
    custom_schedule="0 0 1 * *",
    config={"sector": "electric_vehicles"}
)
```

## Report Types

### Research Reports

Automated project-based research:

```python
scheduler.schedule_report(
    name="Weekly EV Research",
    report_type=ReportType.RESEARCH,
    frequency=ReportFrequency.WEEKLY,
    config={
        "project_name": "EV Weekly",
        "queries": [
            "Latest EV market developments",
            "Battery technology news",
            "Charging infrastructure updates"
        ]
    }
)
```

### Market Intelligence Reports

Comprehensive market analysis:

```python
scheduler.schedule_report(
    name="Market Intelligence",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.WEEKLY,
    config={
        "sector": "electric_vehicles",
        "analysis_type": "comprehensive",
        "time_frame": "current",
        "geographic_focus": "global"
    }
)
```

### Trend Analysis Reports

Emerging trend detection:

```python
scheduler.schedule_report(
    name="Trend Analysis",
    report_type=ReportType.TREND_ANALYSIS,
    frequency=ReportFrequency.DAILY,
    config={
        "industry": "electric_vehicles",
        "time_period": "current",
        "min_confidence": 0.7
    }
)
```

## GitHub Integration

### Automated Publishing

Publish reports directly to GitHub:

```python
scheduler.schedule_report(
    name="Weekly Market Report",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.WEEKLY,
    config={"sector": "electric_vehicles"},
    publish_to_github=True,
    github_config={
        "file_path": "reports/weekly_market.md",
        "commit_message": "Weekly market intelligence report",
        "create_pr": False
    }
)
```

### Pull Request Workflow

Create PRs for team review:

```python
scheduler.schedule_report(
    name="Monthly Analysis",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.MONTHLY,
    config={"sector": "electric_vehicles"},
    publish_to_github=True,
    github_config={
        "file_path": "reports/monthly_analysis.md",
        "commit_message": "Monthly market analysis",
        "create_pr": True,
        "pr_title": "Monthly Market Analysis",
        "pr_body": "Comprehensive monthly EV market intelligence report"
    }
)
```

## Managing Scheduled Reports

### List Reports

```python
reports = scheduler.list_scheduled_reports()
for report in reports:
    print(f"{report['name']}: {report['frequency']} - {report['enabled']}")
```

### Get Report Status

```python
status = scheduler.get_report_status(report_id)
print(f"Last Run: {status['last_run']}")
print(f"Next Run: {status['next_run']}")
print(f"Recent Executions: {len(status['recent_executions'])}")
```

### Enable/Disable Reports

```python
# Disable report temporarily
scheduler.disable_report(report_id)

# Re-enable report
scheduler.enable_report(report_id)
```

### Run Report Immediately

```python
# Execute report on-demand
result = scheduler.run_report_now(report_id)
print(f"Report generated: {result['report_path']}")
```

### Delete Report

```python
# Remove scheduled report
scheduler.delete_report(report_id)
```

## Continuous Monitoring

### Trend Monitoring

Set up continuous trend tracking:

```python
from perplSDK.research.trend_monitor import TrendMonitor

trend_monitor = TrendMonitor()

# Add trends to monitor
ev_trends = [
    "solid-state battery technology",
    "ultra-fast charging",
    "vehicle-to-grid technology",
    "autonomous EV systems",
    "battery recycling innovations"
]

for trend in ev_trends:
    trend_monitor.add_trend_to_monitor(
        topic=trend,
        category="ev_technology",
        monitoring_frequency="weekly"
    )

# Get monitoring status
status = trend_monitor.get_monitoring_status()
print(f"Monitoring {len(status['active_trends'])} trends")
```

### Market Intelligence Monitoring

Continuous market analysis:

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

# Daily market monitoring
scheduler.schedule_report(
    name="Daily Market Monitor",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.DAILY,
    config={
        "sector": MarketSector.ELECTRIC_VEHICLES.value,
        "analysis_type": "trends",
        "time_frame": "current"
    }
)
```

## Complete Automation Workflow

### Multi-Tier Reporting System

```python
from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency

scheduler = ReportScheduler()

# Tier 1: High-frequency monitoring
scheduler.schedule_report(
    name="Hourly News Digest",
    report_type=ReportType.RESEARCH,
    frequency=ReportFrequency.HOURLY,
    config={
        "queries": ["Latest EV news and announcements"]
    }
)

# Tier 2: Daily analysis
scheduler.schedule_report(
    name="Daily Trend Analysis",
    report_type=ReportType.TREND_ANALYSIS,
    frequency=ReportFrequency.DAILY,
    config={
        "industry": "electric_vehicles",
        "time_period": "current"
    },
    publish_to_github=True
)

# Tier 3: Weekly intelligence
scheduler.schedule_report(
    name="Weekly Market Intelligence",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.WEEKLY,
    config={
        "sector": "electric_vehicles",
        "analysis_type": "comprehensive"
    },
    publish_to_github=True
)

# Tier 4: Monthly deep dive
scheduler.schedule_report(
    name="Monthly Strategic Analysis",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.MONTHLY,
    config={
        "sector": "electric_vehicles",
        "analysis_type": "comprehensive",
        "geographic_focus": "global"
    },
    publish_to_github=True,
    github_config={
        "create_pr": True,
        "pr_title": "Monthly Strategic Analysis"
    }
)

# Start all scheduled reports
scheduler.start_scheduler()
```

## Workflow Orchestration

### Sequential Workflows

Execute multiple research phases:

```python
from perplSDK import ResearchAutomation
from perplSDK.research.market_intelligence import MarketIntelligence
from perplSDK.research.trend_monitor import TrendMonitor

# Phase 1: Market research
research = ResearchAutomation()
project = research.create_project("Comprehensive EV Analysis")
project.add_query("Current EV market landscape")
research.conduct_research(project.name)

# Phase 2: Trend detection
trend_monitor = TrendMonitor()
trends = trend_monitor.detect_emerging_trends(
    industry="electric_vehicles",
    time_period="quarterly"
)

# Phase 3: Market intelligence
market_intel = MarketIntelligence()
analysis = market_intel.conduct_market_analysis(
    sector="electric_vehicles",
    analysis_type="comprehensive"
)

# Phase 4: Report generation and publishing
# (automated through scheduler)
```

### Parallel Workflows

Execute multiple analyses simultaneously:

```python
import asyncio
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

async def analyze_sector(sector):
    market_intel = MarketIntelligence()
    return await market_intel.conduct_market_analysis_async(
        sector=sector,
        analysis_type="comprehensive"
    )

async def parallel_analysis():
    sectors = [
        MarketSector.ELECTRIC_VEHICLES,
        MarketSector.BATTERY_TECHNOLOGY,
        MarketSector.CHARGING_INFRASTRUCTURE
    ]
    
    tasks = [analyze_sector(sector) for sector in sectors]
    results = await asyncio.gather(*tasks)
    return results

# Execute parallel analysis
results = asyncio.run(parallel_analysis())
```

## Error Handling and Monitoring

### Error Notifications

```python
from perplSDK.core.exceptions import PerplSDKError

try:
    result = scheduler.run_report_now(report_id)
except PerplSDKError as e:
    # Send notification (email, Slack, etc.)
    print(f"Report generation failed: {e}")
    # Log error
    # Retry or escalate
```

### Health Checks

```python
# Check scheduler health
if scheduler._is_running:
    print("Scheduler is running")
    
# Check recent execution history
status = scheduler.get_report_status(report_id)
recent_failures = [
    execution for execution in status['recent_executions']
    if execution.get('status') == 'failed'
]

if recent_failures:
    print(f"Warning: {len(recent_failures)} recent failures")
```

## Best Practices

1. **Start Simple**: Begin with basic schedules and add complexity
2. **Monitor Performance**: Track execution times and success rates
3. **Handle Errors**: Implement robust error handling and notifications
4. **Use Appropriate Frequencies**: Match frequency to data volatility
5. **Resource Management**: Consider API rate limits and costs
6. **Version Control**: Store scheduler configurations in version control
7. **Test Schedules**: Test scheduled reports before production deployment
8. **Document Workflows**: Maintain documentation of automation logic

## Example Scripts

### Production Automation Setup

```python
#!/usr/bin/env python3
"""
Production automation setup for EV MAX INC.
Sets up all scheduled reports and monitoring.
"""

from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency
from perplSDK.research.trend_monitor import TrendMonitor

def setup_automation():
    scheduler = ReportScheduler()
    
    # Daily morning brief
    scheduler.schedule_report(
        name="Morning EV Brief",
        report_type=ReportType.RESEARCH,
        frequency=ReportFrequency.CUSTOM,
        custom_schedule="0 6 * * *",  # 6 AM daily
        config={
            "queries": [
                "EV news overnight",
                "Stock market pre-open EV sector"
            ]
        }
    )
    
    # Weekly comprehensive report
    scheduler.schedule_report(
        name="Weekly EV Intelligence",
        report_type=ReportType.MARKET_INTELLIGENCE,
        frequency=ReportFrequency.CUSTOM,
        custom_schedule="0 9 * * MON",  # Monday 9 AM
        config={
            "sector": "electric_vehicles",
            "analysis_type": "comprehensive"
        },
        publish_to_github=True
    )
    
    # Monthly strategic analysis
    scheduler.schedule_report(
        name="Monthly Strategic Analysis",
        report_type=ReportType.MARKET_INTELLIGENCE,
        frequency=ReportFrequency.CUSTOM,
        custom_schedule="0 0 1 * *",  # 1st of month
        config={
            "sector": "electric_vehicles",
            "analysis_type": "comprehensive",
            "geographic_focus": "global"
        },
        publish_to_github=True,
        github_config={"create_pr": True}
    )
    
    # Start scheduler
    scheduler.start_scheduler()
    print("Automation setup complete")
    
    # Setup trend monitoring
    trend_monitor = TrendMonitor()
    ev_trends = [
        "solid-state batteries",
        "ultra-fast charging",
        "vehicle-to-grid"
    ]
    
    for trend in ev_trends:
        trend_monitor.add_trend_to_monitor(
            topic=trend,
            monitoring_frequency="weekly"
        )
    
    print(f"Monitoring {len(ev_trends)} trends")

if __name__ == "__main__":
    setup_automation()
```

### Monitoring Dashboard

```python
#!/usr/bin/env python3
"""
Display status of all automated workflows.
"""

from perplSDK.reports.scheduler import ReportScheduler

def display_dashboard():
    scheduler = ReportScheduler()
    
    print("=== Automated Workflows Dashboard ===\n")
    
    # List all reports
    reports = scheduler.list_scheduled_reports()
    
    print(f"Total Reports: {len(reports)}")
    print(f"Scheduler Running: {scheduler._is_running}\n")
    
    # Display each report
    for report in reports:
        print(f"Report: {report['name']}")
        print(f"  Type: {report['report_type']}")
        print(f"  Frequency: {report['frequency']}")
        print(f"  Enabled: {report['enabled']}")
        
        status = scheduler.get_report_status(report['id'])
        if status:
            print(f"  Last Run: {status.get('last_run', 'Never')}")
            print(f"  Next Run: {status.get('next_run', 'Not scheduled')}")
        print()

if __name__ == "__main__":
    display_dashboard()
```

## Troubleshooting

### Scheduler Not Running

```python
# Check if scheduler is running
if not scheduler._is_running:
    scheduler.start_scheduler()
```

### Reports Not Executing

```python
# Check report status
status = scheduler.get_report_status(report_id)
if not status['enabled']:
    scheduler.enable_report(report_id)
```

### GitHub Publishing Failures

```python
# Verify GitHub configuration
from perplSDK.core.config import Config

config = Config.from_env()
if not config.github_token or not config.github_repo:
    print("GitHub configuration incomplete")
```

## See Also

- [Report Generation API](../api/reports.md)
- [GitHub Integration API](../api/github.md)
- [Configuration Guide](configuration.md)
- [EV Industry Research Guide](ev_research.md)
