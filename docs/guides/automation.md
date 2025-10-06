# Automated Workflows Guide

This guide covers setting up automated research workflows, scheduled reports, continuous monitoring, and integration with CI/CD systems.

## Overview

perplSDK provides powerful automation capabilities:
- Scheduled research and reporting
- Continuous trend monitoring
- Automated GitHub publishing
- CI/CD integration
- Event-driven workflows
- Custom automation scripts

## Getting Started

### Basic Scheduled Report

```python
from perplSDK.reports.scheduler import ReportScheduler
from perplSDK.core.config import Config

# Initialize scheduler
config = Config.from_env()
scheduler = ReportScheduler(config)

# Schedule daily report
report_id = scheduler.schedule_report(
    name="Daily Market Update",
    report_type="trend_analysis",
    frequency="daily",
    config={
        "domains": ["electric vehicles"],
        "time_window": "day"
    }
)

# Start scheduler
scheduler.start_scheduler()
```

## Scheduling Options

### Frequency Types

```python
# Daily execution
scheduler.schedule_report(
    name="Daily Trends",
    report_type="trend_analysis",
    frequency="daily",
    config={...}
)

# Weekly execution
scheduler.schedule_report(
    name="Weekly Intelligence",
    report_type="market_intelligence",
    frequency="weekly",
    config={...}
)

# Monthly execution
scheduler.schedule_report(
    name="Monthly Analysis",
    report_type="market_intelligence",
    frequency="monthly",
    config={...}
)
```

### Custom Schedules with Python schedule

```python
import schedule
import time
from datetime import datetime

def custom_research_task():
    """Custom research task with specific logic."""
    # Your research logic here
    pass

# Run every Monday at 9 AM
schedule.every().monday.at("09:00").do(custom_research_task)

# Run every 6 hours
schedule.every(6).hours.do(custom_research_task)

# Run at specific times
schedule.every().day.at("09:00").do(custom_research_task)
schedule.every().day.at("15:00").do(custom_research_task)
schedule.every().day.at("21:00").do(custom_research_task)

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Automated Research Workflows

### Daily Trend Monitoring

```python
from perplSDK.research.trend_monitor import TrendMonitor
from perplSDK.reports.formatter import MarkdownFormatter
from perplSDK.github_integration.publisher import GitHubPublisher

def daily_trend_monitoring():
    """Monitor daily trends and publish report."""
    # Initialize
    trend_monitor = TrendMonitor()
    formatter = MarkdownFormatter()
    github = GitHubPublisher()
    
    # Detect trends
    trends = trend_monitor.detect_emerging_trends(
        search_domains=["electric vehicles", "battery technology"],
        time_window="day",
        min_momentum=0.6
    )
    
    # Format report
    report = formatter.format_trend_report(
        trends=trends,
        title=f"Daily Trend Report - {datetime.now().strftime('%Y-%m-%d')}"
    )
    
    # Save locally
    report_path = formatter.save_report(
        report,
        f"daily_trends_{datetime.now().strftime('%Y%m%d')}"
    )
    
    # Publish to GitHub
    github.publish_file(
        local_file_path=report_path,
        github_file_path=f"reports/daily/{datetime.now().strftime('%Y-%m-%d')}.md",
        commit_message=f"Daily trend report for {datetime.now().strftime('%Y-%m-%d')}"
    )
    
    print(f"✓ Daily trend report published")

# Schedule for 8 AM every day
schedule.every().day.at("08:00").do(daily_trend_monitoring)
```

### Weekly Market Intelligence

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

def weekly_market_intelligence():
    """Generate weekly market intelligence report."""
    market_intel = MarketIntelligence()
    formatter = MarkdownFormatter()
    github = GitHubPublisher()
    
    # Conduct analysis
    analysis = market_intel.conduct_market_analysis(
        sector=MarketSector.ELECTRIC_VEHICLES,
        analysis_type="comprehensive",
        geographic_focus="global"
    )
    
    # Format report
    report = formatter.format_market_intelligence_report(
        analysis=analysis,
        title=f"Weekly Market Intelligence - Week {datetime.now().strftime('%Y-W%U')}"
    )
    
    # Publish
    report_path = formatter.save_report(
        report,
        f"weekly_intel_{datetime.now().strftime('%Y_W%U')}"
    )
    
    github.publish_file(
        local_file_path=report_path,
        github_file_path=f"reports/weekly/{datetime.now().strftime('%Y-W%U')}.md",
        commit_message=f"Weekly intelligence report",
        create_pr=True,
        pr_title=f"Weekly Market Intelligence - Week {datetime.now().strftime('%Y-W%U')}",
        pr_body="Please review this week's market intelligence report."
    )
    
    print(f"✓ Weekly market intelligence published with PR")

# Schedule for Monday 9 AM
schedule.every().monday.at("09:00").do(weekly_market_intelligence)
```

