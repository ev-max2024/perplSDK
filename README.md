# perplSDK

A comprehensive Python SDK for automating AI-powered research, market intelligence, and reporting using the Perplexity API. Designed specifically for organizations like EV MAX INC to streamline research workflows, monitor market trends, and generate actionable insights.

## 🚀 Features

### Core Capabilities
- **Perplexity API Integration**: Seamless async/sync client with rate limiting and error handling
- **Research Automation**: Project-based research with parallel query execution
- **Market Intelligence**: EV industry-focused market analysis with insights extraction
- **COPILOT - Super Fast Performance Intelligence**: Advanced performance analysis across multiple contexts
- **Trend Monitoring**: Emerging trend detection and evolution tracking
- **Report Scheduling**: Automated report generation and scheduling system
- **Markdown Formatting**: Professional report formatting for research outputs
- **GitHub Integration**: Automated publishing to repositories with PR support

### EV MAX INC Specific Features
- Pre-configured EV industry research templates
- Market intelligence for electric vehicles, batteries, and charging infrastructure
- Super fast performance intelligence for EV and manufacturing optimization
- Automated competitive analysis and strategic recommendations
- Workflow improvement automation for manufacturing and operations
- Continuous monitoring of technology and policy developments

## 📦 Installation

```bash
pip install perplSDK
```

Or install from source:

```bash
git clone https://github.com/ev-max2024/perplSDK.git
cd perplSDK
pip install -e .
```

## 🛠️ Quick Start

### 1. Configuration

Set up your environment variables:

```bash
export PERPLEXITY_API_KEY="your-perplexity-api-key"
export GITHUB_TOKEN="your-github-token"  # Optional
export GITHUB_REPO="owner/repo-name"     # Optional
```

Or create a `.env` file (see `.env.example`).

### 2. Basic Usage

```python
from perplSDK import PerplexityClient, ResearchAutomation

# Simple search
client = PerplexityClient()
result = client.search("Latest EV battery technology developments")
print(result.content)

# Research automation
research = ResearchAutomation()
project = research.create_project("EV Market Analysis", "Q4 2024 analysis")
project.add_query("Current EV market share by manufacturer")
project.add_query("EV charging infrastructure growth trends")

# Execute research
research.conduct_research(project.name, parallel=True)
```

### 3. Market Intelligence

```python
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector

market_intel = MarketIntelligence()

# Comprehensive EV market analysis
analysis = market_intel.conduct_market_analysis(
    sector=MarketSector.ELECTRIC_VEHICLES,
    analysis_type="comprehensive",
    geographic_focus="north_america"
)

# Get EV MAX specific insights
ev_max_insights = market_intel.get_ev_max_insights()
print(f"Recommendations: {ev_max_insights['recommendations']}")
```

### 4. COPILOT - Super Fast Performance Intelligence

```python
from perplSDK.research.market_intelligence import MarketIntelligence

market_intel = MarketIntelligence()

# Conduct performance intelligence analysis
performance_analysis = market_intel.conduct_performance_intelligence(
    context="ev",  # or "general", "manufacturing", "operations"
    time_frame="current",
    geographic_focus="north_america"
)

# Access insights and metrics
metrics = performance_analysis['performance_metrics']
print(f"Super Fast Insights: {metrics['super_fast_count']}")
print(f"High Impact: {metrics['high_impact_count']}")

# Get recommendations
for rec in performance_analysis['recommendations']:
    print(f"- {rec}")
```

## 📊 Command Line Interface

perplSDK includes a powerful CLI:

```bash
# Simple search
perpl-research search "EV market trends 2024"

# Research automation
perpl-research research "EV Analysis" --topic "electric vehicles" --output ev_report

# Market intelligence
perpl-research market electric_vehicles --analysis-type trends --output market_report

# COPILOT - Super Fast Performance Intelligence
perpl-research copilot --context ev --output performance_report
perpl-research copilot --context manufacturing --geographic-focus "north america"
perpl-research copilot --context operations --queries "workflow optimization" "process efficiency"

# Data export - convert data to various formats
perpl-research export formats  # List available formats
perpl-research export file data.json --format excel --output report
perpl-research export file data.json --format pdf --output report --title "Market Analysis"
perpl-research export file data.csv --format docx --output document

# Trend monitoring
perpl-research trends detect "electric vehicles" "battery technology"

# Schedule automated reports
perpl-research schedule add "Daily EV Trends" trend_analysis daily --topic "electric vehicles"

# GitHub integration
perpl-research github publish report.md reports/latest.md --message "Latest analysis"
```

## 📁 Data Export

Export research data and reports to multiple formats:

```python
from perplSDK import DataExporter

exporter = DataExporter(output_dir="./exports")

# Export to Excel
excel_path = exporter.export_to_excel(data, "report", sheet_name="Insights")

# Export to PDF
pdf_path = exporter.export_to_pdf(data, "report", title="Market Intelligence Report")

# Export to Word (DOCX)
docx_path = exporter.export_to_docx(data, "report", title="Research Document")

# Export to CSV (for CRM integration)
csv_path = exporter.export_to_csv(data, "report")

# Export to JSON
json_path = exporter.export_to_json(data, "report")

# Export research results directly
exporter.export_research_results(results, "excel", "research_output")

# Check available formats
available = DataExporter.get_available_formats()
```

### Supported Export Formats

- **Excel (.xlsx)** - Professional spreadsheets with formatting and metadata
- **PDF** - Formatted reports with tables and styling
- **Word (.docx)** - Editable documents with tables
- **CSV** - Simple format for CRM and data integration
- **JSON** - Structured data with optional metadata

