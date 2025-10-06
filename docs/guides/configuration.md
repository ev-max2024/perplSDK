# Configuration Guide

This guide covers all aspects of configuring perplSDK, including environment variables, configuration files, API settings, and best practices for different deployment scenarios.

## Overview

perplSDK supports multiple configuration methods:
- Environment variables
- Configuration files (YAML)
- Programmatic configuration
- Runtime configuration

## Quick Start

### Environment Variables

The simplest way to configure perplSDK is through environment variables:

```bash
export PERPLEXITY_API_KEY="your-perplexity-api-key"
export GITHUB_TOKEN="your-github-token"
export GITHUB_REPO="owner/repo-name"
```

### .env File

Create a `.env` file in your project root:

```bash
# Perplexity API Configuration
PERPLEXITY_API_KEY=your-perplexity-api-key
PERPLEXITY_BASE_URL=https://api.perplexity.ai
PERPLEXITY_MODEL=llama-3.1-sonar-small-128k-online

# GitHub Integration (Optional)
GITHUB_TOKEN=your-github-personal-access-token
GITHUB_REPO=owner/repository-name
GITHUB_BRANCH=main

# Report Settings
OUTPUT_DIR=./reports
REPORT_FORMAT=markdown

# Rate Limiting
API_RATE_LIMIT=60
RETRY_ATTEMPTS=3
RETRY_DELAY=1.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/perplsdk.log
```

## Configuration Options

### Perplexity API Settings

#### perplexity_api_key (Required)

Your Perplexity API key.

```python
config = Config(perplexity_api_key="your-api-key")
```

**Environment Variable:** `PERPLEXITY_API_KEY`

**Security Note:** Never commit API keys to version control. Use environment variables or secure secret management.

#### perplexity_base_url

API base URL.

- **Default:** `https://api.perplexity.ai`
- **Environment Variable:** `PERPLEXITY_BASE_URL`

```python
config = Config(
    perplexity_api_key="your-key",
    perplexity_base_url="https://api.perplexity.ai"
)
```

#### perplexity_model

Default model to use for queries.

- **Default:** `llama-3.1-sonar-small-128k-online`
- **Environment Variable:** `PERPLEXITY_MODEL`

Available models:
- `llama-3.1-sonar-small-128k-online` - Fast, cost-effective
- `llama-3.1-sonar-large-128k-online` - More comprehensive
- `llama-3.1-sonar-huge-128k-online` - Maximum capability

```python
config = Config(
    perplexity_api_key="your-key",
    perplexity_model="llama-3.1-sonar-large-128k-online"
)
```

### GitHub Integration Settings

#### github_token (Optional)

GitHub personal access token for repository operations.

- **Environment Variable:** `GITHUB_TOKEN`
- **Required Scopes:** `repo`, `workflow`

To create a token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Generate and save the token

```python
config = Config(
    perplexity_api_key="your-api-key",
    github_token="your-github-token"
)
```

#### github_repo (Optional)

Repository in `owner/repo` format.

- **Environment Variable:** `GITHUB_REPO`

```python
config = Config(
    github_token="your-token",
    github_repo="ev-max2024/perplSDK"
)
```

#### github_branch

Default branch for operations.

- **Default:** `main`
- **Environment Variable:** `GITHUB_BRANCH`

```python
config = Config(
    github_token="your-token",
    github_repo="owner/repo",
    github_branch="develop"
)
```

### Report Settings

#### default_output_dir

Default directory for report outputs.

- **Default:** `./reports`
- **Environment Variable:** `OUTPUT_DIR`

```python
config = Config(
    perplexity_api_key="your-key",
    default_output_dir="/var/reports"
)
```

#### report_format

Default report format.

- **Default:** `markdown`
- **Options:** `markdown`, `html`, `pdf`
- **Environment Variable:** `REPORT_FORMAT`

```python
config = Config(
    perplexity_api_key="your-key",
    report_format="html"
)
```

### Rate Limiting and Retry Settings

#### api_rate_limit

Maximum API requests per minute.

- **Default:** `60`
- **Environment Variable:** `API_RATE_LIMIT`

```python
config = Config(
    perplexity_api_key="your-key",
    api_rate_limit=30  # More conservative
)
```

#### retry_attempts

Number of retry attempts for failed requests.

- **Default:** `3`
- **Environment Variable:** `RETRY_ATTEMPTS`

```python
config = Config(
    perplexity_api_key="your-key",
    retry_attempts=5  # More retries
)
```

