# Trend Monitoring API

The Trend Monitoring module provides tools for detecting emerging trends, tracking trend evolution, and analyzing market dynamics over time.

## Overview

Trend monitoring capabilities:
- Emerging trend detection
- Trend evolution tracking
- Multi-domain trend analysis
- Trend momentum calculation
- Historical trend comparison
- Automated trend alerts

## Installation

```python
from perplSDK.research.trend_monitor import TrendMonitor
```

## TrendMonitor

Main class for trend monitoring operations.

### Initialization

```python
# Using environment configuration
trend_monitor = TrendMonitor()

# With custom configuration
from perplSDK.core.config import Config
config = Config(perplexity_api_key="your-key")
trend_monitor = TrendMonitor(config)
```

### Trend Detection

#### detect_emerging_trends()

Detect emerging trends across specified domains.

```python
def detect_emerging_trends(
    search_domains: List[str],
    time_window: str = "month",
    min_momentum: float = 0.5,
    max_trends: int = 10
) -> List[Dict[str, Any]]
```

**Parameters:**
- `search_domains` (List[str]): Domains to search for trends
- `time_window` (str): Time window for trend detection ("day", "week", "month", "quarter", "year")
- `min_momentum` (float): Minimum momentum score (0.0-1.0)
- `max_trends` (int): Maximum number of trends to return

**Returns:**
- `List[Dict[str, Any]]`: List of detected trends with metadata

**Example:**
```python
trends = trend_monitor.detect_emerging_trends(
    search_domains=["electric vehicles", "battery technology", "autonomous driving"],
    time_window="month",
    min_momentum=0.6,
    max_trends=15
)

for trend in trends:
    print(f"Trend: {trend['name']}")
    print(f"Momentum: {trend['momentum']:.2f}")
    print(f"Domain: {trend['domain']}")
    print(f"Description: {trend['description']}")
    print("---")
```

#### monitor_trend_evolution()

Monitor how a specific trend evolves over time.

```python
def monitor_trend_evolution(
    trend_name: str,
    days_back: int = 30,
    check_points: int = 5
) -> Dict[str, Any]
```

**Parameters:**
- `trend_name` (str): Name of the trend to monitor
- `days_back` (int): Number of days to look back
- `check_points` (int): Number of time points to analyze

**Returns:**
- `Dict[str, Any]`: Trend evolution data with timeline and momentum changes

**Example:**
```python
evolution = trend_monitor.monitor_trend_evolution(
    "solid-state batteries",
    days_back=90,
    check_points=10
)

print(f"Trend: {evolution['trend_name']}")
print(f"Overall Direction: {evolution['direction']}")
print(f"Momentum Change: {evolution['momentum_change']}")

print("\nTimeline:")
for checkpoint in evolution['timeline']:
    print(f"  {checkpoint['date']}: {checkpoint['status']}")
```

### Trend Analysis

#### analyze_trend_momentum()

Analyze the momentum and growth of a trend.

```python
def analyze_trend_momentum(
    trend_name: str,
    context: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `trend_name` (str): Trend to analyze
- `context` (str, optional): Additional context for analysis

**Returns:**
- `Dict[str, Any]`: Momentum analysis with scores and indicators

**Example:**
```python
momentum = trend_monitor.analyze_trend_momentum(
    "EV charging infrastructure",
    context="North America"
)

