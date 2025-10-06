# Configuration Guide

This guide covers all configuration options for perplSDK, including environment variables, configuration files, and programmatic configuration.

## Quick Start

### Environment Variables

The simplest way to configure perplSDK is using environment variables:

```bash
export PERPLEXITY_API_KEY="your-perplexity-api-key"
export GITHUB_TOKEN="your-github-token"          # Optional
export GITHUB_REPO="owner/repo-name"             # Optional
export GITHUB_BRANCH="main"                      # Optional
export OUTPUT_DIR="./reports"                    # Optional
export API_RATE_LIMIT="60"                       # Optional
export LOG_LEVEL="INFO"                          # Optional
```

### .env File

Create a `.env` file in your project root:

```bash
# Required
PERPLEXITY_API_KEY=your-perplexity-api-key

# Optional - GitHub Integration
GITHUB_TOKEN=your-github-token
GITHUB_REPO=owner/repo-name
GITHUB_BRANCH=main

# Optional - Reports
OUTPUT_DIR=./reports

# Optional - API Settings
API_RATE_LIMIT=60

# Optional - Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/perplsdk.log
```

### Configuration File

Create a `config.yaml` file:

```yaml
# Required
perplexity_api_key: your-perplexity-api-key

# Optional - GitHub Integration
github_token: your-github-token
github_repo: owner/repo-name
github_branch: main

# Optional - Reports
default_output_dir: ./reports
report_format: markdown

# Optional - API Settings
perplexity_base_url: https://api.perplexity.ai
perplexity_model: llama-3.1-sonar-small-128k-online
api_rate_limit: 60
retry_attempts: 3
retry_delay: 1.0

# Optional - Logging
log_level: INFO
log_file: ./logs/perplsdk.log
```

## Configuration Options

### Required Settings

#### Perplexity API Key

Your Perplexity API key for authentication.

**Environment Variable:** `PERPLEXITY_API_KEY`  
**Config File:** `perplexity_api_key`  
**Required:** Yes

```python
from perplSDK.core.config import Config

config = Config(perplexity_api_key="your-api-key")
```

### Perplexity API Settings

#### Base URL

API endpoint URL (default: `https://api.perplexity.ai`)

**Environment Variable:** `PERPLEXITY_BASE_URL`  
**Config File:** `perplexity_base_url`  
**Default:** `https://api.perplexity.ai`

#### Model

Default model to use for queries.

**Environment Variable:** `PERPLEXITY_MODEL`  
**Config File:** `perplexity_model`  
**Default:** `llama-3.1-sonar-small-128k-online`

**Available Models:**
- `llama-3.1-sonar-small-128k-online` - Fast, cost-effective
- `llama-3.1-sonar-large-128k-online` - More accurate, higher cost
- `llama-3.1-sonar-huge-128k-online` - Highest accuracy

```python
config = Config(
    perplexity_api_key="your-key",
    perplexity_model="llama-3.1-sonar-large-128k-online"
)
```

### GitHub Integration Settings

#### GitHub Token

Personal access token for GitHub API.

**Environment Variable:** `GITHUB_TOKEN`  
**Config File:** `github_token`  
**Required:** Only for GitHub integration

**Creating a Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Copy token and set in environment variable

#### GitHub Repository

Repository in format `owner/repo`.

**Environment Variable:** `GITHUB_REPO`  
**Config File:** `github_repo`  
**Required:** Only for GitHub integration

```python
config = Config(
    github_token="ghp_your_token",
    github_repo="ev-max2024/research-reports"
)
```

#### GitHub Branch

Default branch for operations.

**Environment Variable:** `GITHUB_BRANCH`  
**Config File:** `github_branch`  
**Default:** `main`

### Report Settings

#### Output Directory

Default directory for saving reports.

**Environment Variable:** `OUTPUT_DIR`  
**Config File:** `default_output_dir`  
**Default:** `./reports`

```python
config = Config(
    perplexity_api_key="your-key",
    default_output_dir="./custom_reports"
)
```

#### Report Format

Default format for reports.

**Environment Variable:** `REPORT_FORMAT`  
**Config File:** `report_format`  
**Default:** `markdown`

### Rate Limiting

#### API Rate Limit

Maximum API requests per minute.

**Environment Variable:** `API_RATE_LIMIT`  
**Config File:** `api_rate_limit`  
**Default:** `60`

```python
config = Config(
    perplexity_api_key="your-key",
    api_rate_limit=100  # 100 requests per minute
)
```

#### Retry Attempts

Number of retry attempts for failed requests.

**Environment Variable:** `RETRY_ATTEMPTS`  
**Config File:** `retry_attempts`  
**Default:** `3`

#### Retry Delay

Delay between retry attempts (seconds).

**Environment Variable:** `RETRY_DELAY`  
**Config File:** `retry_delay`  
**Default:** `1.0`