### Monthly Comprehensive Reports

```python
def monthly_comprehensive_report():
    """Generate monthly comprehensive analysis."""
    research = ResearchAutomation()
    market_intel = MarketIntelligence()
    trend_monitor = TrendMonitor()
    formatter = MarkdownFormatter()
    github = GitHubPublisher()
    
    month = datetime.now().strftime('%Y-%m')
    
    # 1. Market analysis
    market_analysis = market_intel.conduct_market_analysis(
        sector=MarketSector.ELECTRIC_VEHICLES,
        analysis_type="comprehensive"
    )
    
    # 2. Monthly trends
    monthly_trends = trend_monitor.detect_emerging_trends(
        search_domains=["electric vehicles", "battery technology", "charging"],
        time_window="month"
    )
    
    # 3. Performance intelligence
    performance = market_intel.conduct_performance_intelligence(
        context="ev"
    )
    
    # Combine into comprehensive report
    comprehensive_report = f"""# Monthly Comprehensive Report - {month}

## Executive Summary
{generate_executive_summary(market_analysis, monthly_trends, performance)}

## Market Analysis
{formatter.format_market_intelligence_report(market_analysis)}

## Trend Analysis
{formatter.format_trend_report(monthly_trends)}

## Performance Intelligence
{format_performance_section(performance)}

## Strategic Recommendations
{generate_recommendations(market_analysis, monthly_trends, performance)}
"""
    
    # Save and publish
    report_path = formatter.save_report(comprehensive_report, f"monthly_report_{month}")
    github.publish_file(
        local_file_path=report_path,
        github_file_path=f"reports/monthly/{month}.md",
        commit_message=f"Monthly comprehensive report for {month}"
    )

# Run on first day of each month at 10 AM
schedule.every().month.at("01 10:00").do(monthly_comprehensive_report)
```

## Continuous Monitoring

### Real-Time Trend Alerts

```python
def monitor_and_alert():
    """Monitor trends and send alerts for significant changes."""
    trend_monitor = TrendMonitor()
    
    # Monitor key trends
    key_trends = [
        "solid-state battery commercialization",
        "400kW fast charging deployment",
        "vehicle-to-grid technology"
    ]
    
    for trend in key_trends:
        momentum = trend_monitor.analyze_trend_momentum(trend)
        
        # Alert if momentum exceeds threshold
        if momentum['current_momentum'] > 0.8:
            send_alert(
                f"High momentum detected: {trend}",
                f"Momentum score: {momentum['current_momentum']:.2f}\n"
                f"Growth indicators: {momentum['growth_indicators']}"
            )

# Check every hour
schedule.every(1).hours.do(monitor_and_alert)
```

### Competitor Monitoring

```python
def monitor_competitors():
    """Monitor competitor activities and announcements."""
    market_intel = MarketIntelligence()
    
    competitors = ["Tesla", "BYD", "Volkswagen", "Ford", "GM"]
    
    for competitor in competitors:
        # Search for recent news
        research = ResearchAutomation()
        project = research.create_project(f"{competitor} Monitor")
        project.add_query(f"{competitor} electric vehicle announcements last 24 hours")
        project.add_query(f"{competitor} EV technology updates")
        
        project = research.conduct_research(project.name)
        
        # Analyze results for significant updates
        if has_significant_updates(project.results):
            send_competitor_alert(competitor, project.results)

# Check daily at 8 AM
schedule.every().day.at("08:00").do(monitor_competitors)
```

## GitHub Integration Workflows

### Automated Report Publishing

```python
def automated_github_workflow():
    """Complete automated workflow with GitHub integration."""
    # Research
    research = ResearchAutomation()
    project = research.create_project("Automated Daily Analysis")
    project.add_query("Electric vehicle market updates")
    project.add_query("Battery technology news")
    project = research.conduct_research(project.name)
    
    # Format
    formatter = MarkdownFormatter()
    report = formatter.format_research_report(
        project_name=project.name,
        results=project.results,
        metadata={
            "automated": True,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    # Create branch for report
    github = GitHubPublisher()
    branch_name = f"reports/daily-{datetime.now().strftime('%Y%m%d')}"
    
    github.create_branch(branch_name)
    
    # Publish to branch
    report_path = formatter.save_report(report, "daily_analysis")
    github.publish_file(
        local_file_path=report_path,
        github_file_path="reports/daily/latest.md",
        commit_message="Add daily analysis report",
        branch=branch_name,
        create_pr=True,
        pr_title=f"Daily Analysis - {datetime.now().strftime('%Y-%m-%d')}",
        pr_body="Automated daily analysis report. Please review and merge."
    )

# Schedule daily
schedule.every().day.at("18:00").do(automated_github_workflow)
```

