# Custom Templates Guide

This guide covers creating and using custom research templates with perplSDK to streamline repetitive research tasks and maintain consistency across analyses.

## Overview

Research templates provide pre-configured query sets and analysis patterns for common research scenarios. They help:
- Standardize research approaches
- Save time on recurring analyses
- Ensure comprehensive coverage
- Maintain consistency across reports

## Using Built-in Templates

### ResearchTemplate Class

```python
from perplSDK.utils.templates import ResearchTemplate

template = ResearchTemplate()

# Generate queries from template
queries = template.generate_template_queries("ev_market_analysis")

# Use in research project
from perplSDK import ResearchAutomation

research = ResearchAutomation()
project = research.create_project("EV Market Research")

for query in queries:
    project.add_query(query)

research.conduct_research(project.name)
```

## Built-in Templates

### EV Market Analysis

Comprehensive electric vehicle market research:

```python
queries = template.generate_template_queries("ev_market_analysis")

# Generates queries for:
# - Market size and growth
# - Key manufacturers and market share
# - Regional trends
# - Consumer adoption patterns
# - Technology developments
# - Policy and regulations
```

### Technology Assessment

Technology evaluation and analysis:

```python
queries = template.generate_template_queries("technology_assessment")

# Generates queries for:
# - Technology overview
# - Current state of development
# - Key players and innovations
# - Advantages and limitations
# - Market readiness
# - Future outlook
```

### Competitive Analysis

Competitor research and benchmarking:

```python
queries = template.generate_template_queries("competitive_analysis")

# Generates queries for:
# - Market positioning
# - Product/service offerings
# - Pricing strategies
# - Technology differentiation
# - Strengths and weaknesses
# - Strategic partnerships
```

### Trend Analysis

Market and technology trend research:

```python
queries = template.generate_template_queries("trend_analysis")

# Generates queries for:
# - Emerging trends
# - Growth patterns
# - Adoption rates
# - Influencing factors
# - Future projections
# - Industry impact
```

## Creating Custom Templates

### Basic Template Structure

```python
# custom_templates.py

class CustomResearchTemplate:
    """Custom research templates for specific needs."""
    
    def __init__(self):
        self.templates = {
            "battery_deep_dive": self._battery_template,
            "charging_infrastructure": self._charging_template,
            "policy_analysis": self._policy_template,
        }
    
    def generate_queries(self, template_name: str, **kwargs):
        """Generate queries from template."""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        return self.templates[template_name](**kwargs)
    
    def _battery_template(self, **kwargs):
        """Battery technology research template."""
        return [
            "Current state of battery technology",
            "Battery energy density improvements",
            "Battery cost reduction trends",
            "Solid-state battery developments",
            "Battery safety advancements",
            "Battery recycling and sustainability",
            "Battery supply chain analysis",
            "Future battery technology roadmap"
        ]
    
    def _charging_template(self, **kwargs):
        """Charging infrastructure research template."""
        geographic_focus = kwargs.get("geographic_focus", "global")
        
        return [
            f"EV charging infrastructure {geographic_focus}",
            f"Fast charging technology developments {geographic_focus}",
            f"Charging network deployment trends {geographic_focus}",
            f"Charging standards and interoperability {geographic_focus}",
            f"Grid integration challenges {geographic_focus}",
            f"Charging infrastructure investments {geographic_focus}"
        ]
    
    def _policy_template(self, **kwargs):
        """Policy analysis research template."""
        region = kwargs.get("region", "global")
        
        return [
            f"EV incentives and subsidies {region}",
            f"Emission regulations {region}",
            f"Manufacturing requirements {region}",
            f"Infrastructure mandates {region}",
            f"Trade policies affecting EVs {region}",
            f"Future policy roadmap {region}"
        ]
```

### Using Custom Templates

```python
from perplSDK import ResearchAutomation

# Initialize custom template
custom = CustomResearchTemplate()

# Create research project
research = ResearchAutomation()
project = research.create_project("Battery Deep Dive")

# Generate and add queries
queries = custom.generate_queries("battery_deep_dive")
for query in queries:
    project.add_query(query, category="battery_technology")

# Execute research
research.conduct_research(project.name, parallel=True)
```

## Parameterized Templates

### Industry-Specific Templates

