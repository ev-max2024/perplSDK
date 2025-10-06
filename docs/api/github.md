# GitHub Integration API

The GitHub Integration module provides tools for publishing research reports, automating workflows, and managing repository content programmatically.

## Overview

GitHub integration features:
- File publishing and updates
- Pull request creation
- Automated workflows
- Branch management
- Issue tracking integration
- Report archiving
- CI/CD integration

## Installation

```python
from perplSDK.github_integration.publisher import GitHubPublisher
from perplSDK.core.config import Config
```

## Configuration

Set up GitHub credentials:

```bash
export GITHUB_TOKEN="your-github-personal-access-token"
export GITHUB_REPO="owner/repository-name"
export GITHUB_BRANCH="main"
```

Or in `.env` file:

```
GITHUB_TOKEN=your-github-personal-access-token
GITHUB_REPO=owner/repository-name
GITHUB_BRANCH=main
```

## GitHubPublisher

Main class for GitHub publishing operations.

### Initialization

```python
# Using environment configuration
github = GitHubPublisher()

# With custom configuration
config = Config(
    github_token="your-token",
    github_repo="owner/repo",
    github_branch="main"
)
github = GitHubPublisher(config)
```

### File Publishing

#### publish_content()

Publish content directly to a GitHub repository.

```python
def publish_content(
    content: str,
    file_path: str,
    commit_message: str,
    branch: Optional[str] = None,
    create_pr: bool = False,
    pr_title: Optional[str] = None,
    pr_body: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `content` (str): Content to publish
- `file_path` (str): Path in repository
- `commit_message` (str): Git commit message
- `branch` (str, optional): Target branch
- `create_pr` (bool): Create a pull request (default: False)
- `pr_title` (str, optional): Pull request title
- `pr_body` (str, optional): Pull request description

**Returns:**
- `Dict[str, Any]`: Publishing results with commit SHA, URL, and PR info if created

**Example:**
```python
result = github.publish_content(
    content="# Market Analysis\n\nKey findings...",
    file_path="reports/market_analysis.md",
    commit_message="Add market analysis report",
    branch="main"
)

