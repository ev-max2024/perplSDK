# perplSDK - AI Coding Agent Instructions

This file provides essential knowledge for AI coding agents to be productive when working with the perplSDK codebase.

## Repository Overview

**perplSDK** is a comprehensive Python SDK for automating AI-powered research, market intelligence, and reporting using the Perplexity API. It's specifically designed for EV MAX INC to streamline research workflows, monitor market trends, and generate actionable insights.

### Key Features
- Perplexity API integration with rate limiting and error handling
- Research automation with parallel query execution
- Market intelligence focused on EV industry
- COPILOT - Super Fast Performance Intelligence
- Trend monitoring and detection
- Report scheduling and generation
- GitHub integration for automated publishing

## Project Architecture

```
perplSDK/
├── perplSDK/                    # Main package
│   ├── core/                    # Core functionality
│   │   ├── client.py            # Perplexity API client (sync/async)
│   │   ├── config.py            # Configuration management
│   │   └── exceptions.py        # Custom exceptions
│   ├── research/                # Research automation
│   │   ├── automation.py        # Project-based research
│   │   ├── market_intelligence.py  # Market analysis
│   │   └── trend_monitor.py     # Trend detection
│   ├── reports/                 # Report generation
│   │   ├── formatter.py         # Markdown formatting
│   │   └── scheduler.py         # Report scheduling
│   ├── github_integration/      # GitHub automation
│   │   └── publisher.py         # File publishing
│   ├── utils/                   # Utilities
│   │   ├── templates.py         # Research templates
│   │   └── formatters.py        # Formatting utilities
│   └── cli.py                   # Command-line interface
├── tests/                       # Test suite
├── docs/                        # Documentation
├── examples/                    # Example scripts
├── setup.py                     # Package setup
└── requirements.txt             # Dependencies
```

## Development Setup

### Prerequisites
- Python 3.8+
- Perplexity API key
- Optional: GitHub token for integration features

### Installation
```bash
# Clone repository
git clone https://github.com/ev-max2024/perplSDK.git
cd perplSDK

# Install in development mode
pip install -e ".[dev]"
```

