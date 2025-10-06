# Custom Templates Guide

This guide covers creating and using custom research templates, query patterns, and report templates in perplSDK.

## Overview

Templates in perplSDK provide:
- Pre-configured research query sets
- Reusable research patterns
- Industry-specific templates
- Custom report formats
- Query generation based on topics

## Research Templates

### Using Built-in Templates

```python
from perplSDK.utils.templates import ResearchTemplate

template = ResearchTemplate()

# Generate queries for a topic
queries = template.generate_queries(
    topic="electric vehicles",
    template_type="comprehensive"
)

print(f"Generated {len(queries)} queries:")
for query in queries:
    print(f"  - {query}")
```

### Template Types

#### 1. Comprehensive Template

Generates extensive queries covering multiple aspects.

```python
queries = template.generate_queries(
    topic="electric vehicles",
    template_type="comprehensive"
)

# Generates queries like:
# - "Current state of electric vehicles market"
# - "Electric vehicles technology trends"
# - "Electric vehicles competitive landscape"
# - "Electric vehicles consumer adoption"
# - "Electric vehicles regulatory environment"
```

#### 2. Quick Template

Generates focused queries for rapid insights.

```python
queries = template.generate_queries(
    topic="battery technology",
    template_type="quick"
)

# Generates queries like:
# - "Battery technology latest developments"
# - "Battery technology key trends"
# - "Battery technology market leaders"
```

#### 3. Deep Dive Template

Generates detailed technical queries.

```python
queries = template.generate_queries(
    topic="solid-state batteries",
    template_type="deep"
)

# Generates queries like:
# - "Solid-state batteries fundamental technology"
# - "Solid-state batteries manufacturing challenges"
# - "Solid-state batteries performance characteristics"
# - "Solid-state batteries commercialization timeline"
# - "Solid-state batteries competitive developments"
```

#### 4. Market Analysis Template

Generates market-focused queries.

```python
queries = template.generate_queries(
    topic="EV charging infrastructure",
    template_type="market_analysis"
)

# Generates queries like:
# - "EV charging infrastructure market size"
# - "EV charging infrastructure growth projections"
# - "EV charging infrastructure competitive landscape"
# - "EV charging infrastructure regional analysis"
# - "EV charging infrastructure investment trends"
```

## Creating Custom Templates

### Basic Custom Template

```python
class CustomResearchTemplate:
    """Custom research template for specific use cases."""
    
    def __init__(self):
        self.query_patterns = {
            "technology": [
                "{topic} latest innovations",
                "{topic} technical specifications",
                "{topic} performance metrics",
                "{topic} future roadmap"
            ],
            "market": [
                "{topic} market size and growth",
                "{topic} market share by player",
                "{topic} pricing trends",
                "{topic} regional distribution"
            ],
            "competitive": [
                "{topic} major competitors",
                "{topic} competitive advantages",
                "{topic} market positioning",
                "{topic} strategic initiatives"
            ]
        }
    
    def generate_queries(self, topic, categories=None):
        """Generate queries for given topic and categories."""
        if categories is None:
            categories = list(self.query_patterns.keys())
        
        queries = []
        for category in categories:
            if category in self.query_patterns:
                for pattern in self.query_patterns[category]:
                    queries.append(pattern.format(topic=topic))
        
        return queries

# Use custom template
custom_template = CustomResearchTemplate()
queries = custom_template.generate_queries(
    topic="electric vehicle batteries",
    categories=["technology", "market"]
)
```

### Industry-Specific Template

```python
class EVIndustryTemplate:
    """Template specifically for EV industry research."""
    
    def __init__(self):
        self.templates = {
            "vehicle_analysis": [
                "{manufacturer} electric vehicle lineup",
                "{manufacturer} EV pricing strategy",
                "{manufacturer} EV technology features",
                "{manufacturer} EV market position",
                "{manufacturer} EV sales performance"
            ],
            "technology_analysis": [
                "{technology} in electric vehicles",
                "{technology} adoption by manufacturers",
                "{technology} performance benefits",
                "{technology} cost implications",
                "{technology} future developments"
            ],
            "market_segment": [
                "{segment} electric vehicle market",
                "{segment} EV consumer preferences",
                "{segment} EV pricing in {segment}",
                "{segment} EV features and requirements"
            ]
        }
    
    def analyze_manufacturer(self, manufacturer):
        """Generate queries for manufacturer analysis."""
        return [q.format(manufacturer=manufacturer) 
                for q in self.templates["vehicle_analysis"]]
    
    def analyze_technology(self, technology):
        """Generate queries for technology analysis."""
        return [q.format(technology=technology) 
                for q in self.templates["technology_analysis"]]
    
    def analyze_segment(self, segment):
        """Generate queries for market segment analysis."""
        return [q.format(segment=segment) 
                for q in self.templates["market_segment"]]

# Use EV industry template
ev_template = EVIndustryTemplate()

# Analyze Tesla
tesla_queries = ev_template.analyze_manufacturer("Tesla")

# Analyze solid-state batteries
battery_queries = ev_template.analyze_technology("solid-state batteries")

# Analyze luxury segment
luxury_queries = ev_template.analyze_segment("luxury")
```