```python
class IndustryTemplates:
    """Industry-specific research templates."""
    
    def automotive_template(self, focus_area: str, time_frame: str = "current"):
        """Automotive industry research."""
        base_queries = [
            f"{focus_area} in automotive industry",
            f"{focus_area} trends {time_frame}",
            f"{focus_area} key players and innovations",
            f"{focus_area} market size and growth",
            f"{focus_area} challenges and opportunities",
            f"{focus_area} future outlook"
        ]
        return base_queries
    
    def clean_energy_template(self, sector: str):
        """Clean energy sector research."""
        return [
            f"{sector} current market analysis",
            f"{sector} technology developments",
            f"{sector} policy and regulations",
            f"{sector} investment trends",
            f"{sector} adoption barriers",
            f"{sector} growth projections"
        ]
```

### Geographic Templates

```python
class GeographicTemplates:
    """Region-specific research templates."""
    
    def regional_analysis(self, topic: str, region: str):
        """Regional market analysis."""
        return [
            f"{topic} market overview in {region}",
            f"{topic} key players in {region}",
            f"{topic} regulatory environment in {region}",
            f"{topic} consumer behavior in {region}",
            f"{topic} infrastructure in {region}",
            f"{topic} growth opportunities in {region}"
        ]
```

## Template Categories

### Market Research Templates

```python
market_templates = {
    "market_entry": [
        "Market size and segmentation",
        "Competitive landscape",
        "Entry barriers and challenges",
        "Distribution channels",
        "Regulatory requirements",
        "Go-to-market strategies"
    ],
    
    "market_sizing": [
        "Total addressable market",
        "Serviceable addressable market",
        "Serviceable obtainable market",
        "Market growth rate",
        "Market drivers and restraints",
        "Market forecasts"
    ],
    
    "customer_research": [
        "Customer segments and personas",
        "Customer needs and pain points",
        "Buying behavior and decision factors",
        "Customer acquisition costs",
        "Customer lifetime value",
        "Churn and retention patterns"
    ]
}
```

### Technology Research Templates

```python
technology_templates = {
    "technology_evaluation": [
        "Technology maturity level",
        "Technical specifications",
        "Performance benchmarks",
        "Cost analysis",
        "Scalability considerations",
        "Integration requirements"
    ],
    
    "innovation_tracking": [
        "Recent innovations and breakthroughs",
        "Patent activity",
        "R&D investments",
        "Technology roadmaps",
        "Emerging alternatives",
        "Disruptive potential"
    ]
}
```

### Business Analysis Templates

```python
business_templates = {
    "swot_analysis": [
        "Company strengths",
        "Company weaknesses",
        "Market opportunities",
        "External threats",
        "Competitive advantages",
        "Strategic positioning"
    ],
    
    "financial_analysis": [
        "Revenue streams",
        "Cost structure",
        "Profitability metrics",
        "Investment requirements",
        "Financial risks",
        "Return on investment"
    ]
}
```

## Template Composition

### Combining Multiple Templates

```python
def comprehensive_analysis(topic: str):
    """Combine multiple templates for comprehensive analysis."""
    
    # Market perspective
    market_queries = CustomResearchTemplate().generate_queries(
        "market_analysis",
        topic=topic
    )
    
    # Technology perspective
    tech_queries = CustomResearchTemplate().generate_queries(
        "technology_assessment",
        topic=topic
    )
    
    # Competitive perspective
    comp_queries = CustomResearchTemplate().generate_queries(
        "competitive_analysis",
        topic=topic
    )
    
    # Combine all queries
    all_queries = market_queries + tech_queries + comp_queries
    
    return all_queries
```

### Hierarchical Templates

```python
class HierarchicalTemplate:
    """Templates with hierarchical query structure."""
    
    def generate_hierarchical_queries(self, topic: str):
        """Generate queries from broad to specific."""
        return {
            "overview": [
                f"{topic} overview and introduction",
                f"{topic} industry landscape"
            ],
            "detailed": [
                f"{topic} key players and market share",
                f"{topic} technology and innovations",
                f"{topic} market trends and dynamics"
            ],
            "specific": [
                f"{topic} regional analysis",
                f"{topic} segment analysis",
                f"{topic} use case studies"
            ],
            "future": [
                f"{topic} future outlook",
                f"{topic} growth projections",
                f"{topic} emerging opportunities"
            ]
        }
```