## 🚀 COPILOT - Super Fast Performance Intelligence

The COPILOT feature provides super fast performance intelligence analysis across different contexts:

```bash
# General performance intelligence
perpl-research copilot --context general --output performance_intel

# EV-specific performance analysis
perpl-research copilot --context ev --time-frame current

# Manufacturing performance optimization
perpl-research copilot --context manufacturing --geographic-focus "global"

# Operations performance insights
perpl-research copilot --context operations --output ops_performance
```

### Performance Intelligence Contexts

- **general**: High-performance technology innovations and optimization techniques
- **ev**: Electric vehicle performance, acceleration, and fast charging
- **manufacturing**: Production speed, efficiency, and automation performance
- **operations**: Business process performance and workflow optimization

## 🔄 Automated Workflows

### Scheduled Reports

```python
from perplSDK import ReportScheduler

scheduler = ReportScheduler()

# Schedule weekly market intelligence
report_id = scheduler.schedule_report(
    name="Weekly EV Market Intelligence",
    report_type="market_intelligence",
    frequency="weekly",
    config={
        "sector": "electric_vehicles",
        "analysis_type": "comprehensive"
    },
    publish_to_github=True
)

scheduler.start_scheduler()
```

### Trend Monitoring

```python
from perplSDK.research.trend_monitor import TrendMonitor

trend_monitor = TrendMonitor()

# Detect emerging trends
trends = trend_monitor.detect_emerging_trends(
    search_domains=["electric vehicles", "battery technology"],
    time_window="month"
)

# Monitor trend evolution
evolution = trend_monitor.monitor_trend_evolution(
    "solid-state batteries",
    days_back=30
)
```

## 📝 Report Generation

```python
from perplSDK.reports.formatter import MarkdownFormatter

formatter = MarkdownFormatter()

# Format research report
report = formatter.format_research_report(
    project_name="EV Analysis",
    results=research_results,
    metadata={"analysis_type": "Market Research"}
)

# Save report
report_path = formatter.save_report(report, "ev_analysis_2024")
```

## 🚀 GitHub Integration

```python
from perplSDK.github_integration.publisher import GitHubPublisher

github = GitHubPublisher()

# Publish report
result = github.publish_file(
    local_file_path="./reports/analysis.md",
    github_file_path="reports/latest_analysis.md",
    commit_message="Latest market analysis"
)

# Set up automated reporting workflow
github.setup_automated_reporting()
```

## 🏭 EV MAX INC Examples

### Market Intelligence Automation

```python
# Run the comprehensive market intelligence script
python examples/ev_max_market_intelligence.py
```

### Workflow Improvement Analysis

```python
# Analyze and improve operational workflows
python examples/automated_workflow_improvement.py
```

### Complete Feature Demo

```python
# Demonstrate all SDK capabilities
python examples/comprehensive_demo.py
```

## 📚 Documentation

### API Reference
- [PerplexityClient API](docs/api/client.md)
- [Research Automation](docs/api/research.md)
- [Market Intelligence](docs/api/market_intelligence.md)
- [Trend Monitoring](docs/api/trend_monitoring.md)
- [Report Generation](docs/api/reports.md)
- [GitHub Integration](docs/api/github.md)

### Guides
- [Configuration Guide](docs/guides/configuration.md)
- [EV Industry Research](docs/guides/ev_research.md)
- [Automated Workflows](docs/guides/automation.md)
- [Custom Templates](docs/guides/templates.md)

## 🏗️ Architecture

```
perplSDK/
├── core/                    # Core API client and configuration
├── research/               # Research automation modules
│   ├── automation.py       # Project-based research automation
│   ├── market_intelligence.py  # Market analysis and insights
│   └── trend_monitor.py    # Trend detection and monitoring
├── reports/                # Report generation and scheduling
│   ├── formatter.py        # Markdown report formatting
│   └── scheduler.py        # Automated report scheduling
├── github_integration/     # GitHub publishing and automation
├── utils/                  # Utility functions and templates
├── cli.py                  # Command-line interface
└── examples/              # Example scripts and demos
```

## 🔧 Development

### Setup Development Environment

```bash
git clone https://github.com/ev-max2024/perplSDK.git
cd perplSDK
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```

### Code Quality

```bash
black perplSDK/
flake8 perplSDK/
mypy perplSDK/
```

## 📋 Requirements

- Python 3.8+
- Perplexity API key
- Optional: GitHub token for integration features

### Dependencies

- `requests>=2.31.0` - HTTP client
- `aiohttp>=3.8.0` - Async HTTP client
- `schedule>=1.2.0` - Job scheduling
- `PyGithub>=1.59.0` - GitHub API client
- `python-dotenv>=1.0.0` - Environment configuration
- `pydantic>=2.0.0` - Data validation
- `markdown>=3.5.0` - Markdown processing
- `jinja2>=3.1.0` - Template engine
- `pyyaml>=6.0.0` - YAML configuration

### Optional Export Dependencies

Install with `pip install perplSDK[export]`:

- `openpyxl>=3.1.2` - Excel export
- `python-docx>=1.1.0` - Word/DOCX export
- `reportlab>=4.1.0` - PDF export

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/ev-max2024/perplSDK/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ev-max2024/perplSDK/discussions)
- **Email**: dev@evmax.com

## 🎯 Roadmap

- [ ] Enhanced NLP processing for insight extraction
- [ ] Integration with additional AI research APIs
- [ ] Real-time dashboard for trend monitoring
- [ ] Advanced competitive intelligence features
- [ ] Machine learning-powered trend prediction
- [ ] Multi-language support for global research

---

**Built for EV MAX INC and the future of electric mobility research automation.**
