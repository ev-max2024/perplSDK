# Trend Monitoring API Reference

The Trend Monitoring module enables detection, tracking, and analysis of emerging technology and market trends with comprehensive evolution tracking.

## Installation

```python
from perplSDK.research.trend_monitor import TrendMonitor, TrendData
```

## TrendMonitor Class

### Initialization

```python
trend_monitor = TrendMonitor(config=None)
```

**Parameters:**
- `config` (Optional[Config]): Configuration object

## Core Methods

### `add_trend_to_monitor(topic, category=None, monitoring_frequency="weekly")`

Add a new trend topic to monitor.

**Parameters:**
- `topic` (str): Trend topic to monitor
- `category` (Optional[str]): Category classification
- `monitoring_frequency` (str): Monitoring frequency
  - `"daily"`: Daily checks
  - `"weekly"`: Weekly checks
  - `"monthly"`: Monthly checks

**Example:**

```python
trend_monitor.add_trend_to_monitor(
    topic="solid-state battery technology",
    category="battery_technology",
    monitoring_frequency="weekly"
)
```

### `detect_emerging_trends(industry="electric_vehicles", time_period="current", min_confidence=0.6)`

Detect emerging trends in an industry.

**Parameters:**
- `industry` (str): Industry or sector to analyze
- `time_period` (str): Time period for trend detection
  - `"current"`: Current trends
  - `"monthly"`: Last month
  - `"quarterly"`: Last 3 months
  - `"yearly"`: Last year
- `min_confidence` (float): Minimum confidence score (0.0 - 1.0)

**Returns:**
- `List[Dict[str, Any]]`: List of detected trends with metadata

**Example:**

```python
trends = trend_monitor.detect_emerging_trends(
    industry="electric_vehicles",
    time_period="quarterly",
    min_confidence=0.7
)

for trend in trends:
    print(f"{trend['topic']}: {trend['confidence_score']:.1%}")
```

### `analyze_trend_evolution(trend_id, analysis_depth="standard")`

Analyze how a trend has evolved over time.

**Parameters:**
- `trend_id` (str): Trend identifier
- `analysis_depth` (str): Depth of analysis
  - `"basic"`: Basic evolution tracking
  - `"standard"`: Standard analysis with key metrics
  - `"comprehensive"`: Deep analysis with predictions

**Returns:**
- `Dict[str, Any]`: Trend evolution analysis

**Example:**

```python
evolution = trend_monitor.analyze_trend_evolution(
    trend_id="solid_state_batteries",
    analysis_depth="comprehensive"
)
```

### `get_trend_report(format="markdown", include_charts=False)`

Generate a comprehensive trend report.

**Parameters:**
- `format` (str): Report format (`"markdown"`, `"json"`, `"html"`)
- `include_charts` (bool): Whether to include charts/visualizations

**Returns:**
- `str` or `Dict`: Formatted trend report

**Example:**

```python
report = trend_monitor.get_trend_report(
    format="markdown",
    include_charts=False
)

# Save report
with open("trend_report.md", "w") as f:
    f.write(report)
```

### `compare_trends(trend_ids, comparison_metrics=None)`

Compare multiple trends side-by-side.

**Parameters:**
- `trend_ids` (List[str]): List of trend identifiers
- `comparison_metrics` (Optional[List[str]]): Metrics to compare

**Returns:**
- `Dict[str, Any]`: Comparison results

**Example:**

```python
comparison = trend_monitor.compare_trends(
    trend_ids=["trend_1", "trend_2", "trend_3"],
    comparison_metrics=["confidence_score", "momentum", "impact_assessment"]
)
```

## Data Models

### TrendData

```python
@dataclass
class TrendData:
    topic: str                      # Trend topic
    trend_type: str                 # emerging, growing, declining, stable
    confidence_score: float         # 0.0 - 1.0
    momentum: str                   # accelerating, steady, slowing
    timeframe: str                  # short_term, medium_term, long_term
    key_indicators: List[str]       # Key trend indicators
    related_topics: List[str]       # Related topics
    sources: List[str]              # Source URLs
    first_detected: datetime        # First detection timestamp
    last_updated: datetime          # Last update timestamp
    impact_assessment: str          # high, medium, low
    geographic_scope: str           # global, regional, local
```

## Trend Types

- **emerging**: New trends just appearing
- **growing**: Trends with increasing momentum
- **declining**: Trends losing momentum
- **stable**: Established trends with steady presence

## Momentum Types

- **accelerating**: Rapidly increasing attention/adoption
- **steady**: Consistent growth or presence
- **slowing**: Decreasing momentum

## Impact Assessment

- **high**: Major industry impact expected
- **medium**: Moderate impact on sector
- **low**: Limited or niche impact

## EV Industry Trend Categories