print(f"Current Momentum: {momentum['current_momentum']:.2f}")
print(f"Growth Rate: {momentum['growth_rate']}")
print(f"Peak Indicators: {momentum['peak_indicators']}")
```

#### compare_trends()

Compare multiple trends across various metrics.

```python
def compare_trends(
    trend_names: List[str],
    comparison_metrics: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `trend_names` (List[str]): List of trends to compare
- `comparison_metrics` (List[str], optional): Specific metrics to compare

**Returns:**
- `Dict[str, Any]`: Comparative analysis of trends

**Example:**
```python
comparison = trend_monitor.compare_trends(
    trend_names=[
        "electric vehicles",
        "hydrogen fuel cells",
        "hybrid vehicles"
    ],
    comparison_metrics=["momentum", "growth_rate", "market_impact"]
)

print("Trend Comparison:")
for trend, metrics in comparison['trends'].items():
    print(f"{trend}: {metrics}")
```

### Multi-Domain Monitoring

#### monitor_multiple_domains()

Monitor trends across multiple domains simultaneously.

```python
def monitor_multiple_domains(
    domains: Dict[str, List[str]],
    time_window: str = "month"
) -> Dict[str, List[Dict[str, Any]]]
```

**Parameters:**
- `domains` (Dict[str, List[str]]): Dictionary of domain categories and their search terms
- `time_window` (str): Time window for monitoring

**Returns:**
- `Dict[str, List[Dict[str, Any]]]`: Trends organized by domain

**Example:**
```python
domains = {
    "technology": ["AI", "machine learning", "quantum computing"],
    "automotive": ["electric vehicles", "autonomous driving", "car sharing"],
    "energy": ["solar power", "battery storage", "grid modernization"]
}

domain_trends = trend_monitor.monitor_multiple_domains(
    domains=domains,
    time_window="quarter"
)

for domain, trends in domain_trends.items():
    print(f"\n{domain.upper()} Trends:")
    for trend in trends:
        print(f"  - {trend['name']} (momentum: {trend['momentum']:.2f})")
```

### Automated Monitoring

#### setup_trend_tracking()

Set up automated trend tracking with alerts.

```python
def setup_trend_tracking(
    trend_name: str,
    alert_threshold: float = 0.7,
    check_interval: str = "daily"
) -> str
```

**Parameters:**
- `trend_name` (str): Trend to track
- `alert_threshold` (float): Momentum threshold for alerts
- `check_interval` (str): How often to check ("daily", "weekly")

**Returns:**
- `str`: Tracking ID

**Example:**
```python
tracking_id = trend_monitor.setup_trend_tracking(
    "solid-state battery adoption",
    alert_threshold=0.8,
    check_interval="weekly"
)

print(f"Tracking ID: {tracking_id}")
```

## Complete Workflow Examples

### Basic Trend Detection

```python
from perplSDK.research.trend_monitor import TrendMonitor

# Initialize
trend_monitor = TrendMonitor()

# Detect emerging trends
trends = trend_monitor.detect_emerging_trends(
    search_domains=["electric vehicles", "battery technology"],
    time_window="month",
    min_momentum=0.5
)

# Display results
print("Emerging Trends:")
for i, trend in enumerate(trends, 1):
    print(f"\n{i}. {trend['name']}")
    print(f"   Momentum: {trend['momentum']:.2f}")
    print(f"   Description: {trend['description']}")
    print(f"   Sources: {len(trend['sources'])}")
```

### Tracking Trend Evolution

```python
# Monitor a specific trend over time
evolution = trend_monitor.monitor_trend_evolution(
    "fast charging technology",
    days_back=180,
    check_points=12
)

# Analyze the evolution
print(f"Trend: {evolution['trend_name']}")
print(f"Direction: {evolution['direction']}")
print(f"Momentum Change: {evolution['momentum_change']}")

if evolution['direction'] == "increasing":
    print("✓ This trend is gaining momentum")
elif evolution['direction'] == "decreasing":
    print("⚠ This trend is losing momentum")
else:
    print("→ This trend is stable")

# Plot timeline
print("\nEvolution Timeline:")
for point in evolution['timeline']:
    bars = "█" * int(point['momentum'] * 10)
    print(f"{point['date']}: {bars} {point['momentum']:.2f}")
```

### Comparative Trend Analysis

```python
# Compare multiple technologies
technologies = [
    "lithium-ion batteries",
    "solid-state batteries",
    "hydrogen fuel cells"
]

comparison = trend_monitor.compare_trends(
    trend_names=technologies,
    comparison_metrics=["momentum", "market_impact", "innovation_rate"]
)

# Display comparison
print("Technology Comparison:")
print("-" * 60)
for tech in technologies:
    metrics = comparison['trends'][tech]
    print(f"\n{tech}:")
    print(f"  Momentum: {metrics['momentum']:.2f}")
    print(f"  Market Impact: {metrics['market_impact']}")
    print(f"  Innovation Rate: {metrics['innovation_rate']}")

# Identify leader
leader = comparison['leader']
print(f"\nCurrent Leader: {leader}")
```

### Multi-Domain Monitoring

```python
# Set up comprehensive domain monitoring
domains = {
    "EV Technology": [
        "battery technology",
        "electric motors",
        "power electronics"
    ],
    "Infrastructure": [
        "charging stations",
        "grid integration",
        "smart charging"
    ],
    "Market": [
        "EV adoption",
        "consumer preferences",
        "pricing trends"
    ]
}

results = trend_monitor.monitor_multiple_domains(
    domains=domains,
    time_window="quarter"
)

# Create summary report
for domain, trends in results.items():
    print(f"\n{'='*60}")
    print(f"{domain}")
    print('='*60)
    
    if trends:
        for trend in sorted(trends, key=lambda x: x['momentum'], reverse=True)[:5]:
            print(f"  {trend['name']}: {trend['momentum']:.2f}")
    else:
        print("  No significant trends detected")
```

### Automated Trend Alerts

```python
# Set up tracking for key trends
key_trends = [
    "solid-state battery commercialization",
    "400kW fast charging deployment",
    "vehicle-to-grid technology"
]

tracking_ids = []
for trend in key_trends:
    tracking_id = trend_monitor.setup_trend_tracking(
        trend,
        alert_threshold=0.75,
        check_interval="weekly"
    )
    tracking_ids.append((trend, tracking_id))
    print(f"Now tracking: {trend} (ID: {tracking_id})")
```

## Advanced Features

### Custom Momentum Calculation

```python
# Analyze trend momentum with custom context
momentum = trend_monitor.analyze_trend_momentum(
    "bidirectional charging",
    context="residential market"
)

print(f"Momentum Score: {momentum['current_momentum']:.2f}")
print(f"Growth Indicators:")
for indicator in momentum['growth_indicators']:
    print(f"  - {indicator}")
```

### Historical Trend Comparison

```python
# Compare current trends with historical data
current_trends = trend_monitor.detect_emerging_trends(
    search_domains=["electric vehicles"],
    time_window="month"
)

# Compare with 6 months ago
historical_evolution = trend_monitor.monitor_trend_evolution(
    "electric vehicles",
    days_back=180,
    check_points=6
)

print("Current vs Historical:")
print(f"Current Momentum: {current_trends[0]['momentum']:.2f}")
print(f"6-Month Change: {historical_evolution['momentum_change']}")
```

### Trend Filtering and Ranking

```python
# Detect trends with custom filtering
all_trends = trend_monitor.detect_emerging_trends(
    search_domains=["automotive technology"],
    time_window="quarter",
    min_momentum=0.3,  # Lower threshold to capture more
    max_trends=50
)

# Filter high-momentum trends
high_momentum = [t for t in all_trends if t['momentum'] > 0.7]

# Sort by various metrics
by_momentum = sorted(all_trends, key=lambda x: x['momentum'], reverse=True)
by_relevance = sorted(all_trends, key=lambda x: x['relevance_score'], reverse=True)

print(f"High-Momentum Trends: {len(high_momentum)}")
print(f"Top Trend: {by_momentum[0]['name']}")
```

## Integration with Other Modules

### With Market Intelligence

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

market_intel = MarketIntelligence()
trend_monitor = TrendMonitor()

# Detect trends
trends = trend_monitor.detect_emerging_trends(
    search_domains=["electric vehicles"],
    time_window="quarter"
)

# Analyze top trend in detail
top_trend = trends[0]
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    custom_queries=[f"Deep analysis of {top_trend['name']}"]
)
```

### With Research Automation

```python
from perplSDK.research.automation import ResearchAutomation