print(f"Published: {result['html_url']}")
print(f"Commit SHA: {result['commit_sha']}")
```

#### publish_file()

Publish a local file to GitHub.

```python
def publish_file(
    local_file_path: str,
    github_file_path: str,
    commit_message: str,
    branch: Optional[str] = None,
    create_pr: bool = False,
    pr_title: Optional[str] = None,
    pr_body: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `local_file_path` (str): Path to local file
- `github_file_path` (str): Target path in repository
- `commit_message` (str): Git commit message
- `branch` (str, optional): Target branch
- `create_pr` (bool): Create a pull request
- `pr_title` (str, optional): Pull request title
- `pr_body` (str, optional): Pull request description

**Returns:**
- `Dict[str, Any]`: Publishing results

**Example:**
```python
result = github.publish_file(
    local_file_path="./reports/ev_analysis.md",
    github_file_path="reports/2024/ev_analysis.md",
    commit_message="Update EV analysis report",
    branch="main"
)
```

### Pull Request Management

#### create_pull_request()

Create a pull request.

```python
def create_pull_request(
    title: str,
    body: str,
    head: str,
    base: str = "main"
) -> Dict[str, Any]
```

**Parameters:**
- `title` (str): PR title
- `body` (str): PR description
- `head` (str): Source branch
- `base` (str): Target branch (default: "main")

**Returns:**
- `Dict[str, Any]`: Pull request information

**Example:**
```python
pr = github.create_pull_request(
    title="Weekly Market Intelligence Report",
    body="This PR adds the weekly market intelligence report for W48 2024.",
    head="reports/week-48",
    base="main"
)

print(f"PR created: {pr['html_url']}")
print(f"PR number: {pr['number']}")
```

#### update_pull_request()

Update an existing pull request.

```python
def update_pull_request(
    pr_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None
) -> Dict[str, Any]
```

**Example:**
```python
updated = github.update_pull_request(
    pr_number=42,
    body="Updated with additional analysis and recommendations."
)
```

### Branch Management

#### create_branch()

Create a new branch.

```python
def create_branch(
    branch_name: str,
    from_branch: str = "main"
) -> Dict[str, Any]
```

**Example:**
```python
branch = github.create_branch(
    branch_name="reports/q4-2024",
    from_branch="main"
)
```

#### delete_branch()

Delete a branch.

```python
def delete_branch(branch_name: str) -> bool
```

**Example:**
```python
success = github.delete_branch("reports/old-branch")
```

### Automated Workflows

#### setup_automated_reporting()

Set up automated reporting workflow with GitHub Actions.

```python
def setup_automated_reporting(
    schedule: str = "0 9 * * 1",  # Cron format
    report_types: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `schedule` (str): Cron schedule expression
- `report_types` (List[str], optional): Types of reports to automate

**Returns:**
- `Dict[str, Any]`: Workflow configuration

**Example:**
```python
workflow = github.setup_automated_reporting(
    schedule="0 9 * * 1",  # Every Monday at 9 AM
    report_types=["market_intelligence", "trend_analysis"]
)
```

#### setup_issue_tracking()

Set up issue tracking for research tasks.

```python
def setup_issue_tracking(
    labels: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Example:**
```python
tracking = github.setup_issue_tracking(
    labels=["research", "market-intelligence", "automated"]
)
```

### Batch Operations

#### publish_multiple_files()

Publish multiple files in a single commit.

```python
def publish_multiple_files(
    files: List[Dict[str, str]],
    commit_message: str,
    branch: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `files` (List[Dict]): List of file dictionaries with 'local_path' and 'github_path'
- `commit_message` (str): Commit message
- `branch` (str, optional): Target branch

**Example:**
```python
files = [
    {"local_path": "./reports/summary.md", "github_path": "reports/summary.md"},
    {"local_path": "./reports/details.md", "github_path": "reports/details.md"},
    {"local_path": "./data/metrics.json", "github_path": "data/metrics.json"}
]

result = github.publish_multiple_files(
    files=files,
    commit_message="Add weekly reports and metrics",
    branch="main"
)
```

## Complete Workflow Examples

### Basic Publishing

```python
from perplSDK.github_integration.publisher import GitHubPublisher
from perplSDK.reports.formatter import MarkdownFormatter
from perplSDK.research.automation import ResearchAutomation

# Conduct research
research = ResearchAutomation()
project = research.create_project("Weekly EV Update")
project.add_query("Latest EV market developments")
project = research.conduct_research(project.name)

# Format report
formatter = MarkdownFormatter()
report = formatter.format_research_report(
    project_name=project.name,
    results=project.results
)
report_path = formatter.save_report(report, "weekly_ev_update")

# Publish to GitHub
github = GitHubPublisher()
result = github.publish_file(
    local_file_path=report_path,
    github_file_path="reports/weekly/latest.md",
    commit_message="Add weekly EV update"
)

print(f"Published successfully: {result['html_url']}")
```

### Publishing with Pull Request

```python
# Publish to feature branch with PR
result = github.publish_file(
    local_file_path="./reports/analysis.md",
    github_file_path="reports/market_analysis.md",
    commit_message="Add market analysis",
    branch="analysis/market",
    create_pr=True,
    pr_title="Market Analysis Report - Q4 2024",
    pr_body="""
## Summary
Comprehensive market analysis for Q4 2024

## Key Findings
- Market growth of 35%
- New players entering the market
- Technology trends shifting

## Recommendations
- Expand product line
- Invest in R&D
- Strategic partnerships
    """
)

print(f"PR created: {result['pr_url']}")
```

### Automated Weekly Reports

```python
from perplSDK.reports.scheduler import ReportScheduler
from perplSDK.github_integration.publisher import GitHubPublisher
import schedule
import time

def generate_and_publish_report():
    # Generate report
    research = ResearchAutomation()
    project = research.create_project("Weekly Report")
    project.add_query("Weekly EV trends")
    project = research.conduct_research(project.name)
    
    # Format
    formatter = MarkdownFormatter()
    report = formatter.format_research_report(
        project_name=project.name,
        results=project.results
    )
    report_path = formatter.save_report(report, "weekly_report")
    
    # Publish
    github = GitHubPublisher()
    github.publish_file(
        local_file_path=report_path,
        github_file_path=f"reports/weekly/{datetime.now().strftime('%Y-%m-%d')}.md",
        commit_message=f"Weekly report for {datetime.now().strftime('%Y-%m-%d')}"
    )
    print("Weekly report published")

# Schedule weekly execution
schedule.every().monday.at("09:00").do(generate_and_publish_report)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

### Multi-File Publishing

```python
from datetime import datetime

# Generate multiple reports
date_str = datetime.now().strftime("%Y-%m-%d")

# Market intelligence report
market_analysis = market_intel.conduct_market_analysis(...)
market_report = formatter.format_market_intelligence_report(market_analysis)
market_path = formatter.save_report(market_report, "market_report")

# Trend analysis report
trends = trend_monitor.detect_emerging_trends(...)
trend_report = formatter.format_trend_report(trends)
trend_path = formatter.save_report(trend_report, "trend_report")

# Publish all files together
files = [
    {
        "local_path": market_path,
        "github_path": f"reports/{date_str}/market_intelligence.md"
    },
    {
        "local_path": trend_path,
        "github_path": f"reports/{date_str}/trend_analysis.md"
    }
]

github.publish_multiple_files(
    files=files,
    commit_message=f"Add reports for {date_str}"
)
```

### Report Archive Management

```python
from datetime import datetime, timedelta

def archive_old_reports():
    """Archive reports older than 90 days."""
    github = GitHubPublisher()
    
    # Create archive branch
    archive_branch = f"archive/{datetime.now().year}"
    github.create_branch(
        branch_name=archive_branch,
        from_branch="main"
    )
    
    # Move old reports to archive branch
    cutoff_date = datetime.now() - timedelta(days=90)
    # ... logic to identify and move old reports ...
    
    # Create PR for review
    github.create_pull_request(
        title=f"Archive reports older than {cutoff_date.strftime('%Y-%m-%d')}",
        body="Moving old reports to archive for better organization.",
        head=archive_branch,
        base="main"
    )

# Run monthly
schedule.every().month.do(archive_old_reports)
```

## Advanced Features

### Custom Workflow Triggers

```python
# Set up custom GitHub Actions workflow
workflow_content = """
name: Research Report Generation
on:
  schedule:
    - cron: '0 9 * * 1'
  workflow_dispatch:

jobs:
  generate-report:
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
      - name: Generate report
        env:
          PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/generate_weekly_report.py
"""

github.publish_content(
    content=workflow_content,
    file_path=".github/workflows/research_report.yml",
    commit_message="Add automated research report workflow"
)
```

### Issue-Based Research Tracking

```python
from github import Github

# Create issues for research tasks
gh = Github(config.github_token)
repo = gh.get_repo(config.github_repo)

# Create research task issue
issue = repo.create_issue(
    title="Research Task: EV Battery Trends Q1 2025",
    body="""
## Research Scope
- Battery technology developments
- Cost trends
- Manufacturing capacity

## Deliverables
- [ ] Initial research
- [ ] Market analysis
- [ ] Final report

## Timeline
Due: 2025-01-31
    """,
    labels=["research", "high-priority"]
)

print(f"Research task created: {issue.html_url}")
```

### Version Control for Reports

```python
def publish_versioned_report(report_content, report_name):
    """Publish report with version tracking."""
    github = GitHubPublisher()
    
    # Get current version
    version = get_next_version(report_name)
    
    # Publish versioned report
    result = github.publish_content(
        content=report_content,
        file_path=f"reports/{report_name}/v{version}.md",
        commit_message=f"Add {report_name} v{version}"
    )
    
    # Update latest symlink or copy
    github.publish_content(
        content=report_content,
        file_path=f"reports/{report_name}/latest.md",
        commit_message=f"Update {report_name} latest to v{version}"
    )
    
    return result
```

## Integration with CI/CD

### GitHub Actions Integration

```python
# Generate report in GitHub Actions
def main():
    # This script runs in GitHub Actions
    github = GitHubPublisher()
    research = ResearchAutomation()
    
    # Generate report
    project = research.create_project("Automated Report")
    project.add_query("Latest market trends")
    project = research.conduct_research(project.name)
    
    # Format and publish
    formatter = MarkdownFormatter()
    report = formatter.format_research_report(
        project_name=project.name,
        results=project.results
    )
    
    # Publish directly (already in repo)
    report_path = formatter.save_report(report, "automated_report")
    
    # Commit and push handled by GitHub Actions
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()
```

## Error Handling

```python
from perplSDK.github_integration.publisher import GitHubPublishingError

try:
    result = github.publish_file(
        local_file_path="report.md",
        github_file_path="reports/report.md",
        commit_message="Add report"
    )
except GitHubPublishingError as e:
    print(f"Publishing failed: {e}")
    # Retry logic or notification
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### 1. Use Meaningful Commit Messages

```python
# Good
commit_message = "Add Q4 2024 market intelligence report with trend analysis"

# Not recommended
commit_message = "Update report"
```

### 2. Organize Reports in Directories

```python
# Organized structure
github_file_path = f"reports/{year}/{quarter}/market_intelligence.md"

# Less organized
github_file_path = "market_intelligence.md"
```

### 3. Use Pull Requests for Review

```python
# Important reports should go through PR review
github.publish_file(
    local_file_path=report_path,
    github_file_path="reports/strategic/annual_review.md",
    commit_message="Add annual strategic review",
    create_pr=True,
    pr_title="Annual Strategic Review 2024",
    pr_body="Please review before merging"
)
```

### 4. Implement Versioning

```python
# Keep version history
version = "2.1"
github_file_path = f"reports/market_analysis/v{version}.md"
```

### 5. Add Metadata to Commits

```python
metadata = {
    "report_type": "market_intelligence",
    "generated_by": "perplSDK",
    "version": "2.1"
}

commit_message = f"""Add market intelligence report

Report Type: {metadata['report_type']}
Generated By: {metadata['generated_by']}
Version: {metadata['version']}
"""
```

## See Also

- [Report Generation](reports.md)
- [Research Automation](research.md)
- [Automated Workflows Guide](../guides/automation.md)
- [Configuration Guide](../guides/configuration.md)
