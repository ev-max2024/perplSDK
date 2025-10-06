# Research Automation API Reference

The Research Automation module provides project-based research capabilities with parallel query execution, result management, and comprehensive research planning.

## Installation

```python
from perplSDK import ResearchAutomation
from perplSDK.research.automation import ResearchProject
```

## ResearchAutomation Class

### Initialization

```python
research = ResearchAutomation(config=None)
```

**Parameters:**
- `config` (Optional[Config]): Configuration object. If None, loads from environment.

## Project Management

### `create_project(name, description="")`

Create a new research project.

**Parameters:**
- `name` (str): Project name (unique identifier)
- `description` (str): Project description

**Returns:**
- `ResearchProject`: New project instance

**Example:**

```python
project = research.create_project(
    "EV Market Analysis",
    "Q4 2024 electric vehicle market research"
)
```

### `get_project(name)`

Retrieve an existing project.

**Parameters:**
- `name` (str): Project name

**Returns:**
- `Optional[ResearchProject]`: Project instance or None

### `list_projects()`

List all project names.

**Returns:**
- `List[str]`: List of project names

## Research Execution

### `conduct_research(project_name, queries=None, parallel=True, save_results=True)`

Execute research queries for a project.

**Parameters:**
- `project_name` (str): Name of the project
- `queries` (Optional[List[str]]): Custom queries (uses project queries if None)
- `parallel` (bool): Execute queries in parallel
- `save_results` (bool): Save results to project

**Returns:**
- `ResearchProject`: Updated project with results

**Example:**

```python
# Create and execute research
project = research.create_project("EV Research")
project.add_query("Latest EV battery technology")
project.add_query("EV charging infrastructure trends")

research.conduct_research(project.name, parallel=True)

# Access results
for result in project.results:
    print(result.content)
```

### `generate_research_plan(topic, depth="comprehensive")`

Generate a research plan for a topic.

**Parameters:**
- `topic` (str): Research topic
- `depth` (str): Research depth ("basic", "comprehensive", "deep")

**Returns:**
- `List[str]`: Generated research queries

**Example:**

```python
queries = research.generate_research_plan(
    "electric vehicle adoption",
    depth="comprehensive"
)
print(f"Generated {len(queries)} research queries")
```

## ResearchProject Class

### Attributes

```python
project = ResearchProject(name, description)
project.name              # Project name
project.description       # Description
project.queries          # List of queries
project.results          # List of SearchResults
project.created_at       # Creation timestamp
project.updated_at       # Last update timestamp
project.metadata         # Custom metadata dict
```

### Methods

#### `add_query(query, category="general", priority=1, **kwargs)`

Add a query to the project.

**Parameters:**
- `query` (str): Query string
- `category` (str): Query category
- `priority` (int): Query priority (1-5)
- `**kwargs`: Additional query parameters

**Example:**

```python
project.add_query(
    "EV market share by manufacturer",
    category="market_analysis",
    priority=1
)
```

#### `to_dict()`

Convert project to dictionary for serialization.

**Returns:**
- `Dict[str, Any]`: Project data as dictionary

## Research Templates

### `generate_template_queries(template_name)`

Generate queries from a template.

**Available Templates:**
- `ev_market_analysis`: Electric vehicle market research
- `technology_assessment`: Technology evaluation
- `competitive_analysis`: Competitor research
- `trend_analysis`: Market trend research

**Example:**

```python
from perplSDK.utils.templates import ResearchTemplate

template = ResearchTemplate()
queries = template.generate_template_queries("ev_market_analysis")
```

## Advanced Features

### Parallel Execution

```python
# Execute multiple projects in parallel
projects = ["Project A", "Project B", "Project C"]
for project_name in projects:
    research.conduct_research(project_name, parallel=True)
```

### Custom Query Parameters

```python
project.add_query(
    "EV battery innovations",
    category="technology",
    priority=1,
    model="llama-3.1-sonar-large-128k-online",
    return_related_questions=True
)
```

### Saving and Loading Projects

```python
import json

# Save project
project_data = project.to_dict()
with open("project.json", "w") as f:
    json.dump(project_data, f)

# Load project
with open("project.json", "r") as f:
    data = json.load(f)
# Reconstruct project from data
```

## Integration with Reports

```python
from perplSDK.reports.formatter import MarkdownFormatter

# Generate report from research
formatter = MarkdownFormatter()
report = formatter.format_research_report(
    project_name=project.name,
    results=project.results,
    metadata={"description": project.description}
)

# Save report
report_path = formatter.save_report(report, "ev_research_2024")
```

## Best Practices

1. **Organize by Project**: Group related queries into projects
2. **Use Categories**: Categorize queries for better organization
3. **Set Priorities**: Prioritize important queries
4. **Enable Parallel Execution**: Use parallel mode for faster results
5. **Save Results**: Enable save_results for persistence
6. **Use Templates**: Leverage templates for common research types

## Error Handling

```python
from perplSDK.core.exceptions import PerplSDKError

try:
    project = research.conduct_research("My Project")
except PerplSDKError as e:
    print(f"Research error: {e}")
```

## Examples

### Complete Research Workflow

```python
from perplSDK import ResearchAutomation
from perplSDK.reports.formatter import MarkdownFormatter

# Initialize
research = ResearchAutomation()
formatter = MarkdownFormatter()

# Create project
project = research.create_project(
    "EV Market Q4 2024",
    "Comprehensive EV market analysis"
)

# Add queries
project.add_query("Current EV market share by manufacturer")
project.add_query("EV battery technology innovations 2024")
project.add_query("Charging infrastructure expansion trends")
project.add_query("EV policy developments")

# Execute research
research.conduct_research(project.name, parallel=True)

# Generate report
report = formatter.format_research_report(
    project_name=project.name,
    results=project.results,
    metadata={"total_queries": len(project.queries)}
)

# Save report
report_path = formatter.save_report(report, "ev_market_q4_2024")
print(f"Report saved to: {report_path}")
```

## See Also

- [PerplexityClient API](client.md)
- [Market Intelligence](market_intelligence.md)
- [Report Generation](reports.md)
- [Automated Workflows Guide](../guides/automation.md)