### Pull Request Workflow

```python
def pr_workflow():
    """Create reports with pull request workflow."""
    # Generate multiple reports
    reports = generate_weekly_reports()
    
    github = GitHubPublisher()
    branch = f"reports/week-{datetime.now().strftime('%Y-W%U')}"
    
    # Create feature branch
    github.create_branch(branch)
    
    # Publish all reports to branch
    files = []
    for report_name, report_content in reports.items():
        formatter = MarkdownFormatter()
        path = formatter.save_report(report_content, report_name)
        files.append({
            "local_path": path,
            "github_path": f"reports/weekly/{report_name}.md"
        })
    
    # Batch publish
    github.publish_multiple_files(
        files=files,
        commit_message="Add weekly reports",
        branch=branch
    )
    
    # Create PR
    github.create_pull_request(
        title=f"Weekly Reports - Week {datetime.now().strftime('%Y-W%U')}",
        body="Weekly reports for review and approval",
        head=branch,
        base="main"
    )
```

## CI/CD Integration

### GitHub Actions Workflow

Create `.github/workflows/research_automation.yml`:

```yaml
name: Automated Research

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  research:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install perplSDK
      
      - name: Run research automation
        env:
          PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPO: ${{ github.repository }}
        run: |
          python scripts/automated_research.py
      
      - name: Commit reports
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add reports/
          git commit -m "Add automated research reports" || echo "No changes"
          git push
```

### Docker-Based Automation

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install perplSDK
RUN pip install perplSDK

# Copy automation scripts
COPY automation/ ./automation/