### Dynamic Template with Categories

```python
class DynamicResearchTemplate:
    """Dynamic template that adapts to different research needs."""
    
    def __init__(self):
        self.category_queries = {
            "overview": [
                "What is {topic}?",
                "{topic} current state and trends",
                "{topic} key players and stakeholders"
            ],
            "technology": [
                "{topic} technical specifications",
                "{topic} innovation and R&D",
                "{topic} technology roadmap"
            ],
            "market": [
                "{topic} market size and projections",
                "{topic} market dynamics and drivers",
                "{topic} regional market analysis"
            ],
            "competitive": [
                "{topic} competitive landscape",
                "{topic} market share analysis",
                "{topic} competitive strategies"
            ],
            "regulatory": [
                "{topic} regulatory framework",
                "{topic} compliance requirements",
                "{topic} policy developments"
            ],
            "consumer": [
                "{topic} consumer behavior",
                "{topic} adoption barriers",
                "{topic} user preferences"
            ],
            "financial": [
                "{topic} cost analysis",
                "{topic} pricing trends",
                "{topic} investment landscape"
            ],
            "future": [
                "{topic} future outlook",
                "{topic} emerging opportunities",
                "{topic} potential challenges"
            ]
        }
    
    def generate_research_plan(self, topic, depth="standard"):
        """Generate research plan based on depth."""
        if depth == "quick":
            categories = ["overview", "market"]
        elif depth == "standard":
            categories = ["overview", "technology", "market", "competitive"]
        elif depth == "comprehensive":
            categories = list(self.category_queries.keys())
        else:
            categories = depth  # Assume depth is list of categories
        
        queries = {}
        for category in categories:
            if category in self.category_queries:
                queries[category] = [
                    q.format(topic=topic)
                    for q in self.category_queries[category]
                ]
        
        return queries

# Use dynamic template
dynamic = DynamicResearchTemplate()

# Quick research
quick_plan = dynamic.generate_research_plan("EV charging", depth="quick")

# Comprehensive research
comprehensive_plan = dynamic.generate_research_plan(
    "battery recycling",
    depth="comprehensive"
)

# Custom categories
custom_plan = dynamic.generate_research_plan(
    "autonomous driving",
    depth=["technology", "regulatory", "future"]
)
```

## Report Templates

### Markdown Report Template

```python
class MarkdownReportTemplate:
    """Custom Markdown report template."""
    
    def __init__(self):
        self.template = """# {title}

**Date:** {date}
**Author:** {author}
**Version:** {version}

## Executive Summary

{executive_summary}

## Table of Contents

{toc}

## Introduction

{introduction}

## Key Findings

{key_findings}

## Detailed Analysis

{detailed_analysis}

## Market Insights

{market_insights}

## Technology Trends

{technology_trends}

## Competitive Landscape

{competitive_landscape}

## Recommendations

{recommendations}

## Conclusion

{conclusion}

## Appendix

### Methodology
{methodology}

### Data Sources
{data_sources}

### Glossary
{glossary}
"""
    
    def generate_report(self, **kwargs):
        """Generate report from template."""
        return self.template.format(**kwargs)

# Use template
template = MarkdownReportTemplate()
report = template.generate_report(
    title="EV Market Analysis Q4 2024",
    date="2024-12-01",
    author="Market Intelligence Team",
    version="1.0",
    executive_summary="Summary...",
    toc="1. Introduction\n2. Findings...",
    introduction="Introduction text...",
    key_findings="- Finding 1\n- Finding 2",
    # ... other sections
)
```

### Structured Report Template

