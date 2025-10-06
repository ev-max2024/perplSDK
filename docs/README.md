# perplSDK Documentation

Welcome to the perplSDK documentation! This comprehensive guide will help you get started with AI-powered research automation for the electric vehicle industry and beyond.

## 📚 Quick Navigation

### Getting Started
- [Main README](../README.md) - Overview and quick start
- [Configuration Guide](guides/configuration.md) - Setup and configuration
- [COPILOT Guide](COPILOT_GUIDE.md) - Super fast performance intelligence

### API Reference

Complete API documentation for all SDK components:

- **[PerplexityClient API](api/client.md)** - Core API client for search and queries
- **[Research Automation](api/research.md)** - Project-based research with parallel execution
- **[Market Intelligence](api/market_intelligence.md)** - Market analysis and COPILOT performance intelligence
- **[Trend Monitoring](api/trend_monitoring.md)** - Trend detection and evolution tracking
- **[Report Generation](api/reports.md)** - Markdown formatting and automated scheduling
- **[GitHub Integration](api/github.md)** - Automated publishing and repository management

### Guides

Step-by-step guides for common use cases:

- **[Configuration Guide](guides/configuration.md)** - Environment setup, config files, and best practices
- **[EV Industry Research](guides/ev_research.md)** - Electric vehicle market research workflows
- **[Automated Workflows](guides/automation.md)** - Scheduling, monitoring, and orchestration
- **[Custom Templates](guides/templates.md)** - Creating and using research templates

## 🎯 Use Case Examples

### Market Research
- **Comprehensive Market Analysis**: [Market Intelligence API](api/market_intelligence.md)
- **Competitive Analysis**: [EV Industry Research Guide](guides/ev_research.md#competitive-landscape)
- **Trend Detection**: [Trend Monitoring API](api/trend_monitoring.md)

### Automation
- **Scheduled Reports**: [Automated Workflows Guide](guides/automation.md#report-scheduling)
- **Continuous Monitoring**: [Automated Workflows Guide](guides/automation.md#continuous-monitoring)
- **GitHub Publishing**: [GitHub Integration API](api/github.md)

### Performance Intelligence
- **COPILOT Analysis**: [COPILOT Guide](COPILOT_GUIDE.md)
- **Performance Metrics**: [Market Intelligence API](api/market_intelligence.md#copilot---performance-intelligence)
- **Optimization Opportunities**: [EV Industry Research Guide](guides/ev_research.md#copilot-for-ev-performance-analysis)

## 🚀 Quick Start Examples

### Basic Search

```python
from perplSDK import PerplexityClient

client = PerplexityClient()
result = client.search("Latest EV battery technology")
print(result.content)
```

See: [PerplexityClient API](api/client.md)

### Research Project

```python
from perplSDK import ResearchAutomation

research = ResearchAutomation()
project = research.create_project("EV Analysis")
project.add_query("EV market trends")
project.add_query("Battery innovations")
research.conduct_research(project.name)
```

See: [Research Automation API](api/research.md)

### Market Intelligence

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

market_intel = MarketIntelligence()
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive"
)
```

See: [Market Intelligence API](api/market_intelligence.md)

### Scheduled Reports

```python
from perplSDK.reports.scheduler import ReportScheduler, ReportType, ReportFrequency

scheduler = ReportScheduler()
scheduler.schedule_report(
    name="Weekly EV Report",
    report_type=ReportType.MARKET_INTELLIGENCE,
    frequency=ReportFrequency.WEEKLY,
    config={"sector": "electric_vehicles"}
)
scheduler.start_scheduler()
```

See: [Automated Workflows Guide](guides/automation.md)

## 📖 Documentation Structure

```
docs/
├── README.md                    # This file
├── COPILOT_GUIDE.md            # COPILOT performance intelligence guide
├── api/                        # API Reference Documentation
│   ├── client.md               # PerplexityClient API
│   ├── research.md             # Research Automation API
│   ├── market_intelligence.md  # Market Intelligence API
│   ├── trend_monitoring.md     # Trend Monitoring API
│   ├── reports.md              # Report Generation API
│   └── github.md               # GitHub Integration API
└── guides/                     # User Guides
    ├── configuration.md        # Configuration and setup
    ├── ev_research.md          # EV industry research
    ├── automation.md           # Automated workflows
    └── templates.md            # Custom templates
```

## 🔍 Finding What You Need

### I want to...

**Get started quickly**
→ [Main README Quick Start](../README.md#quick-start)

**Configure the SDK**
→ [Configuration Guide](guides/configuration.md)

**Conduct EV market research**
→ [EV Industry Research Guide](guides/ev_research.md)

**Set up automated reports**
→ [Automated Workflows Guide](guides/automation.md)

**Analyze performance opportunities**
→ [COPILOT Guide](COPILOT_GUIDE.md)

**Publish reports to GitHub**
→ [GitHub Integration API](api/github.md)

**Monitor industry trends**
→ [Trend Monitoring API](api/trend_monitoring.md)

**Create custom research templates**
→ [Custom Templates Guide](guides/templates.md)

**Understand API methods**
→ [API Reference](api/) section

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/ev-max2024/perplSDK/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ev-max2024/perplSDK/discussions)
- **Email**: dev@evmax.com

## 📝 Contributing to Documentation

Found an error or want to improve the documentation? Contributions are welcome!

1. Fork the repository
2. Make your changes to the documentation
3. Submit a pull request

See the [Contributing Guide](../README.md#contributing) for more details.

## 🎓 Learning Path

### Beginner
1. Read [Main README](../README.md)
2. Follow [Configuration Guide](guides/configuration.md)
3. Try basic examples from [PerplexityClient API](api/client.md)

### Intermediate
1. Explore [Research Automation API](api/research.md)
2. Learn about [Market Intelligence](api/market_intelligence.md)
3. Try [EV Industry Research Guide](guides/ev_research.md) examples

### Advanced
1. Master [Automated Workflows](guides/automation.md)
2. Create [Custom Templates](guides/templates.md)
3. Implement [GitHub Integration](api/github.md)
4. Optimize with [COPILOT](COPILOT_GUIDE.md)

## 📊 API Coverage

| Component | API Docs | Guide |
|-----------|----------|-------|
| Core Client | [✓](api/client.md) | [Configuration](guides/configuration.md) |
| Research Automation | [✓](api/research.md) | [EV Research](guides/ev_research.md) |
| Market Intelligence | [✓](api/market_intelligence.md) | [EV Research](guides/ev_research.md) |
| Trend Monitoring | [✓](api/trend_monitoring.md) | [EV Research](guides/ev_research.md) |
| Report Generation | [✓](api/reports.md) | [Automation](guides/automation.md) |
| GitHub Integration | [✓](api/github.md) | [Automation](guides/automation.md) |
| COPILOT | [✓](COPILOT_GUIDE.md) | [EV Research](guides/ev_research.md#copilot-for-ev-performance-analysis) |
| Templates | - | [✓](guides/templates.md) |

## 🔄 Documentation Updates

This documentation is maintained alongside the codebase. Last updated: 2024

For the latest version, visit the [GitHub repository](https://github.com/ev-max2024/perplSDK).

---

**Built for EV MAX INC and high-performance organizations worldwide.**
