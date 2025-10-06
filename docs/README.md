# perplSDK Documentation

Welcome to the comprehensive documentation for perplSDK - the Python SDK for AI-powered research, market intelligence, and automated reporting.

## 📚 Documentation Structure

### API Reference

Complete API documentation for all SDK modules:

- **[PerplexityClient API](api/client.md)** - Core API client for Perplexity integration
  - Search operations (sync/async)
  - Rate limiting and error handling
  - Batch operations
  - Configuration options

- **[Research Automation](api/research.md)** - Project-based research management
  - Research projects and queries
  - Parallel execution
  - Result aggregation
  - Research plan generation

- **[Market Intelligence](api/market_intelligence.md)** - Market analysis and insights
  - Market analysis by sector
  - COPILOT - Performance Intelligence
  - EV-specific insights
  - Competitive intelligence

- **[Trend Monitoring](api/trend_monitoring.md)** - Trend detection and tracking
  - Emerging trend detection
  - Trend evolution monitoring
  - Multi-domain analysis
  - Automated alerts

- **[Report Generation](api/reports.md)** - Professional report formatting
  - Markdown/HTML formatting
  - Report templates
  - Scheduled reports
  - GitHub integration

- **[GitHub Integration](api/github.md)** - Repository automation
  - File publishing
  - Pull request workflows
  - Automated workflows
  - CI/CD integration

### Guides

Comprehensive guides for common use cases:

- **[Configuration Guide](guides/configuration.md)** - Setup and configuration
  - Environment variables
  - Configuration files
  - Security best practices
  - Multi-environment setup

- **[EV Industry Research](guides/ev_research.md)** - Electric vehicle research
  - EV market analysis
  - Battery technology research
  - Charging infrastructure analysis
  - EV MAX INC workflows

- **[Automated Workflows](guides/automation.md)** - Automation and scheduling
  - Scheduled reports
  - Continuous monitoring
  - CI/CD integration
  - Event-driven workflows

- **[Custom Templates](guides/templates.md)** - Research and report templates
  - Query templates
  - Report templates
  - Industry-specific templates
  - Template customization

- **[Privacy and Security](guides/privacy_and_security.md)** - Security best practices
  - API key management
  - Data privacy
  - Access control
  - Compliance (GDPR, SOC 2)

- **[User Access and Settings](guides/user_access.md)** - User management
  - User roles and permissions
  - Team access
  - User settings
  - Multi-user workflows

### Special Topics

- **[COPILOT Guide](COPILOT_GUIDE.md)** - Super Fast Performance Intelligence

## 🚀 Quick Start

### Installation

```bash
pip install perplSDK
```

### Basic Configuration

```bash
export PERPLEXITY_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"  # Optional
```

See the [Configuration Guide](guides/configuration.md) for detailed setup.

### First Research Project

```python
from perplSDK import PerplexityClient, ResearchAutomation

# Simple search
client = PerplexityClient()
result = client.search("Latest EV battery technology")
print(result.content)

# Research automation
research = ResearchAutomation()
project = research.create_project("EV Analysis")
project.add_query("Current EV market trends")
project = research.conduct_research(project.name)
```

See [Research Automation API](api/research.md) for more examples.

## 📖 Documentation by Use Case

### For Researchers

Start here to conduct AI-powered research:

1. [PerplexityClient API](api/client.md) - Basic search operations
2. [Research Automation](api/research.md) - Project-based research
3. [Custom Templates](guides/templates.md) - Reusable query patterns
4. [Report Generation](api/reports.md) - Formatting results

### For Market Analysts

Focus on market intelligence and analysis:

1. [Market Intelligence API](api/market_intelligence.md) - Market analysis
2. [Trend Monitoring](api/trend_monitoring.md) - Trend tracking
3. [EV Industry Research](guides/ev_research.md) - EV-specific workflows
4. [Report Generation](api/reports.md) - Professional reports

### For Engineering Teams

Set up automated research workflows:

1. [Configuration Guide](guides/configuration.md) - Setup and deployment
2. [Automated Workflows](guides/automation.md) - Scheduling and automation
3. [GitHub Integration](api/github.md) - CI/CD integration
4. [Privacy and Security](guides/privacy_and_security.md) - Security practices

### For Administrators

Manage access and security:

1. [User Access and Settings](guides/user_access.md) - User management
2. [Privacy and Security](guides/privacy_and_security.md) - Security setup
3. [Configuration Guide](guides/configuration.md) - System configuration

## 🔍 Finding What You Need

### By Topic

- **Getting Started**: [Configuration Guide](guides/configuration.md)
- **API Keys**: [Configuration Guide](guides/configuration.md#api-key-management)
- **Search Operations**: [PerplexityClient API](api/client.md)
- **Market Analysis**: [Market Intelligence API](api/market_intelligence.md)
- **Performance Intelligence**: [Market Intelligence API](api/market_intelligence.md#performance-intelligence-copilot)
- **Trend Detection**: [Trend Monitoring API](api/trend_monitoring.md)
- **Report Formatting**: [Report Generation API](api/reports.md)
- **Automation**: [Automated Workflows Guide](guides/automation.md)
- **Security**: [Privacy and Security Guide](guides/privacy_and_security.md)
- **EV Research**: [EV Industry Research Guide](guides/ev_research.md)

### By Feature

- **COPILOT**: [Market Intelligence API](api/market_intelligence.md#performance-intelligence-copilot) | [COPILOT Guide](COPILOT_GUIDE.md)
- **GitHub Publishing**: [GitHub Integration API](api/github.md)
- **Scheduled Reports**: [Automated Workflows](guides/automation.md) | [Report Generation](api/reports.md)
- **Templates**: [Custom Templates Guide](guides/templates.md)
- **Multi-User**: [User Access Guide](guides/user_access.md)

## 📊 Code Examples

Each documentation page includes comprehensive examples:

- **Basic Usage**: Simple, getting-started examples
- **Advanced Usage**: Complex workflows and patterns
- **Best Practices**: Recommended approaches
- **Integration Examples**: Combining multiple features

## 🆘 Getting Help

### Documentation Issues

Found an error or unclear documentation? Please:
1. Check the [GitHub Issues](https://github.com/ev-max2024/perplSDK/issues)
2. Open a new issue with the "documentation" label
3. Suggest improvements via pull request

### Support Channels

- **GitHub Issues**: [ev-max2024/perplSDK/issues](https://github.com/ev-max2024/perplSDK/issues)
- **GitHub Discussions**: [ev-max2024/perplSDK/discussions](https://github.com/ev-max2024/perplSDK/discussions)
- **Email**: dev@evmax.com

## 📝 Documentation Statistics

- **Total Documentation Files**: 13
- **API Reference Pages**: 6
- **Guide Pages**: 6
- **Total Documentation Lines**: 7,500+
- **Code Examples**: 100+

## 🔄 Documentation Updates

This documentation is continuously updated. Last major update: December 2024

### Recent Additions

- Complete API reference for all modules
- Comprehensive guides for common workflows
- Security and privacy documentation
- User access and permissions guide
- EV industry-specific research guide
- Automated workflows and scheduling guide
- Custom templates guide

## 📄 License

This documentation is part of perplSDK, licensed under the MIT License.

---

**Built with ❤️ for EV MAX INC and the future of AI-powered research automation.**