```python
class StructuredReportTemplate:
    """Template with structured sections."""
    
    def __init__(self):
        self.sections = []
    
    def add_section(self, title, level, content):
        """Add a section to the report."""
        self.sections.append({
            "title": title,
            "level": level,
            "content": content
        })
    
    def add_executive_summary(self, key_points):
        """Add executive summary."""
        content = "## Executive Summary\n\n"
        for point in key_points:
            content += f"- {point}\n"
        self.add_section("Executive Summary", 2, content)
    
    def add_market_overview(self, market_data):
        """Add market overview section."""
        content = f"""## Market Overview

**Market Size:** {market_data.get('size', 'N/A')}
**Growth Rate:** {market_data.get('growth_rate', 'N/A')}
**Key Players:** {', '.join(market_data.get('players', []))}

{market_data.get('description', '')}
"""
        self.add_section("Market Overview", 2, content)
    
    def add_trend_analysis(self, trends):
        """Add trend analysis section."""
        content = "## Trend Analysis\n\n"
        for trend in trends:
            content += f"### {trend['name']}\n\n"
            content += f"**Momentum:** {trend['momentum']:.2f}\n\n"
            content += f"{trend['description']}\n\n"
        self.add_section("Trend Analysis", 2, content)
    
    def generate(self, title, metadata=None):
        """Generate complete report."""
        report = f"# {title}\n\n"
        
        if metadata:
            report += "**Metadata:**\n"
            for key, value in metadata.items():
                report += f"- **{key}:** {value}\n"
            report += "\n"
        
        for section in self.sections:
            report += section['content'] + "\n\n"
        
        return report

# Use structured template
report_builder = StructuredReportTemplate()

report_builder.add_executive_summary([
    "EV market grew 35% in 2024",
    "Battery costs decreased 15%",
    "Charging infrastructure expanded significantly"
])

report_builder.add_market_overview({
    "size": "$580 billion",
    "growth_rate": "35% YoY",
    "players": ["Tesla", "BYD", "Volkswagen"],
    "description": "The EV market continues strong growth..."
})

report_builder.add_trend_analysis(trends)

final_report = report_builder.generate(
    "Q4 2024 EV Market Report",
    metadata={
        "Date": "2024-12-01",
        "Author": "Research Team",
        "Classification": "Internal"
    }
)
```

## Query Pattern Templates

### Question-Based Pattern

```python
class QuestionBasedTemplate:
    """Template that generates question-style queries."""
    
    def __init__(self):
        self.question_types = {
            "what": ["What is {topic}?", "What are the key aspects of {topic}?"],
            "how": ["How does {topic} work?", "How is {topic} evolving?"],
            "why": ["Why is {topic} important?", "Why are companies investing in {topic}?"],
            "when": ["When will {topic} be widely adopted?", "When did {topic} emerge?"],
            "who": ["Who are the leaders in {topic}?", "Who is investing in {topic}?"],
            "where": ["Where is {topic} being deployed?", "Where is {topic} most advanced?"]
        }
    
    def generate_questions(self, topic, question_types=None):
        """Generate question-based queries."""
        if question_types is None:
            question_types = list(self.question_types.keys())
        
        questions = []
        for qtype in question_types:
            if qtype in self.question_types:
                for pattern in self.question_types[qtype]:
                    questions.append(pattern.format(topic=topic))
        
        return questions

# Use question-based template
question_template = QuestionBasedTemplate()
questions = question_template.generate_questions("solid-state batteries")
```

### Comparison Template

```python
class ComparisonTemplate:
    """Template for comparison research."""
    
    def compare_technologies(self, tech1, tech2):
        """Generate queries to compare two technologies."""
        return [
            f"Compare {tech1} vs {tech2}",
            f"{tech1} advantages over {tech2}",
            f"{tech2} advantages over {tech1}",
            f"{tech1} and {tech2} cost comparison",
            f"{tech1} and {tech2} performance comparison",
            f"Market adoption: {tech1} vs {tech2}"
        ]
    
    def compare_companies(self, company1, company2, focus_areas=None):
        """Generate queries to compare companies."""
        if focus_areas is None:
            focus_areas = ["market_share", "technology", "strategy"]
        
        queries = [f"Compare {company1} and {company2}"]
        
        for area in focus_areas:
            queries.append(f"{company1} vs {company2} {area}")
        
        return queries

# Use comparison template
comparison = ComparisonTemplate()

tech_queries = comparison.compare_technologies(
    "lithium-ion batteries",
    "solid-state batteries"
)

company_queries = comparison.compare_companies(
    "Tesla",
    "BYD",
    focus_areas=["technology", "market_share", "pricing"]
)
```

### Time-Based Template