# Run scheduler
CMD ["python", "automation/main_scheduler.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  research-automation:
    build: .
    environment:
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITHUB_REPO=${GITHUB_REPO}
    volumes:
      - ./reports:/app/reports
      - ./logs:/app/logs
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## Advanced Automation Patterns

### Event-Driven Automation

```python
class ResearchEventHandler:
    """Handle research events and trigger workflows."""
    
    def __init__(self):
        self.handlers = {}
    
    def on_trend_detected(self, trend):
        """Handle new trend detection."""
        if trend['momentum'] > 0.8:
            # Trigger deep dive research
            research = ResearchAutomation()
            project = research.create_project(f"Deep Dive: {trend['name']}")
            
            # Generate comprehensive queries
            template = ResearchTemplate()
            queries = template.generate_queries(trend['name'], "deep")
            
            for query in queries:
                project.add_query(query)
            
            research.conduct_research(project.name)
    
    def on_competitor_update(self, competitor, update):
        """Handle competitor updates."""
        # Trigger competitive analysis
        market_intel = MarketIntelligence()
        analysis = market_intel.analyze_competitors(
            sector=MarketSector.ELECTRIC_VEHICLES,
            competitors=[competitor],
            focus_areas=["technology", "market_share"]
        )
        
        # Alert stakeholders
        send_alert(f"Competitor Update: {competitor}", analysis)
    
    def on_market_shift(self, shift_data):
        """Handle significant market shifts."""
        # Trigger comprehensive analysis
        market_intel = MarketIntelligence()
        analysis = market_intel.conduct_market_analysis(
            sector=MarketSector.ELECTRIC_VEHICLES,
            analysis_type="comprehensive"
        )
        
        # Generate urgent report
        generate_urgent_report(analysis)

# Use event handler
handler = ResearchEventHandler()

# Monitor and trigger events
def monitor_events():
    trends = trend_monitor.detect_emerging_trends(...)
    for trend in trends:
        if trend['momentum'] > 0.8:
            handler.on_trend_detected(trend)

schedule.every(6).hours.do(monitor_events)
```

### Adaptive Scheduling

```python
class AdaptiveScheduler:
    """Scheduler that adapts based on conditions."""
    
    def __init__(self):
        self.research_frequency = "daily"
        self.last_significant_change = None
    
    def check_and_adjust(self):
        """Adjust scheduling based on market activity."""
        # Check market volatility
        volatility = self.measure_market_volatility()
        
        if volatility > 0.7:
            # High volatility - increase frequency
            self.research_frequency = "every_6_hours"
        elif volatility < 0.3:
            # Low volatility - decrease frequency
            self.research_frequency = "weekly"
        else:
            # Normal volatility - standard frequency
            self.research_frequency = "daily"
    
    def measure_market_volatility(self):
        """Measure recent market activity."""
        # Implementation to measure volatility
        # based on trend momentum, news volume, etc.
        pass

scheduler = AdaptiveScheduler()
```

### Multi-Stage Pipeline

```python
def research_pipeline():
    """Multi-stage automated research pipeline."""
    
    # Stage 1: Discovery
    print("Stage 1: Discovery")
    trends = trend_monitor.detect_emerging_trends(
        search_domains=["electric vehicles"],
        time_window="week"
    )
    
    # Stage 2: Filtering
    print("Stage 2: Filtering")
    significant_trends = [t for t in trends if t['momentum'] > 0.7]
    
    # Stage 3: Deep Analysis
    print("Stage 3: Deep Analysis")
    analyses = []
    for trend in significant_trends:
        research = ResearchAutomation()
        project = research.create_project(f"Analysis: {trend['name']}")
        
        # Add targeted queries
        project.add_query(f"Market impact of {trend['name']}")
        project.add_query(f"Technology behind {trend['name']}")
        project.add_query(f"Competitive landscape for {trend['name']}")
        
        project = research.conduct_research(project.name)
        analyses.append(project)
    
    # Stage 4: Synthesis
    print("Stage 4: Synthesis")
    combined_report = synthesize_analyses(analyses)
    
    # Stage 5: Publishing
    print("Stage 5: Publishing")
    publish_report(combined_report)
    
    # Stage 6: Notification
    print("Stage 6: Notification")
    notify_stakeholders(combined_report)

# Run pipeline weekly
schedule.every().monday.at("06:00").do(research_pipeline)
```

## Error Handling and Monitoring

### Robust Error Handling

```python
import logging
from perplSDK.core.exceptions import APIError, RateLimitError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='automation.log'
)

def robust_research_task():
    """Research task with comprehensive error handling."""
    try:
        # Attempt research
        research = ResearchAutomation()
        project = research.create_project("Daily Analysis")
        project.add_query("EV market updates")
        project = research.conduct_research(project.name)
        
        logging.info("Research completed successfully")
        
    except RateLimitError:
        logging.warning("Rate limit hit, retrying in 1 hour")
        schedule.every(1).hours.do(robust_research_task).tag('retry')
        
    except APIError as e:
        logging.error(f"API error: {e}")
        send_alert("Research automation failed", str(e))
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        send_alert("Critical automation error", str(e))
```

### Health Checks

```python
def health_check():
    """Check automation system health."""
    checks = {
        "api_connection": check_api_connection(),
        "github_connection": check_github_connection(),
        "disk_space": check_disk_space(),
        "scheduled_jobs": check_scheduled_jobs()
    }
    
    if not all(checks.values()):
        send_alert("Automation health check failed", checks)

# Run health check every hour
schedule.every(1).hours.do(health_check)
```

## Best Practices

### 1. Use Configuration Management

```python
# Keep automation config in YAML
automation_config = {
    "schedules": {
        "daily_trends": {"time": "08:00", "enabled": True},
        "weekly_intel": {"time": "09:00", "day": "monday", "enabled": True},
        "monthly_report": {"day": 1, "time": "10:00", "enabled": True}
    },
    "monitoring": {
        "key_trends": ["solid-state batteries", "fast charging"],
        "competitors": ["Tesla", "BYD", "Volkswagen"]
    },
    "alerts": {
        "email": "team@evmax.com",
        "slack_webhook": "https://..."
    }
}
```

### 2. Implement Logging

```python
import logging

logger = logging.getLogger('perplSDK.automation')

def automated_task():
    logger.info("Starting automated task")
    try:
        # Task logic
        logger.info("Task completed successfully")
    except Exception as e:
        logger.error(f"Task failed: {e}", exc_info=True)
```

### 3. Monitor and Alert

```python
def send_alert(title, message):
    """Send alert via multiple channels."""
    # Email
    send_email(title, message)
    
    # Slack
    send_slack_notification(title, message)
    
    # Log
    logging.warning(f"Alert: {title} - {message}")
```

### 4. Test Automation

```python
def test_automation():
    """Test automation workflows before production."""
    # Dry run mode
    scheduler = ReportScheduler(dry_run=True)
    
    # Test each workflow
    test_daily_trends()
    test_weekly_intel()
    test_monthly_report()
    
    print("All automation tests passed")
```

## See Also

- [Report Generation API](../api/reports.md)
- [GitHub Integration API](../api/github.md)
- [Configuration Guide](configuration.md)
- [EV Research Guide](ev_research.md)
