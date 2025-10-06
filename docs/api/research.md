# Research Automation API

The Research Automation module provides project-based research management with support for parallel query execution, result aggregation, and comprehensive research workflows.

## Overview

Research automation enables:
- Project-based research organization
- Multiple query management
- Parallel query execution
- Result aggregation and analysis
- Research plan generation from templates
- Project persistence and retrieval

## Installation

```python
from perplSDK.research.automation import ResearchAutomation, ResearchProject
from perplSDK.core.config import Config
```

## ResearchProject

A `ResearchProject` represents a collection of related research queries and their results.

### Initialization

```python
# Create through ResearchAutomation
research = ResearchAutomation()
project = research.create_project("EV Market Analysis", "Q4 2024 comprehensive analysis")

# Or directly
from perplSDK.research.automation import ResearchProject
project = ResearchProject("Project Name", "Description")
```

### Attributes

- `name` (str): Project name
- `description` (str): Project description
- `queries` (List[Dict]): List of research queries with metadata
- `results` (List[SearchResult]): Research results
- `created_at` (datetime): Project creation timestamp
- `updated_at` (datetime): Last update timestamp
- `metadata` (Dict): Custom project metadata

### Methods

#### add_query()

Add a research query to the project.

```python
def add_query(
    query: str,
    category: str = "general",
    priority: int = 1,
    **kwargs
)
```

**Parameters:**
- `query` (str): The research query
- `category` (str): Query category for organization (default: "general")
- `priority` (int): Query priority for execution order (default: 1)
- `**kwargs`: Additional query parameters

**Example:**
```python
project.add_query(
    "Current EV market share by manufacturer",
    category="market_analysis",
    priority=1
)
project.add_query(
    "EV charging infrastructure trends",
    category="infrastructure",
    priority=2
)
```

#### to_dict()

Convert project to dictionary for serialization.

```python
project_data = project.to_dict()
# Save to JSON
import json
with open("project.json", "w") as f:
    json.dump(project_data, f, indent=2)
```

## ResearchAutomation

Main class for automating research workflows.

### Initialization

```python
# Using environment configuration
research = ResearchAutomation()

# With custom configuration
config = Config(perplexity_api_key="your-key")
research = ResearchAutomation(config)
```

### Project Management

#### create_project()

Create a new research project.

```python
def create_project(name: str, description: str = "") -> ResearchProject
```

**Example:**
```python
project = research.create_project(
    "EV Battery Tech Analysis",
    "Comprehensive analysis of battery technology trends"
)
```

#### get_project()

Retrieve an existing project.

```python
def get_project(name: str) -> Optional[ResearchProject]
```

**Example:**
```python
project = research.get_project("EV Battery Tech Analysis")
if project:
    print(f"Found project with {len(project.queries)} queries")
```

#### list_projects()

List all project names.

```python
def list_projects() -> List[str]
```

**Example:**
```python
projects = research.list_projects()
print(f"Active projects: {', '.join(projects)}")
```

### Research Execution

#### conduct_research()

Execute research for a project.

```python
def conduct_research(
    project_name: str,
    queries: Optional[List[str]] = None,
    parallel: bool = True,
    save_results: bool = True
) -> ResearchProject
```

**Parameters:**
- `project_name` (str): Name of the project
- `queries` (List[str], optional): Additional queries to add
- `parallel` (bool): Execute queries in parallel (default: True)
- `save_results` (bool): Save results to project (default: True)

**Returns:**
- `ResearchProject`: Updated project with results

**Example:**
```python
# Execute existing project queries
project = research.conduct_research("EV Battery Tech Analysis", parallel=True)

# Add queries during execution
project = research.conduct_research(
    "EV Battery Tech Analysis",
    queries=[
        "Latest solid-state battery developments",
        "Battery recycling innovations"
    ]
)
```

#### generate_research_plan()

Generate a comprehensive research plan using templates.

```python
def generate_research_plan(
    topic: str,
    plan_type: str = "comprehensive",
    custom_categories: Optional[List[str]] = None
) -> List[str]
```

**Parameters:**
- `topic` (str): Research topic
- `plan_type` (str): Type of plan ("comprehensive", "quick", "deep", "market_analysis")
- `custom_categories` (List[str], optional): Custom query categories

**Returns:**
- `List[str]`: List of generated research queries

**Example:**
```python
# Generate comprehensive research plan
queries = research.generate_research_plan(
    "electric vehicles",
    plan_type="comprehensive"
)

# Create project and add queries
project = research.create_project("EV Research", "Comprehensive EV analysis")
for query in queries:
    project.add_query(query)
```

