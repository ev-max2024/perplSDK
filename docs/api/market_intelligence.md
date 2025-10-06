# Market Intelligence API Reference

The Market Intelligence module provides comprehensive market analysis capabilities with sector-specific insights, competitive analysis, and performance intelligence including the COPILOT feature.

## Installation

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector
```

## MarketIntelligence Class

### Initialization

```python
market_intel = MarketIntelligence(config=None)
```

**Parameters:**
- `config` (Optional[Config]): Configuration object

## Market Sectors

### MarketSector Enum

Available market sectors for analysis:

```python
MarketSector.ELECTRIC_VEHICLES          # Electric vehicle industry
MarketSector.AUTOMOTIVE                 # General automotive
MarketSector.CLEAN_ENERGY              # Clean energy sector
MarketSector.BATTERY_TECHNOLOGY        # Battery innovations
MarketSector.CHARGING_INFRASTRUCTURE   # EV charging
MarketSector.AUTONOMOUS_VEHICLES       # Self-driving vehicles
MarketSector.MOBILITY_SERVICES         # Transportation services
MarketSector.ENERGY_STORAGE           # Energy storage solutions
MarketSector.PERFORMANCE              # Performance optimization
```

## Core Methods

### `generate_market_queries(sector, analysis_type="comprehensive", time_frame="current", geographic_focus=None)`

Generate market research queries for a specific sector.

**Parameters:**
- `sector` (MarketSector): Market sector to analyze
- `analysis_type` (str): Analysis type
  - `"comprehensive"`: Complete market analysis
  - `"trends"`: Market trends only
  - `"competitive"`: Competitive landscape
  - `"opportunities"`: Growth opportunities
  - `"risks"`: Risk assessment
- `time_frame` (str): Time frame for analysis
  - `"current"`: Current state
  - `"quarterly"`: Last 3 months
  - `"yearly"`: Last 12 months
  - `"5year"`: Long-term trends
- `geographic_focus` (Optional[str]): Geographic region
  - `"global"`, `"north_america"`, `"europe"`, `"asia"`, `"china"`, etc.

**Returns:**
- `List[str]`: Generated market research queries

**Example:**

```python
queries = market_intel.generate_market_queries(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive",
    time_frame="current",
    geographic_focus="north_america"
)
```

### `conduct_market_analysis(sector, analysis_type="comprehensive", time_frame="current", geographic_focus=None, save_report=True)`

Conduct comprehensive market analysis.

**Parameters:**
Same as `generate_market_queries()` plus:
- `save_report` (bool): Whether to save the analysis report

**Returns:**
- `Dict[str, Any]`: Analysis results containing:
  - `sector`: Market sector analyzed
  - `queries`: Queries executed
  - `insights`: List of MarketInsight objects
  - `summary`: Executive summary
  - `report_path`: Path to saved report (if saved)

**Example:**

```python
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive",
    time_frame="current"
)

print(f"Generated {len(analysis['insights'])} insights")
```

### `extract_insights(results, sector)`

Extract structured insights from search results.

**Parameters:**
- `results` (List[SearchResult]): Search results
- `sector` (MarketSector): Market sector

**Returns:**
- `List[MarketInsight]`: Extracted insights

## COPILOT - Performance Intelligence

### `conduct_performance_intelligence(context="general", time_frame="current", geographic_focus=None, custom_queries=None)`

Execute super fast performance intelligence analysis.

**Parameters:**
- `context` (str): Analysis context
  - `"general"`: High-performance innovations across industries
  - `"ev"`: EV-specific performance analysis
  - `"manufacturing"`: Manufacturing performance optimization
  - `"operations"`: Operational performance
- `time_frame` (str): Time frame for analysis
- `geographic_focus` (Optional[str]): Geographic region
- `custom_queries` (Optional[List[str]]): Additional custom queries

**Returns:**
- `Dict[str, Any]`: Performance analysis containing:
  - `context`: Analysis context
  - `insights`: Performance insights
  - `performance_metrics`: Key metrics
  - `recommendations`: Strategic recommendations
  - `report_path`: Path to saved report

**Performance Metrics:**
- `total_insights`: Total number of insights
- `super_fast_count`: Number of super fast insights
- `super_fast_percentage`: Percentage of super fast insights
- `high_impact_count`: Number of high-impact opportunities
- `average_confidence`: Average confidence score

**Example:**

```python
# EV performance analysis
analysis = market_intel.conduct_performance_intelligence(
    context="ev",
    time_frame="current",
    geographic_focus="global"
)

metrics = analysis['performance_metrics']
print(f"Super Fast Insights: {metrics['super_fast_count']}")
print(f"Average Confidence: {metrics['average_confidence']:.1%}")