research = ResearchAutomation()
trend_monitor = TrendMonitor()

# Detect trends
trends = trend_monitor.detect_emerging_trends(
    search_domains=["battery technology"],
    time_window="month"
)

# Create research project for top trends
project = research.create_project("Trend Deep Dive")
for trend in trends[:5]:
    project.add_query(f"Comprehensive analysis of {trend['name']}")
    project.add_query(f"Market implications of {trend['name']}")

research.conduct_research(project.name)
```

### With Scheduled Reports

```python
from perplSDK.reports.scheduler import ReportScheduler

scheduler = ReportScheduler()

# Schedule weekly trend reports
report_id = scheduler.schedule_report(
    name="Weekly Trend Monitor",
    report_type="trend_analysis",
    frequency="weekly",
    config={
        "domains": ["electric vehicles", "battery technology"],
        "time_window": "week",
        "min_momentum": 0.6
    }
)
```

## Best Practices

### 1. Choose Appropriate Time Windows

```python
# Short-term trends
daily_trends = trend_monitor.detect_emerging_trends(
    search_domains=["EV news"],
    time_window="day"
)

# Long-term trends
yearly_trends = trend_monitor.detect_emerging_trends(
    search_domains=["automotive industry"],
    time_window="year"
)
```

### 2. Set Meaningful Momentum Thresholds

```python
# High-confidence trends only
high_confidence = trend_monitor.detect_emerging_trends(
    search_domains=["technology"],
    min_momentum=0.8
)

# Capture all potential trends
all_potential = trend_monitor.detect_emerging_trends(
    search_domains=["technology"],
    min_momentum=0.3
)
```

### 3. Regular Monitoring

```python
# Set up periodic checks
import schedule
import time

def check_trends():
    trends = trend_monitor.detect_emerging_trends(
        search_domains=["electric vehicles"],
        time_window="week"
    )
    print(f"Found {len(trends)} trends")

schedule.every().monday.at("09:00").do(check_trends)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

## See Also

- [Market Intelligence](market_intelligence.md)
- [Research Automation](research.md)
- [Report Scheduling](reports.md)
- [Automated Workflows Guide](../guides/automation.md)
