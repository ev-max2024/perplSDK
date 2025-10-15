# GitHub Integration API Reference

The GitHub Integration module enables automated publishing of reports and research outputs to GitHub repositories, including support for pull requests and branch management.

## Installation

```python
from perplSDK.github_integration.publisher import GitHubPublisher
```

## GitHubPublisher Class

### Initialization

```python
github = GitHubPublisher(config=None)
```

**Parameters:**
- `config` (Optional[Config]): Configuration object with GitHub credentials

**Required Configuration:**
- `github_token`: GitHub personal access token
- `github_repo`: Repository in format `owner/repo`

**Example:**

```python
from perplSDK.core.config import Config

config = Config(
    github_token="ghp_your_token",
    github_repo="ev-max2024/research-reports"
)
github = GitHubPublisher(config)
```

## Core Methods

### `publish_content(content, file_path, commit_message, branch=None, create_pr=False, pr_title=None, pr_body=None)`

Publish content to a GitHub repository.

**Parameters:**
- `content` (str): Content to publish
- `file_path` (str): Path in repository where to publish
- `commit_message` (str): Git commit message
- `branch` (Optional[str]): Target branch (defaults to config branch)
- `create_pr` (bool): Whether to create a pull request
- `pr_title` (Optional[str]): Pull request title
- `pr_body` (Optional[str]): Pull request body

**Returns:**
- `Dict[str, Any]`: Publishing results containing:
  - `success` (bool): Whether operation succeeded
  - `file_path` (str): Path to published file
  - `commit_sha` (str): Commit SHA
  - `pr_url` (Optional[str]): Pull request URL (if created)

**Example:**

```python
result = github.publish_content(
    content=report_content,
    file_path="reports/ev_analysis_2024.md",
    commit_message="Add EV market analysis report",
    branch="main"
)

print(f"Published to: {result['file_path']}")
print(f"Commit: {result['commit_sha']}")
```

### `publish_file(local_file_path, github_file_path, commit_message, branch=None, create_pr=False, pr_title=None, pr_body=None)`

Publish a local file to GitHub repository.

**Parameters:**
- `local_file_path` (str): Path to local file
- `github_file_path` (str): Path in repository
- `commit_message` (str): Commit message
- `branch` (Optional[str]): Target branch
- `create_pr` (bool): Whether to create a pull request
- `pr_title` (Optional[str]): Pull request title
- `pr_body` (Optional[str]): Pull request body

**Returns:**
- `Dict[str, Any]`: Publishing results

**Example:**

```python
result = github.publish_file(
    local_file_path="./reports/analysis.md",
    github_file_path="reports/latest_analysis.md",
    commit_message="Update market analysis"
)
```

### `create_pull_request(title, body, head_branch, base_branch=None)`

Create a pull request.

**Parameters:**
- `title` (str): Pull request title
- `body` (str): Pull request description
- `head_branch` (str): Source branch
- `base_branch` (Optional[str]): Target branch (defaults to config branch)

**Returns:**
- `Dict[str, Any]`: Pull request details containing:
  - `number` (int): PR number
  - `url` (str): PR URL
  - `state` (str): PR state

**Example:**

```python
pr = github.create_pull_request(
    title="Weekly EV Market Report",
    body="Automated weekly market intelligence report",
    head_branch="reports/weekly-update",
    base_branch="main"
)

print(f"Created PR #{pr['number']}: {pr['url']}")
```

### `update_file(file_path, content, commit_message, branch=None)`

Update an existing file in the repository.

**Parameters:**
- `file_path` (str): Path to file in repository
- `content` (str): New content
- `commit_message` (str): Commit message
- `branch` (Optional[str]): Target branch

**Returns:**
- `Dict[str, Any]`: Update results

**Example:**

```python
result = github.update_file(
    file_path="README.md",
    content=updated_readme,
    commit_message="Update README with latest results"
)
```

### `delete_file(file_path, commit_message, branch=None)`

Delete a file from the repository.

**Parameters:**
- `file_path` (str): Path to file in repository
- `commit_message` (str): Commit message
- `branch` (Optional[str]): Target branch

**Returns:**
- `Dict[str, Any]`: Deletion results

**Example:**

```python
result = github.delete_file(
    file_path="reports/old_report.md",
    commit_message="Remove outdated report"
)
```

## Branch Management

### `create_branch(branch_name, source_branch=None)`

Create a new branch.

**Parameters:**
- `branch_name` (str): Name for the new branch
- `source_branch` (Optional[str]): Source branch (defaults to default branch)

**Returns:**
- `Dict[str, Any]`: Branch creation results

**Example:**

```python
result = github.create_branch(
    branch_name="feature/new-reports",
    source_branch="main"
)
```

### `list_branches()`

List all branches in the repository.

**Returns:**
- `List[str]`: List of branch names

**Example:**

```python
branches = github.list_branches()
for branch in branches:
    print(branch)
```

## File Management

### `file_exists(file_path, branch=None)`

Check if a file exists in the repository.

**Parameters:**
- `file_path` (str): Path to file
- `branch` (Optional[str]): Branch to check (defaults to default branch)

**Returns:**
- `bool`: True if file exists

**Example:**