### Batch Operations

#### batch_research()

Execute multiple research queries across multiple projects.

```python
def batch_research(
    projects: List[str],
    parallel: bool = True
) -> Dict[str, ResearchProject]
```

**Parameters:**
- `projects` (List[str]): List of project names
- `parallel` (bool): Execute projects in parallel

**Returns:**
- `Dict[str, ResearchProject]`: Dictionary of updated projects

**Example:**
```python
results = research.batch_research(
    ["EV Market Analysis", "Battery Tech Analysis"],
    parallel=True
)
```

## Complete Workflow Example

### Basic Research Workflow

```python
from perplSDK.research.automation import ResearchAutomation

# Initialize
research = ResearchAutomation()

# Create project
project = research.create_project(
    "EV Market Analysis Q4 2024",
    "Comprehensive analysis of EV market trends"
)

# Add queries
project.add_query("Current EV market share by manufacturer", priority=1)
project.add_query("EV charging infrastructure growth", priority=2)
project.add_query("Battery technology innovations", priority=3)

# Execute research
project = research.conduct_research(project.name, parallel=True)

# Access results
for i, result in enumerate(project.results):
    print(f"\n=== Query {i+1} ===")
    print(result.content[:200])
    print(f"Sources: {len(result.sources)}")
```

### Using Research Templates

```python
from perplSDK.research.automation import ResearchAutomation

research = ResearchAutomation()

# Generate research plan
queries = research.generate_research_plan(
    "electric vehicle market",
    plan_type="market_analysis"
)

# Create and populate project
project = research.create_project("EV Market Deep Dive")
for query in queries:
    project.add_query(query)

# Execute
project = research.conduct_research(project.name)
```

### Iterative Research

```python
# Initial research
project = research.create_project("EV Technology")
project.add_query("Current state of EV battery technology")
project = research.conduct_research(project.name)

# Analyze initial results and add follow-up queries
if "solid-state" in project.results[0].content.lower():
    project.add_query("Solid-state battery timeline and challenges")
    project = research.conduct_research(project.name)
```

### Saving and Loading Projects

```python
import json

# Save project
project_data = project.to_dict()
with open("ev_research.json", "w") as f:
    json.dump(project_data, f, indent=2)

# Load project (manual restoration)
with open("ev_research.json", "r") as f:
    data = json.load(f)

project = research.create_project(data["name"], data["description"])
for query_data in data["queries"]:
    project.add_query(
        query_data["query"],
        category=query_data["category"],
        priority=query_data["priority"]
    )
```

## Advanced Usage

### Custom Query Prioritization

```python
# Add queries with priorities
project.add_query("Critical market data", priority=1)
project.add_query("Supporting trends", priority=2)
project.add_query("Background information", priority=3)

# Queries are executed in priority order when parallel=False
project = research.conduct_research(project.name, parallel=False)
```

### Query Categories

```python
# Organize queries by category
categories = {
    "market": ["market share", "sales trends"],
    "technology": ["battery tech", "charging speeds"],
    "policy": ["regulations", "incentives"]
}

for category, queries in categories.items():
    for query in queries:
        project.add_query(query, category=category)
```

### Metadata Tracking

```python
# Add custom metadata
project.metadata["analyst"] = "John Doe"
project.metadata["report_deadline"] = "2024-12-31"
project.metadata["stakeholders"] = ["Engineering", "Marketing"]

# Access metadata later
print(f"Analyst: {project.metadata['analyst']}")
```

## Performance Considerations

### Parallel vs Sequential Execution

```python
# Parallel execution - faster but more resource intensive
project = research.conduct_research(project.name, parallel=True)

# Sequential execution - slower but more controlled
project = research.conduct_research(project.name, parallel=False)
```

### Query Optimization

```python
# Batch related queries together
project.add_query("EV market share in North America, Europe, and Asia")

# Better than three separate queries:
# - "EV market share in North America"
# - "EV market share in Europe"
# - "EV market share in Asia"
```

## Error Handling

```python
from perplSDK.core.exceptions import APIError, RateLimitError

try:
    project = research.conduct_research("Project Name", parallel=True)
except RateLimitError:
    # Retry with sequential execution
    project = research.conduct_research("Project Name", parallel=False)
except APIError as e:
    print(f"Research failed: {e}")
```

## See Also

- [PerplexityClient API](client.md)
- [Market Intelligence](market_intelligence.md)
- [Research Templates](../guides/templates.md)
- [Automated Workflows](../guides/automation.md)