### Configuration
Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Or use `config.yaml` from `config.yaml.example`.

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
black perplSDK/      # Format code
flake8 perplSDK/     # Lint code
mypy perplSDK/       # Type checking
```

## Code Organization and Conventions

### Module Responsibilities

#### Core Module (`perplSDK/core/`)
- **client.py**: Perplexity API client with rate limiting, retry logic, sync/async support
  - `PerplexityClient`: Main client class
  - `SearchResult`: Pydantic model for API responses
  - Rate limiting enforced per `api_rate_limit` config
  
- **config.py**: Configuration management using Pydantic
  - `Config`: Configuration model with validation
  - Loads from environment variables or YAML files
  - Required fields: `perplexity_api_key`
  
- **exceptions.py**: Custom exception classes
  - `APIError`, `AuthenticationError`, `RateLimitError`, `ConfigurationError`

#### Research Module (`perplSDK/research/`)
- **automation.py**: Project-based research automation
  - `ResearchProject`: Project container for queries and results
  - `ResearchAutomation`: Main automation class
  - Supports parallel query execution
  
- **market_intelligence.py**: Market analysis and insights
  - `MarketIntelligence`: Comprehensive market analysis
  - `MarketSector`: Enum of supported sectors (ELECTRIC_VEHICLES, etc.)
  - `conduct_performance_intelligence()`: COPILOT performance analysis
  - EV MAX INC specific focus areas pre-configured
  
- **trend_monitor.py**: Trend detection and monitoring
  - `TrendMonitor`: Emerging trend detection
  - `detect_emerging_trends()`: Multi-domain trend analysis
  - `monitor_trend_evolution()`: Track trend changes over time

#### Reports Module (`perplSDK/reports/`)
- **formatter.py**: Professional report formatting
  - `MarkdownFormatter`: Markdown report generation
  - Templates for different report types
  
- **scheduler.py**: Automated report scheduling
  - `ReportScheduler`: Schedule periodic reports
  - Supports daily, weekly, monthly schedules
  - Optional GitHub publishing integration

#### GitHub Integration (`perplSDK/github_integration/`)
- **publisher.py**: GitHub automation
  - `GitHubPublisher`: Publish files to repositories
  - PR creation and management
  - Requires `github_token` and `github_repo` configuration

### Coding Conventions

#### Style Guidelines
- **Formatting**: Use Black for code formatting (line length: 88)
- **Linting**: Follow Flake8 rules
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Use Google-style docstrings for all public functions/classes

Example:
```python
def function_name(param1: str, param2: int) -> Dict[str, Any]:
    """Brief description.
    
    Detailed description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

#### Error Handling
- Use custom exceptions from `core.exceptions`
- Always handle rate limit errors gracefully
- Retry logic with exponential backoff for API calls

#### Configuration
- Use `Config.from_env()` to load configuration
- Always validate required fields with `config.validate_required_fields()`
- Support both environment variables and YAML configuration

#### Async/Sync Pattern
- Core client supports both sync and async operations
- Use `async def` for async methods, suffix with `_async` if needed
- Async operations for batch processing and parallel queries

### Testing Patterns

#### Test Structure
- Tests located in `tests/` directory
- Use pytest as test framework
- Mock external API calls using `unittest.mock`

Example test structure:
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_config():
    """Create mock configuration."""
    return Config(perplexity_api_key="test-key")

def test_feature(mock_config):
    """Test specific feature."""
    # Arrange
    client = PerplexityClient(mock_config)
    
    # Act
    result = client.method()
    
    # Assert
    assert result is not None
```

#### Mocking API Calls
Always mock Perplexity API calls in tests:
```python
@patch('requests.Session.post')
def test_search(mock_post, client):
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "test"}}]
    }
    result = client.search("query")
    assert result.content == "test"
```

## Common Development Tasks

### Adding a New Research Query Type

1. Update `perplSDK/research/automation.py`:
```python
def add_query(self, query: str, category: str = "general", **kwargs):
    self.queries.append({
        "query": query,
        "category": category,
        "kwargs": kwargs
    })
```

2. Add corresponding template in `perplSDK/utils/templates.py`

3. Add tests in `tests/test_research_automation.py`

### Adding a New Market Sector

1. Update `MarketSector` enum in `perplSDK/research/market_intelligence.py`:
```python
class MarketSector(Enum):
    NEW_SECTOR = "new_sector"
```

2. Update query generation logic in `generate_market_queries()`

3. Add sector-specific templates

### Adding CLI Commands

1. Add command function in `perplSDK/cli.py`:
```python
def cmd_new_feature(args):
    """Execute new feature command."""
    # Implementation
    return 0
```

2. Register in argument parser:
```python
parser_new = subparsers.add_parser('new-feature', help='Description')
parser_new.add_argument('--param', type=str, help='Parameter')
parser_new.set_defaults(func=cmd_new_feature)
```

3. Test manually:
```bash
perpl-research new-feature --param value
```

### Creating Custom Report Templates

1. Add template in `perplSDK/utils/templates.py`
2. Use Jinja2 templating syntax
3. Register in `MarkdownFormatter` class

### Extending GitHub Integration

1. Update `GitHubPublisher` in `perplSDK/github_integration/publisher.py`
2. Use PyGithub library for GitHub API interactions
3. Handle authentication with `github_token` from config

## Configuration Management

### Environment Variables
Primary configuration method. Key variables:
- `PERPLEXITY_API_KEY` (required): Perplexity API authentication
- `GITHUB_TOKEN` (optional): GitHub integration
- `GITHUB_REPO` (optional): Target repository (owner/repo)
- `API_RATE_LIMIT` (default: 60): Requests per minute
- `OUTPUT_DIR` (default: ./reports): Output directory
- `LOG_LEVEL` (default: INFO): Logging level

### YAML Configuration
Alternative to environment variables:
```yaml
perplexity_api_key: "your-key"
github_token: "your-token"
api_rate_limit: 60
```

Load with: `Config.from_yaml("config.yaml")`

### Validation
Always validate configuration:
```python
config = Config.from_env()
config.validate_required_fields()  # Raises ConfigurationError if missing
```

## API Integration Patterns

### Perplexity API Client Usage

#### Basic Search
```python
from perplSDK import PerplexityClient

client = PerplexityClient()
result = client.search(
    "query text",
    max_tokens=1024,
    temperature=0.7,
    recency_filter="month"
)
print(result.content)
client.close()  # Always close when done
```

#### Async Search
```python
async def async_search():
    client = PerplexityClient()
    result = await client.search_async("query")
    await client.close_async()
    return result
```

#### Batch Queries
```python
queries = ["query1", "query2", "query3"]
results = client.batch_search(queries, parallel=True)
```

### Rate Limiting
- Automatic rate limiting based on `api_rate_limit` config
- Implements sliding window algorithm
- Raises `RateLimitError` when limit exceeded
- Retry logic with exponential backoff

### Error Handling
```python
from perplSDK.core.exceptions import APIError, RateLimitError

try:
    result = client.search("query")
except RateLimitError:
    # Handle rate limit
    time.sleep(60)
except APIError as e:
    # Handle API error
    logger.error(f"API error: {e}")
```

## EV MAX INC Specific Features

### Market Intelligence Focus Areas
Pre-configured for EV industry:
- Electric vehicle market trends
- EV charging infrastructure development
- Battery technology innovations
- EV policy and regulations
- Competitive landscape analysis
- Consumer adoption patterns
- Market share analysis
- Sustainability trends

### COPILOT - Performance Intelligence
```python
from perplSDK.research.market_intelligence import MarketIntelligence

market_intel = MarketIntelligence()
performance = market_intel.conduct_performance_intelligence(
    context="ev",  # or "general", "manufacturing", "operations"
    time_frame="current",
    geographic_focus="north_america"
)
```

### Contexts
- **general**: High-performance technology innovations
- **ev**: Electric vehicle performance and fast charging
- **manufacturing**: Production speed and efficiency
- **operations**: Business process performance

## CLI Usage Patterns

### Common Commands
```bash
# Simple search
perpl-research search "query text"

# Research automation
perpl-research research "Project Name" --topic "electric vehicles" --output report.md

# Market intelligence
perpl-research market electric_vehicles --analysis-type comprehensive

# COPILOT performance intelligence
perpl-research copilot --context ev --output performance_report.md

# Trend monitoring
perpl-research trends detect "topic1" "topic2"

# Schedule reports
perpl-research schedule add "Report Name" trend_analysis daily --topic "EVs"

# GitHub publishing
perpl-research github publish local.md remote.md --message "Update"
```

### Command Structure
- All commands use `perpl-research` entry point
- Subcommands: search, research, market, copilot, trends, schedule, github
- Use `--help` for detailed options: `perpl-research [command] --help`

## Dependencies and Version Management

### Core Dependencies
- `requests>=2.31.0`: HTTP client for sync operations
- `aiohttp>=3.9.4`: Async HTTP client
- `schedule>=1.2.0`: Job scheduling
- `PyGithub>=1.59.0`: GitHub API client
- `python-dotenv>=1.0.0`: Environment configuration
- `pydantic>=2.5.0`: Data validation and settings
- `markdown>=3.5.0`: Markdown processing
- `jinja2>=3.1.0`: Template engine
- `pyyaml>=6.0.0`: YAML configuration

### Development Dependencies
- `pytest>=7.0.0`: Testing framework
- `pytest-asyncio>=0.21.0`: Async testing
- `black>=23.0.0`: Code formatting
- `flake8>=6.0.0`: Linting
- `mypy>=1.0.0`: Type checking

### Version Requirements
- Python 3.8+ required
- Compatible with Python 3.8, 3.9, 3.10, 3.11, 3.12

## Git Workflow

### Branch Naming
- Feature branches: `feature/description`
- Bug fixes: `fix/description`
- Documentation: `docs/description`
- CI/CD: `ci/description`
- Copilot tasks: `copilot/description`

### Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

### Pull Request Process
1. Create feature branch from `main`
2. Make changes with descriptive commits
3. Run tests: `pytest tests/`
4. Run code quality checks: `black`, `flake8`, `mypy`
5. Push and create PR
6. Address review feedback
7. Merge after approval

## Debugging and Troubleshooting

### Common Issues

#### API Authentication Errors
- Check `PERPLEXITY_API_KEY` is set correctly
- Verify API key is valid and active
- Check rate limits haven't been exceeded

#### Configuration Errors
- Ensure `.env` file exists or environment variables are set
- Run `config.validate_required_fields()` to check required fields
- Check file paths for `config.yaml` if using YAML config

#### Rate Limit Errors
- Default limit: 60 requests/minute
- Adjust `API_RATE_LIMIT` if needed
- Implement exponential backoff in retry logic

#### Import Errors
- Ensure package is installed: `pip install -e .`
- Check Python version (>=3.8 required)
- Verify all dependencies installed: `pip install -r requirements.txt`

### Logging
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or set `LOG_LEVEL=DEBUG` in environment variables.

### Debugging Tips
1. Check logs in `perplsdk.log` (if `LOG_FILE` configured)
2. Use `--verbose` flag with CLI commands
3. Test API key with simple search first
4. Verify network connectivity to Perplexity API
5. Check GitHub token permissions for integration features

## Examples and Templates

### Example Scripts
Located in `examples/` directory:
- `basic_validation.py`: Basic functionality validation
- `comprehensive_demo.py`: All features demonstration
- `ev_max_market_intelligence.py`: Market intelligence automation
- `copilot_performance_intelligence.py`: COPILOT performance analysis
- `automated_workflow_improvement.py`: Workflow automation

### Running Examples
```bash
# Ensure environment is configured
cp .env.example .env
# Edit .env with your credentials

# Run example
python examples/comprehensive_demo.py
```

## Security Considerations

### API Key Management
- Never commit API keys to version control
- Use `.env` files (excluded in `.gitignore`)
- Use environment variables in production
- Rotate keys regularly

### GitHub Token Permissions
- Use fine-grained tokens with minimal permissions
- Only grant repository write access if needed
- Store securely, never in code

### Data Privacy
- Research results may contain sensitive data
- Be cautious when publishing reports to public repositories
- Review output before automated GitHub publishing

## Performance Optimization

### Rate Limiting
- Default: 60 requests/minute
- Use batch operations for multiple queries
- Implement caching for repeated queries

### Async Operations
- Use async methods for I/O-bound operations
- Parallel query execution with `parallel=True`
- Batch processing for multiple research projects

### Memory Management
- Close clients when done: `client.close()`
- Stream large results instead of loading in memory
- Clean up temporary files in `OUTPUT_DIR`

## Best Practices

### Code Quality
1. Always use type hints
2. Write docstrings for public APIs
3. Add tests for new features
4. Run `black` before committing
5. Check with `flake8` and `mypy`

### API Usage
1. Always handle exceptions
2. Implement retry logic with backoff
3. Close clients properly
4. Monitor rate limits
5. Validate responses

### Configuration
1. Use `Config.from_env()` consistently
2. Validate configuration early
3. Provide sensible defaults
4. Document all configuration options

### Testing
1. Mock external API calls
2. Test error conditions
3. Use fixtures for common setups
4. Maintain >80% code coverage
5. Test both sync and async paths

### Documentation
1. Update README for user-facing changes
2. Update docstrings for API changes
3. Add examples for new features
4. Keep this file updated

## Additional Resources

### Documentation
- **API Reference**: `docs/api/`
- **Guides**: `docs/guides/`
- **README**: `README.md`
- **COPILOT Guide**: `docs/COPILOT_GUIDE.md`

### External Links
- **Perplexity API Docs**: https://docs.perplexity.ai
- **PyGithub Docs**: https://pygithub.readthedocs.io
- **Pydantic Docs**: https://docs.pydantic.dev

### Support
- **Issues**: https://github.com/ev-max2024/perplSDK/issues
- **Discussions**: https://github.com/ev-max2024/perplSDK/discussions
- **Email**: dev@evmax.com

---

**Last Updated**: 2025-10-30
**Version**: 0.1.0
**Maintained by**: EV MAX INC