```python
if github.file_exists("reports/analysis.md"):
    print("File exists")
```

### `get_file_content(file_path, branch=None)`

Get content of a file from the repository.

**Parameters:**
- `file_path` (str): Path to file
- `branch` (Optional[str]): Branch to read from

**Returns:**
- `str`: File content

**Example:**

```python
content = github.get_file_content("reports/analysis.md")
print(content)
```

## Automated Workflows

### `setup_automated_reporting()`

Set up GitHub Actions workflow for automated reporting.

**Returns:**
- `Dict[str, Any]`: Setup results

**Example:**

```python
result = github.setup_automated_reporting()
print(f"Workflow created: {result['workflow_path']}")
```

## Advanced Features

### Pull Request Management

```python
# Create PR with detailed body
pr = github.create_pull_request(
    title="Q4 2024 Market Analysis",
    body="""
    ## Summary
    Quarterly market intelligence report
    
    ## Key Findings
    - Market growth of 15%
    - New competitors emerging
    - Technology advances
    
    ## Next Steps
    - Review insights
    - Update strategy
    """,
    head_branch="reports/q4-2024"
)
```

### Batch File Publishing

```python
# Publish multiple files
files = [
    ("reports/summary.md", "Summary report"),
    ("reports/detailed.md", "Detailed analysis"),
    ("reports/charts.md", "Visualization charts")
]

for file_path, message in files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    result = github.publish_content(
        content=content,
        file_path=f"published/{file_path}",
        commit_message=message
    )
    print(f"Published: {file_path}")
```

### Directory Management

```python
# Organize reports by date
from datetime import datetime

date_str = datetime.now().strftime("%Y-%m-%d")
file_path = f"reports/{date_str}/analysis.md"

result = github.publish_content(
    content=report,
    file_path=file_path,
    commit_message=f"Add report for {date_str}"
)
```

## Integration with Report Scheduler

```python
from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency

scheduler = ReportScheduler()

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

## Error Handling

```python
from perplSDK.github_integration.publisher import GitHubPublishingError

try:
    result = github.publish_content(
        content=report,
        file_path="reports/analysis.md",
        commit_message="Add report"
    )
except GitHubPublishingError as e:
    print(f"Publishing failed: {e}")
```

## Best Practices

1. **Use Personal Access Tokens**: Create tokens with minimum required permissions
2. **Descriptive Commit Messages**: Write clear, informative commit messages
3. **Branch Strategy**: Use feature branches for experimental reports
4. **Pull Requests**: Use PRs for team review of important reports
5. **Organize Files**: Use logical directory structure for reports
6. **Error Handling**: Implement proper error handling for production use
7. **Rate Limiting**: Be aware of GitHub API rate limits

## Security Considerations

1. **Never Commit Tokens**: Store tokens in environment variables or config files
2. **Use Minimal Permissions**: Grant only necessary repository permissions
3. **Rotate Tokens**: Regularly rotate access tokens
4. **Private Repositories**: Use private repos for sensitive data

## Examples

### Complete Publishing Workflow

```python
from perplSDK import ResearchAutomation
from perplSDK.reports.formatter import MarkdownFormatter
from perplSDK.github_integration.publisher import GitHubPublisher

# Conduct research
research = ResearchAutomation()
project = research.create_project("EV Analysis")
project.add_query("Latest EV market trends")
research.conduct_research(project.name)

# Format report
formatter = MarkdownFormatter()
report = formatter.format_research_report(
    project_name=project.name,
    results=project.results
)

# Publish to GitHub
github = GitHubPublisher()
result = github.publish_content(
    content=report,
    file_path="reports/ev_analysis_latest.md",
    commit_message="Add latest EV market analysis",
    create_pr=True,
    pr_title="Latest EV Market Analysis",
    pr_body="Automated research report on EV market trends"
)

print(f"Report published: {result['file_path']}")
if result.get('pr_url'):
    print(f"Pull request: {result['pr_url']}")
```

### Automated Daily Updates

```python
from datetime import datetime

# Generate report
report = generate_daily_report()

# Publish with date-based naming
date_str = datetime.now().strftime("%Y-%m-%d")
result = github.publish_content(
    content=report,
    file_path=f"reports/daily/{date_str}.md",
    commit_message=f"Daily report for {date_str}",
    branch="main"
)

# Update latest link
github.publish_content(
    content=f"See [latest report](daily/{date_str}.md)",
    file_path="reports/LATEST.md",
    commit_message="Update latest report link"
)
```

### Multi-Repository Publishing

```python
from perplSDK.core.config import Config

# Publish to multiple repos
repos = [
    "ev-max2024/research-reports",
    "ev-max2024/public-insights",
    "ev-max2024/internal-analysis"
]

for repo in repos:
    config = Config(
        github_token=os.getenv("GITHUB_TOKEN"),
        github_repo=repo
    )
    publisher = GitHubPublisher(config)
    
    result = publisher.publish_content(
        content=report,
        file_path="reports/analysis.md",
        commit_message="Add analysis report"
    )
    print(f"Published to {repo}")
```

## See Also

- [Report Generation](reports.md)
- [Research Automation](research.md)
- [Configuration Guide](../guides/configuration.md)