Pre-configured categories for EV industry:

```python
trend_monitor.ev_trend_categories = [
    "battery_technology",
    "charging_infrastructure",
    "autonomous_driving",
    "ev_adoption",
    "policy_regulations",
    "market_competition",
    "sustainability",
    "supply_chain"
]
```

## Advanced Features

### Continuous Monitoring

```python
# Set up continuous monitoring
trends_to_monitor = [
    ("solid-state batteries", "battery_technology"),
    ("ultra-fast charging", "charging_infrastructure"),
    ("vehicle-to-grid", "energy_storage")
]

for topic, category in trends_to_monitor:
    trend_monitor.add_trend_to_monitor(
        topic=topic,
        category=category,
        monitoring_frequency="weekly"
    )

# Get monitoring status
status = trend_monitor.get_monitoring_status()
```

### Trend Filtering

```python
# Filter by confidence score
high_confidence = [
    trend for trend in trends
    if trend['confidence_score'] > 0.75
]

# Filter by impact
high_impact = [
    trend for trend in trends
    if trend['impact_assessment'] == 'high'
]

# Filter by momentum
accelerating = [
    trend for trend in trends
    if trend['momentum'] == 'accelerating'
]
```

### Geographic Analysis

```python
# Compare trends across regions
regions = ["north_america", "europe", "asia"]

regional_trends = {}
for region in regions:
    trends = trend_monitor.detect_emerging_trends(
        industry="electric_vehicles",
        geographic_focus=region
    )
    regional_trends[region] = trends
```

## Integration with Reports

```python
from perplSDK.reports.formatter import MarkdownFormatter

# Detect trends
trends = trend_monitor.detect_emerging_trends(
    industry="electric_vehicles",
    time_period="quarterly"
)

# Format report
formatter = MarkdownFormatter()
report = formatter.format_trend_report(
    trends=trends,
    report_title="EV Industry Trend Analysis Q4 2024",
    include_detailed_analysis=True
)

# Save report
report_path = formatter.save_report(report, "ev_trends_q4_2024")
```

## Best Practices

1. **Set Appropriate Confidence Thresholds**: Use higher thresholds for critical decisions
2. **Regular Monitoring**: Set up consistent monitoring schedules
3. **Track Evolution**: Monitor how trends change over time
4. **Focus on High-Impact**: Prioritize high-impact trends
5. **Cross-Reference**: Validate trends across multiple sources
6. **Geographic Context**: Consider regional variations in trends

## Examples

### Complete Trend Analysis Workflow

```python
from perplSDK.research.trend_monitor import TrendMonitor
from perplSDK.reports.formatter import MarkdownFormatter

# Initialize
trend_monitor = TrendMonitor()

# Detect emerging trends
trends = trend_monitor.detect_emerging_trends(
    industry="electric_vehicles",
    time_period="quarterly",
    min_confidence=0.7
)

print(f"Detected {len(trends)} emerging trends")

# Add high-confidence trends to monitoring
for trend in trends:
    if trend['confidence_score'] > 0.8:
        trend_monitor.add_trend_to_monitor(
            topic=trend['topic'],
            category=trend.get('category', 'general'),
            monitoring_frequency="weekly"
        )

# Generate report
formatter = MarkdownFormatter()
report = formatter.format_trend_report(
    trends=trends,
    report_title="EV Trend Analysis",
    include_detailed_analysis=True
)

# Save
report_path = formatter.save_report(report, "ev_trends")
print(f"Report saved to: {report_path}")
```

### Multi-Category Analysis

```python
categories = [
    "battery_technology",
    "charging_infrastructure",
    "autonomous_driving"
]

category_trends = {}
for category in categories:
    trends = trend_monitor.detect_emerging_trends(
        industry=category,
        time_period="quarterly"
    )
    category_trends[category] = trends
    
    print(f"\n{category}:")
    print(f"  Total trends: {len(trends)}")
    print(f"  High impact: {sum(1 for t in trends if t['impact_assessment'] == 'high')}")
```

### Trend Evolution Tracking

```python
# Monitor a specific trend over time
trend_id = "solid_state_batteries"

# Initial detection
trend_monitor.add_trend_to_monitor(
    topic="solid-state battery technology",
    category="battery_technology"
)

# Analyze evolution after some time
evolution = trend_monitor.analyze_trend_evolution(
    trend_id=trend_id,
    analysis_depth="comprehensive"
)

print(f"Trend Type: {evolution['trend_type']}")
print(f"Momentum: {evolution['momentum']}")
print(f"Impact: {evolution['impact_assessment']}")
```

## See Also

- [Market Intelligence](market_intelligence.md)
- [Research Automation](research.md)
- [Report Generation](reports.md)
- [EV Industry Research Guide](../guides/ev_research.md)
