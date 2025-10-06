# Market Intelligence API

The Market Intelligence module provides specialized tools for conducting comprehensive market analysis, with built-in support for the electric vehicle industry and general market research.

## Overview

Market intelligence features:
- EV-focused market analysis
- COPILOT - Super Fast Performance Intelligence
- Market sector analysis
- Competitive intelligence
- Trend identification and tracking
- Strategic recommendations
- Geographic market analysis

## Installation

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector
```

## MarketSector Enum

Predefined market sectors for analysis:

```python
class MarketSector:
    ELECTRIC_VEHICLES = "electric_vehicles"
    BATTERIES = "batteries"
    CHARGING_INFRASTRUCTURE = "charging_infrastructure"
    AUTOMOTIVE = "automotive"
    ENERGY = "energy"
    TECHNOLOGY = "technology"
```

## MarketIntelligence

Main class for market intelligence operations.

### Initialization

```python
# Using environment configuration
market_intel = MarketIntelligence()

# With custom configuration
from perplSDK.core.config import Config
config = Config(perplexity_api_key="your-key")
market_intel = MarketIntelligence(config)
```

### Market Analysis

#### conduct_market_analysis()

Perform comprehensive market analysis.

```python
def conduct_market_analysis(
    sector: MarketSector,
    analysis_type: str = "comprehensive",
    geographic_focus: Optional[str] = None,
    time_frame: str = "current",
    custom_queries: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `sector` (MarketSector): Market sector to analyze
- `analysis_type` (str): Analysis depth ("comprehensive", "quick", "trends", "competitive")
- `geographic_focus` (str, optional): Geographic region ("north_america", "europe", "asia", "global")
- `time_frame` (str): Time frame for analysis ("current", "historical", "future")
- `custom_queries` (List[str], optional): Additional custom queries

**Returns:**
- `Dict[str, Any]`: Analysis results with market insights, trends, and recommendations

**Example:**
```python
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive",
    geographic_focus="north_america",
    time_frame="current"
)

print(f"Market Size: {analysis['market_overview']['size']}")
print(f"Key Players: {analysis['competitive_landscape']['major_players']}")
print(f"Trends: {analysis['trends']}")
```

### Performance Intelligence (COPILOT)

#### conduct_performance_intelligence()

COPILOT - Super Fast Performance Intelligence analysis.

```python
def conduct_performance_intelligence(
    context: str = "general",
    time_frame: str = "current",
    geographic_focus: Optional[str] = None,
    custom_queries: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `context` (str): Performance context ("general", "ev", "manufacturing", "operations")
- `time_frame` (str): Time frame for analysis
- `geographic_focus` (str, optional): Geographic region
- `custom_queries` (List[str], optional): Additional queries

**Returns:**
- `Dict[str, Any]`: Performance intelligence with metrics and recommendations

**Context Types:**
- **general**: High-performance technology innovations and optimization
- **ev**: Electric vehicle performance, acceleration, fast charging
- **manufacturing**: Production speed, efficiency, automation
- **operations**: Business process performance and workflow optimization

**Example:**
```python
# EV performance analysis
performance = market_intel.conduct_performance_intelligence(
    context="ev",
    time_frame="current",
    geographic_focus="north_america"
)

print(f"Super Fast Insights: {performance['performance_metrics']['super_fast_count']}")
print(f"High Impact Items: {performance['performance_metrics']['high_impact_count']}")
print("\nRecommendations:")
for rec in performance['recommendations']:
    print(f"- {rec}")

# Manufacturing performance
mfg_performance = market_intel.conduct_performance_intelligence(
    context="manufacturing",
    custom_queries=["lean manufacturing best practices"]
)
```

### EV-Specific Analysis

#### get_ev_max_insights()

Get EV MAX specific insights and recommendations.

```python
def get_ev_max_insights(
    focus_areas: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `focus_areas` (List[str], optional): Specific areas of focus

**Returns:**
- `Dict[str, Any]`: EV MAX specific insights and strategic recommendations

**Example:**
```python
insights = market_intel.get_ev_max_insights(
    focus_areas=["battery_technology", "charging_infrastructure", "market_expansion"]
)

print("Strategic Recommendations:")
for rec in insights['recommendations']:
    print(f"- {rec}")
    
print("\nOpportunities:")
for opp in insights['opportunities']:
    print(f"- {opp}")
```

#### analyze_ev_market_trends()

Analyze specific EV market trends.

```python
def analyze_ev_market_trends(
    trend_categories: Optional[List[str]] = None,
    time_period: str = "current"
) -> Dict[str, Any]
```

**Parameters:**
- `trend_categories` (List[str], optional): Categories to analyze
- `time_period` (str): Time period for trend analysis

**Returns:**
- `Dict[str, Any]`: Trend analysis results

**Example:**
```python
trends = market_intel.analyze_ev_market_trends(
    trend_categories=["technology", "consumer_behavior", "policy"],
    time_period="6_months"
)
```

### Competitive Intelligence

#### analyze_competitors()

Analyze competitive landscape.

```python
def analyze_competitors(
    sector: MarketSector,
    competitors: Optional[List[str]] = None,
    focus_areas: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `sector` (MarketSector): Market sector
- `competitors` (List[str], optional): Specific competitors to analyze
- `focus_areas` (List[str], optional): Areas to focus on

**Returns:**
- `Dict[str, Any]`: Competitive analysis results

**Example:**
```python
competitive_analysis = market_intel.analyze_competitors(
    sector=MarketSector.ELECTRIC_VEHICLES,
    competitors=["Tesla", "BYD", "Volkswagen"],
    focus_areas=["technology", "market_share", "innovation"]
)
```

## Complete Workflow Examples

### Comprehensive Market Analysis

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

# Initialize
market_intel = MarketIntelligence()

# Conduct comprehensive analysis
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive",
    geographic_focus="global"
)

# Extract key insights
print("=== Market Overview ===")
print(f"Size: {analysis['market_overview']['size']}")
print(f"Growth Rate: {analysis['market_overview']['growth_rate']}")

print("\n=== Key Trends ===")
for trend in analysis['trends']:
    print(f"- {trend}")

print("\n=== Recommendations ===")
for rec in analysis['recommendations']:
    print(f"- {rec}")
```

### COPILOT Performance Intelligence

```python
# General performance intelligence
general_perf = market_intel.conduct_performance_intelligence(
    context="general"
)

# EV-specific performance
ev_perf = market_intel.conduct_performance_intelligence(
    context="ev",
    time_frame="current"
)

# Manufacturing performance
mfg_perf = market_intel.conduct_performance_intelligence(
    context="manufacturing",
    custom_queries=["automation technologies", "efficiency metrics"]
)

# Compare performance metrics
print(f"EV Super Fast Count: {ev_perf['performance_metrics']['super_fast_count']}")
print(f"Manufacturing High Impact: {mfg_perf['performance_metrics']['high_impact_count']}")
```

### Multi-Region Analysis

```python
regions = ["north_america", "europe", "asia"]
regional_analysis = {}

for region in regions:
    analysis = market_intel.conduct_market_analysis(
        sector=MarketSector.ELECTRIC_VEHICLES,
        analysis_type="quick",
        geographic_focus=region
    )
    regional_analysis[region] = analysis

# Compare regions
for region, analysis in regional_analysis.items():
    print(f"{region}: {analysis['market_overview']['size']}")
```

### Combined Intelligence Workflow

```python
# 1. Market analysis
market_analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive"
)

# 2. Performance intelligence
performance = market_intel.conduct_performance_intelligence(
    context="ev"
)

# 3. EV MAX specific insights
ev_max_insights = market_intel.get_ev_max_insights()

# 4. Competitive analysis
competitive = market_intel.analyze_competitors(
    sector=MarketSector.ELECTRIC_VEHICLES,
    competitors=["Tesla", "BYD"]
)

# Aggregate insights
all_insights = {
    "market": market_analysis,
    "performance": performance,
    "ev_max": ev_max_insights,
    "competitive": competitive
}
```

## Advanced Features

### Custom Query Integration

```python
custom_queries = [
    "Impact of government subsidies on EV adoption",
    "Battery supply chain constraints",
    "Charging infrastructure investment trends"
]

analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    custom_queries=custom_queries
)
```

### Trend Tracking Over Time

```python
# Historical analysis
historical = market_intel.conduct_market_analysis(
    sector=MarketSector.BATTERIES,
    time_frame="historical"
)

# Current analysis
current = market_intel.conduct_market_analysis(
    sector=MarketSector.BATTERIES,
    time_frame="current"
)

# Compare trends
historical_trends = historical['trends']
current_trends = current['trends']
```

### Strategic Planning

```python
# Get strategic insights for EV MAX
insights = market_intel.get_ev_max_insights(
    focus_areas=[
        "product_development",
        "market_expansion",
        "technology_partnerships",
        "competitive_positioning"
    ]
)

# Generate strategic recommendations
print("Strategic Action Plan:")
for i, rec in enumerate(insights['recommendations'], 1):
    print(f"{i}. {rec}")
```

## Integration with Other Modules

### With Research Automation

```python
from perplSDK.research.automation import ResearchAutomation

research = ResearchAutomation()
market_intel = MarketIntelligence()

# Create research project based on market intelligence
insights = market_intel.get_ev_max_insights()
project = research.create_project("EV MAX Strategic Research")

for opportunity in insights['opportunities']:
    project.add_query(f"Detailed analysis: {opportunity}")

research.conduct_research(project.name)
```

### With Report Generation

```python
from perplSDK.reports.formatter import MarkdownFormatter

formatter = MarkdownFormatter()

# Conduct analysis
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES
)

# Format as report
report = formatter.format_market_intelligence_report(
    analysis=analysis,
    title="Q4 2024 EV Market Intelligence Report"
)

formatter.save_report(report, "ev_market_intelligence")
```

## Best Practices

### 1. Choose Appropriate Analysis Type

```python
# Quick analysis for rapid insights
quick = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="quick"
)

# Comprehensive for detailed strategic planning
comprehensive = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive"
)
```

### 2. Use Geographic Focus

```python
# Regional strategy
regional = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    geographic_focus="north_america"
)

# Global strategy
global_analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    geographic_focus="global"
)
```

### 3. Combine Multiple Contexts

```python
# Get complete performance picture
contexts = ["general", "ev", "manufacturing", "operations"]
performance_data = {}

for context in contexts:
    performance_data[context] = market_intel.conduct_performance_intelligence(
        context=context
    )
```

## See Also

- [Research Automation](research.md)
- [Trend Monitoring](trend_monitoring.md)
- [Report Generation](reports.md)
- [EV Industry Research Guide](../guides/ev_research.md)