#### retry_delay

Delay between retry attempts in seconds.

- **Default:** `1.0`
- **Environment Variable:** `RETRY_DELAY`

```python
config = Config(
    perplexity_api_key="your-key",
    retry_delay=2.0  # Longer delay
)
```

### Logging Settings

#### log_level

Logging verbosity level.

- **Default:** `INFO`
- **Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Environment Variable:** `LOG_LEVEL`

```python
config = Config(
    perplexity_api_key="your-key",
    log_level="DEBUG"
)
```

#### log_file

Path to log file.

- **Default:** `None` (logs to console)
- **Environment Variable:** `LOG_FILE`

```python
config = Config(
    perplexity_api_key="your-key",
    log_file="/var/log/perplsdk.log"
)
```

## Configuration Methods

### 1. Environment Variables (Recommended)

```python
from perplSDK.core.config import Config

# Loads from environment variables automatically
config = Config.from_env()
```

**Advantages:**
- Easy to manage in different environments
- Works well with Docker and cloud deployments
- Keeps secrets out of code

### 2. Configuration File

Create a `config.yaml` file:

```yaml
perplexity_api_key: your-api-key
perplexity_base_url: https://api.perplexity.ai
perplexity_model: llama-3.1-sonar-small-128k-online

github_token: your-github-token
github_repo: owner/repo
github_branch: main

default_output_dir: ./reports
report_format: markdown

api_rate_limit: 60
retry_attempts: 3
retry_delay: 1.0

log_level: INFO
log_file: ./logs/perplsdk.log
```

Load the configuration:

```python
from perplSDK.core.config import Config

config = Config.from_file("config.yaml")
```

**Advantages:**
- Easy to version control (without secrets)
- Clear documentation of settings
- Easy to share team configurations

**Security:** Use `.gitignore` to exclude files containing secrets.

### 3. Programmatic Configuration

```python
from perplSDK.core.config import Config

config = Config(
    perplexity_api_key="your-key",
    github_token="your-token",
    github_repo="owner/repo",
    api_rate_limit=60,
    log_level="INFO"
)
```

**Advantages:**
- Full control over configuration
- Can load secrets from secure vaults
- Dynamic configuration based on runtime conditions

### 4. Hybrid Approach (Recommended for Production)

```python
from perplSDK.core.config import Config
import os

# Load base config from file
config = Config.from_file("config.yaml")

# Override sensitive values from environment
config.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
config.github_token = os.getenv("GITHUB_TOKEN")
```

## Configuration for Different Environments

### Development

```yaml
# config.dev.yaml
perplexity_model: llama-3.1-sonar-small-128k-online
api_rate_limit: 30
log_level: DEBUG
default_output_dir: ./dev-reports
```

```python
config = Config.from_file("config.dev.yaml")
```

### Staging

```yaml
# config.staging.yaml
perplexity_model: llama-3.1-sonar-large-128k-online
api_rate_limit: 60
log_level: INFO
default_output_dir: ./staging-reports
```

### Production

```yaml
# config.prod.yaml
perplexity_model: llama-3.1-sonar-large-128k-online
api_rate_limit: 60
retry_attempts: 5
log_level: WARNING
log_file: /var/log/perplsdk/production.log
default_output_dir: /var/reports
```

Load based on environment:

```python
import os
from perplSDK.core.config import Config

env = os.getenv("ENV", "dev")
config = Config.from_file(f"config.{env}.yaml")

# Override with environment variables for secrets
config.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
config.github_token = os.getenv("GITHUB_TOKEN")
```

## Validation

Validate configuration before use:

```python
from perplSDK.core.config import Config
from perplSDK.core.exceptions import ConfigurationError

try:
    config = Config.from_env()
    config.validate_required_fields()
    print("✓ Configuration valid")
except ConfigurationError as e:
    print(f"✗ Configuration error: {e}")
    exit(1)
```

## Saving Configuration

Save current configuration to a file:

```python
config = Config(
    perplexity_api_key="your-key",
    api_rate_limit=60,
    log_level="INFO"
)

config.save_to_file("my_config.yaml")
```

**Note:** Be careful not to commit files containing API keys.

## Docker Configuration

### Using Environment Variables

```dockerfile
FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install perplSDK

ENV PERPLEXITY_API_KEY=""
ENV GITHUB_TOKEN=""
ENV GITHUB_REPO=""

CMD ["python", "app.py"]
```