## Template Integration

### With Research Automation

```python
from perplSDK import ResearchAutomation

def execute_template_research(template_name: str, **kwargs):
    """Execute research using a template."""
    
    # Generate queries from template
    template = CustomResearchTemplate()
    queries = template.generate_queries(template_name, **kwargs)
    
    # Create and execute research project
    research = ResearchAutomation()
    project = research.create_project(f"Research: {template_name}")
    
    for query in queries:
        project.add_query(query)
    
    # Execute with parallel processing
    research.conduct_research(project.name, parallel=True)
    
    return project
```

### With Report Scheduler

```python
from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency

def schedule_template_report(template_name: str):
    """Schedule recurring report using template."""
    
    template = CustomResearchTemplate()
    queries = template.generate_queries(template_name)
    
    scheduler = ReportScheduler()
    report_id = scheduler.schedule_report(
        name=f"Weekly {template_name}",
        report_type=ReportType.RESEARCH,
        frequency=ReportFrequency.WEEKLY,
        config={
            "project_name": template_name,
            "queries": queries
        }
    )
    
    return report_id
```

## Best Practices

1. **Modular Design**: Create reusable template components
2. **Parameterization**: Make templates flexible with parameters
3. **Categorization**: Organize templates by use case
4. **Documentation**: Document template purpose and usage
5. **Versioning**: Version control template definitions
6. **Testing**: Test templates with sample data
7. **Maintenance**: Regularly update templates based on feedback

## Example Templates

### Comprehensive EV Analysis Template

```python
class EVAnalysisTemplate:
    """Comprehensive EV industry analysis templates."""
    
    def full_ev_analysis(self, geographic_focus: str = "global"):
        """Complete EV industry analysis."""
        
        queries = []
        
        # Market analysis
        queries.extend([
            f"EV market size and growth {geographic_focus}",
            f"EV market share by manufacturer {geographic_focus}",
            f"EV sales trends {geographic_focus}"
        ])
        
        # Technology
        queries.extend([
            f"EV battery technology developments {geographic_focus}",
            f"EV charging infrastructure {geographic_focus}",
            f"EV range and performance improvements"
        ])
        
        # Business
        queries.extend([
            f"EV pricing trends {geographic_focus}",
            f"EV cost of ownership analysis",
            f"EV incentives and subsidies {geographic_focus}"
        ])
        
        # Competition
        queries.extend([
            f"EV competitive landscape {geographic_focus}",
            f"New EV market entrants",
            f"EV strategic partnerships"
        ])
        
        # Future
        queries.extend([
            f"EV market forecasts {geographic_focus}",
            f"EV technology roadmap",
            f"EV adoption barriers and solutions"
        ])
        
        return queries
```

### Quarterly Business Review Template

```python
class QBRTemplate:
    """Quarterly business review template."""
    
    def generate_qbr(self, quarter: str, year: str):
        """Generate QBR research queries."""
        period = f"Q{quarter} {year}"
        
        return [
            f"Market performance {period}",
            f"Industry trends {period}",
            f"Competitive movements {period}",
            f"Technology developments {period}",
            f"Regulatory changes {period}",
            f"Customer sentiment {period}",
            f"Financial performance indicators {period}",
            f"Strategic opportunities {period}"
        ]
```

## Template Library Organization

```python
# template_library.py

class TemplateLibrary:
    """Central repository for all research templates."""
    
    def __init__(self):
        self.categories = {
            "market": MarketTemplates(),
            "technology": TechnologyTemplates(),
            "competitive": CompetitiveTemplates(),
            "geographic": GeographicTemplates(),
            "industry": IndustryTemplates()
        }
    
    def list_templates(self, category: str = None):
        """List available templates."""
        if category:
            return self.categories[category].list_templates()
        else:
            all_templates = {}
            for cat, templates in self.categories.items():
                all_templates[cat] = templates.list_templates()
            return all_templates
    
    def get_template(self, category: str, template_name: str):
        """Retrieve specific template."""
        return self.categories[category].get_template(template_name)
```

## See Also

- [Research Automation API](../api/research.md)
- [EV Industry Research Guide](ev_research.md)
- [Automated Workflows Guide](automation.md)
- [Configuration Guide](configuration.md)