### Logging

#### Log Level

Logging level for the SDK.

**Environment Variable:** `LOG_LEVEL`  
**Config File:** `log_level`  
**Default:** `INFO`

**Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

```python
config = Config(
    perplexity_api_key="your-key",
    log_level="DEBUG"
)
```

#### Log File

Path to log file (optional).

**Environment Variable:** `LOG_FILE`  
**Config File:** `log_file`  
**Default:** `None` (logs to console only)

## Loading Configuration

### From Environment Variables

```python
from perplSDK.core.config import Config

# Load from environment variables
config = Config.from_env()
```

### From Configuration File

```python
from perplSDK.core.config import Config

# Load from YAML file
config = Config.from_file("config.yaml")
```

### Programmatic Configuration

```python
from perplSDK.core.config import Config

config = Config(
    perplexity_api_key="your-api-key",
    perplexity_model="llama-3.1-sonar-large-128k-online",
    github_token="your-github-token",
    github_repo="owner/repo",
    default_output_dir="./reports",
    api_rate_limit=100,
    log_level="DEBUG"
)
```

### Saving Configuration

```python
# Save configuration to file
config.save_to_file("my_config.yaml")
```

## Configuration Priority

When multiple configuration sources are present, they are applied in this order (later sources override earlier):

1. Default values
2. Configuration file
3. Environment variables
4. Programmatic configuration

## Validation

Configuration is validated when creating clients:

```python
from perplSDK import PerplexityClient
from perplSDK.core.exceptions import ConfigurationError

try:
    config = Config()  # Missing API key
    client = PerplexityClient(config)
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Environment-Specific Configuration

### Development

```yaml
# config.dev.yaml
perplexity_api_key: ${PERPLEXITY_DEV_KEY}
log_level: DEBUG
default_output_dir: ./dev_reports
```

### Production

```yaml
# config.prod.yaml
perplexity_api_key: ${PERPLEXITY_PROD_KEY}
log_level: WARNING
default_output_dir: /var/reports
api_rate_limit: 100
```

### Testing

```yaml
# config.test.yaml
perplexity_api_key: test-key
log_level: DEBUG
default_output_dir: ./test_reports
```

## Best Practices

1. **Use Environment Variables**: Store sensitive data in environment variables, not code
2. **Separate Environments**: Use different configurations for dev/test/prod
3. **Version Control**: Add `.env` and sensitive config files to `.gitignore`
4. **Validate Early**: Validate configuration at application startup
5. **Document Settings**: Document custom configuration requirements
6. **Use .env Files**: Use `.env` files for local development
7. **Secure Tokens**: Never commit API keys or tokens to version control

## Example Configurations

### Minimal Configuration

```python
from perplSDK import PerplexityClient

# Minimal - just API key from environment
client = PerplexityClient()
```

### Complete Configuration

```python
from perplSDK.core.config import Config
from perplSDK import PerplexityClient, ResearchAutomation
from perplSDK.github_integration.publisher import GitHubPublisher

# Complete configuration
config = Config(
    # Required
    perplexity_api_key="your-api-key",
    
    # API Settings
    perplexity_model="llama-3.1-sonar-large-128k-online",
    api_rate_limit=100,
    retry_attempts=5,
    retry_delay=2.0,
    
    # GitHub Integration
    github_token="your-github-token",
    github_repo="owner/repo",
    github_branch="main",
    
    # Reports
    default_output_dir="./reports",
    report_format="markdown",
    
    # Logging
    log_level="INFO",
    log_file="./logs/perplsdk.log"
)

# Use configuration
client = PerplexityClient(config)
research = ResearchAutomation(config)
github = GitHubPublisher(config)
```

### Organization-Specific Configuration

```python
# EV MAX INC configuration
config = Config.from_env()

# Override for specific use case
config.perplexity_model = "llama-3.1-sonar-large-128k-online"
config.default_output_dir = "./ev_max_reports"
config.api_rate_limit = 120

# Use throughout application
```

## Troubleshooting

### Missing API Key

**Error:** `ConfigurationError: Perplexity API key is required`

**Solution:** Set `PERPLEXITY_API_KEY` environment variable or provide in config

### Invalid GitHub Token

**Error:** `GitHubPublishingError: Failed to connect to GitHub repository`

**Solution:** Verify token has correct permissions and repository exists

### Rate Limit Issues

**Error:** `RateLimitError: Rate limit exceeded`

**Solution:** Reduce `api_rate_limit` or increase request spacing

### File Permission Issues

**Error:** `PermissionError: Cannot write to output directory`

**Solution:** Ensure `default_output_dir` exists and is writable

## See Also

- [PerplexityClient API](../api/client.md)
- [GitHub Integration](../api/github.md)
- [Automated Workflows Guide](automation.md)