Run with environment variables:

```bash
docker run \
  -e PERPLEXITY_API_KEY="your-key" \
  -e GITHUB_TOKEN="your-token" \
  -e GITHUB_REPO="owner/repo" \
  myapp
```

### Using Docker Secrets

```yaml
# docker-compose.yml
version: '3.8'
services:
  perplsdk:
    image: myapp
    secrets:
      - perplexity_key
      - github_token
    environment:
      PERPLEXITY_API_KEY_FILE: /run/secrets/perplexity_key
      GITHUB_TOKEN_FILE: /run/secrets/github_token

secrets:
  perplexity_key:
    external: true
  github_token:
    external: true
```

## Kubernetes Configuration

### ConfigMap for Non-Sensitive Settings

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: perplsdk-config
data:
  api_rate_limit: "60"
  log_level: "INFO"
  output_dir: "/var/reports"
```

### Secret for Sensitive Data

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: perplsdk-secrets
type: Opaque
data:
  perplexity-api-key: <base64-encoded-key>
  github-token: <base64-encoded-token>
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: perplsdk-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp
        env:
        - name: PERPLEXITY_API_KEY
          valueFrom:
            secretKeyRef:
              name: perplsdk-secrets
              key: perplexity-api-key
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: perplsdk-secrets
              key: github-token
        - name: API_RATE_LIMIT
          valueFrom:
            configMapKeyRef:
              name: perplsdk-config
              key: api_rate_limit
```

## Security Best Practices

### 1. Never Commit Secrets

Add to `.gitignore`:

```
.env
*.yaml.local
config.prod.yaml
secrets/
```

### 2. Use Secret Management

For production, use:
- AWS Secrets Manager
- Azure Key Vault
- Google Cloud Secret Manager
- HashiCorp Vault

Example with AWS Secrets Manager:

```python
import boto3
import json
from perplSDK.core.config import Config

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

secrets = get_secret('perplsdk/production')

config = Config(
    perplexity_api_key=secrets['perplexity_api_key'],
    github_token=secrets['github_token'],
    # ... other settings from file
)
```

### 3. Rotate Keys Regularly

Implement key rotation:

```python
def check_and_rotate_keys():
    # Check key age
    # Rotate if needed
    # Update configuration
    pass
```

### 4. Use Read-Only Tokens Where Possible

For GitHub, create tokens with minimal required permissions:
- Read-only for fetching data
- Write permissions only where needed

## Troubleshooting

### Missing API Key

```
ConfigurationError: Perplexity API key is required
```

**Solution:** Set `PERPLEXITY_API_KEY` environment variable or in config file.

### Invalid Configuration File

```
ConfigurationError: Error loading configuration: ...
```

**Solution:** Check YAML syntax and file path.

### Rate Limit Issues

If hitting rate limits frequently:

```python
config = Config(
    perplexity_api_key="your-key",
    api_rate_limit=30,  # Reduce rate
    retry_attempts=5,   # More retries
    retry_delay=2.0     # Longer delays
)
```

### GitHub Authentication Failed

```
GitHubPublishingError: Failed to connect to GitHub repository
```

**Solution:** 
1. Verify token has correct scopes
2. Check repository name format (`owner/repo`)
3. Ensure repository exists and token has access

## Configuration Examples

### Minimal Configuration

```python
from perplSDK.core.config import Config

config = Config(perplexity_api_key="your-key")
```

### Full Configuration

```python
config = Config(
    perplexity_api_key="your-api-key",
    perplexity_base_url="https://api.perplexity.ai",
    perplexity_model="llama-3.1-sonar-large-128k-online",
    github_token="your-github-token",
    github_repo="owner/repo",
    github_branch="main",
    default_output_dir="/var/reports",
    report_format="markdown",
    api_rate_limit=60,
    retry_attempts=3,
    retry_delay=1.0,
    log_level="INFO",
    log_file="/var/log/perplsdk.log"
)
```

### High-Volume Configuration

For high-volume usage:

```python
config = Config(
    perplexity_api_key="your-key",
    perplexity_model="llama-3.1-sonar-small-128k-online",
    api_rate_limit=100,  # Higher if your plan allows
    retry_attempts=2,     # Fewer retries for speed
    retry_delay=0.5       # Shorter delays
)
```

## See Also

- [PerplexityClient API](../api/client.md)
- [Security Best Practices](security.md)
- [Deployment Guide](deployment.md)