# Access recommendations
for rec in analysis['recommendations']:
    print(f"- {rec}")
```

## Competitive Analysis

### `analyze_competitors(sector, companies=None, focus_areas=None)`

Analyze competitive landscape.

**Parameters:**
- `sector` (MarketSector): Market sector
- `companies` (Optional[List[str]]): Specific companies to analyze
- `focus_areas` (Optional[List[str]]): Specific focus areas

**Returns:**
- `Dict[str, Any]`: Competitive analysis results

**Example:**

```python
competitive_analysis = market_intel.analyze_competitors(
    sector=MarketSector.ELECTRIC_VEHICLES,
    companies=["Tesla", "BYD", "Volkswagen"],
    focus_areas=["market_share", "technology", "pricing"]
)
```

## Data Models

### MarketInsight

```python
@dataclass
class MarketInsight:
    title: str                    # Insight title
    content: str                  # Detailed content
    sector: MarketSector         # Market sector
    impact_level: str            # high, medium, low
    time_relevance: str          # immediate, short_term, long_term
    sources: List[str]           # Source URLs
    confidence_score: float      # 0.0 - 1.0
    generated_at: datetime       # Timestamp
    tags: List[str]             # Classification tags
```

## EV MAX INC Focus Areas

Pre-configured focus areas for EV MAX INC:

```python
market_intel.ev_max_focus_areas = [
    "electric vehicle market trends",
    "EV charging infrastructure development",
    "battery technology innovations",
    "EV policy and regulations",
    "competitive landscape in EV industry",
    "consumer adoption patterns for EVs",
    "EV market share analysis",
    "sustainability trends in automotive"
]
```

## Advanced Usage

### Custom Sector Analysis

```python
# Multi-sector analysis
sectors = [
    MarketSector.ELECTRIC_VEHICLES,
    MarketSector.BATTERY_TECHNOLOGY,
    MarketSector.CHARGING_INFRASTRUCTURE
]

for sector in sectors:
    analysis = market_intel.conduct_market_analysis(
        sector=sector,
        time_frame="quarterly"
    )
    print(f"{sector.value}: {len(analysis['insights'])} insights")
```

### Geographic Comparison

```python
regions = ["north_america", "europe", "asia"]

for region in regions:
    analysis = market_intel.conduct_market_analysis(
        sector=MarketSector.ELECTRIC_VEHICLES,
        geographic_focus=region
    )
```

### Integration with Reports

```python
from perplSDK.reports.formatter import MarkdownFormatter

# Conduct analysis
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES
)

# Format report
formatter = MarkdownFormatter()
report = formatter.format_market_intelligence_report(
    analysis_results=analysis,
    sector=MarketSector.ELECTRIC_VEHICLES
)

# Save
formatter.save_report(report, "ev_market_intelligence")
```

## Best Practices

1. **Choose Appropriate Sector**: Select the most relevant market sector
2. **Define Analysis Scope**: Use time_frame and geographic_focus appropriately
3. **Focus on High-Impact**: Prioritize insights with high impact_level
4. **Monitor Confidence**: Review confidence_score for reliability
5. **Use COPILOT**: Leverage performance intelligence for optimization
6. **Regular Updates**: Conduct periodic analyses to track changes

## Examples

### Complete Market Intelligence Workflow

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

# Initialize
market_intel = MarketIntelligence()

# Conduct comprehensive analysis
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive",
    time_frame="current",
    geographic_focus="global",
    save_report=True
)

# Extract high-impact insights
high_impact = [
    insight for insight in analysis['insights']
    if insight.impact_level == "high"
]

print(f"High-Impact Insights: {len(high_impact)}")
for insight in high_impact:
    print(f"\n{insight.title}")
    print(f"Confidence: {insight.confidence_score:.1%}")
    print(f"Time Relevance: {insight.time_relevance}")
```

### COPILOT Performance Analysis

```python
# Multiple context analysis
contexts = ["general", "ev", "manufacturing", "operations"]

for context in contexts:
    analysis = market_intel.conduct_performance_intelligence(
        context=context,
        time_frame="current"
    )
    
    metrics = analysis['performance_metrics']
    print(f"\n{context.upper()} Context:")
    print(f"  Super Fast Insights: {metrics['super_fast_count']}")
    print(f"  High Impact: {metrics['high_impact_count']}")
```

## See Also

- [Research Automation](research.md)
- [Trend Monitoring](trend_monitoring.md)
- [COPILOT Guide](../COPILOT_GUIDE.md)
- [EV Industry Research Guide](../guides/ev_research.md)