```python
class TimeBasedTemplate:
    """Template for time-series analysis."""
    
    def generate_historical_queries(self, topic, years_back=5):
        """Generate queries for historical analysis."""
        current_year = datetime.now().year
        queries = []
        
        for year in range(current_year - years_back, current_year + 1):
            queries.append(f"{topic} in {year}")
            queries.append(f"{topic} trends {year}")
        
        return queries
    
    def generate_forecast_queries(self, topic, years_ahead=5):
        """Generate queries for future analysis."""
        current_year = datetime.now().year
        queries = []
        
        for year in range(current_year, current_year + years_ahead + 1):
            queries.append(f"{topic} predictions for {year}")
            queries.append(f"{topic} outlook {year}")
        
        return queries
    
    def generate_trend_queries(self, topic):
        """Generate queries for trend analysis over time."""
        return [
            f"{topic} historical trends",
            f"{topic} evolution over time",
            f"{topic} past, present, and future",
            f"{topic} timeline and milestones",
            f"{topic} year-over-year changes"
        ]

# Use time-based template
time_template = TimeBasedTemplate()

historical = time_template.generate_historical_queries("EV market", years_back=3)
forecast = time_template.generate_forecast_queries("EV adoption", years_ahead=5)
trends = time_template.generate_trend_queries("battery technology")
```

## Integration Examples

### Using Templates with Research Automation

```python
from perplSDK.research.automation import ResearchAutomation
from perplSDK.utils.templates import ResearchTemplate

# Initialize
research = ResearchAutomation()
template = ResearchTemplate()

# Generate queries from template
queries = template.generate_queries(
    "electric vehicle charging",
    template_type="comprehensive"
)

# Create project and add queries
project = research.create_project("EV Charging Analysis")
for query in queries:
    project.add_query(query)

# Execute research
project = research.conduct_research(project.name, parallel=True)
```

### Combining Multiple Templates

```python
# Combine different template types
ev_template = EVIndustryTemplate()
question_template = QuestionBasedTemplate()
comparison_template = ComparisonTemplate()

# Collect queries from different templates
all_queries = []

# Technology analysis
all_queries.extend(ev_template.analyze_technology("fast charging"))

# Question-based exploration
all_queries.extend(question_template.generate_questions("ultra-fast charging"))

# Comparison
all_queries.extend(comparison_template.compare_technologies(
    "DC fast charging",
    "ultra-fast charging"
))

# Create comprehensive project
project = research.create_project("Comprehensive Charging Analysis")
for query in all_queries:
    project.add_query(query)
```

### Template-Based Scheduled Research

```python
from perplSDK.reports.scheduler import ReportScheduler

def template_based_research():
    """Automated research using templates."""
    template = ResearchTemplate()
    research = ResearchAutomation()
    
    # Generate weekly research plan
    queries = template.generate_queries(
        "electric vehicles",
        template_type="quick"  # Quick update
    )
    
    project = research.create_project("Weekly Update")
    for query in queries:
        project.add_query(query)
    
    research.conduct_research(project.name)

# Schedule weekly
import schedule
schedule.every().monday.at("09:00").do(template_based_research)
```

## Best Practices

### 1. Keep Templates Flexible

```python
class FlexibleTemplate:
    """Template that can be easily customized."""
    
    def __init__(self, custom_patterns=None):
        self.patterns = {
            "default": ["{topic} analysis", "{topic} trends"],
            **(custom_patterns or {})
        }
    
    def add_pattern(self, category, patterns):
        """Add custom pattern at runtime."""
        self.patterns[category] = patterns
```

### 2. Version Your Templates

```python
class VersionedTemplate:
    """Template with version tracking."""
    
    VERSION = "2.0"
    LAST_UPDATED = "2024-12-01"
    
    def __init__(self):
        self.metadata = {
            "version": self.VERSION,
            "last_updated": self.LAST_UPDATED
        }
```

### 3. Document Templates

```python
class DocumentedTemplate:
    """Well-documented template."""
    
    def generate_queries(self, topic, depth="standard"):
        """
        Generate research queries for a topic.
        
        Args:
            topic: Research topic
            depth: Research depth ("quick", "standard", "comprehensive")
        
        Returns:
            List of research queries
        
        Examples:
            >>> template = DocumentedTemplate()
            >>> queries = template.generate_queries("EVs", "quick")
        """
        pass
```

### 4. Test Templates

```python
def test_template():
    """Test template generation."""
    template = CustomResearchTemplate()
    
    # Test query generation
    queries = template.generate_queries("test topic")
    assert len(queries) > 0
    assert all(isinstance(q, str) for q in queries)
    
    print("✓ Template tests passed")

test_template()
```

## See Also

- [Research Automation API](../api/research.md)
- [EV Research Guide](ev_research.md)
- [Automated Workflows](automation.md)
