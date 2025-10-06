# Privacy and Security Guide

This guide covers privacy considerations, data handling, security best practices, and compliance requirements when using perplSDK.

## Overview

perplSDK handles potentially sensitive research data and API credentials. This guide helps you:
- Protect API keys and tokens
- Handle research data securely
- Comply with data protection regulations
- Implement security best practices
- Manage user access and permissions

## Data Privacy

### Data Collection and Storage

#### What Data Does perplSDK Collect?

perplSDK collects and processes:

1. **Research Queries**: Questions and topics submitted for analysis
2. **API Responses**: Results from Perplexity API
3. **Configuration Data**: Settings and preferences
4. **Usage Metrics**: API usage statistics (optional)
5. **Report Data**: Generated reports and analysis

#### Where Is Data Stored?

- **Local Storage**: Reports saved to your specified output directory
- **GitHub**: If publishing is enabled, reports stored in your repository
- **No Cloud Storage**: perplSDK does not store your data in external cloud services

### Data Handling

#### Research Data

```python
from perplSDK.core.config import Config

# Configure where data is stored
config = Config(
    perplexity_api_key="your-key",
    default_output_dir="/secure/path/reports"  # Use secure location
)

# Research results are only stored locally
research = ResearchAutomation(config)
project = research.create_project("Sensitive Analysis")
# ... project results stored in configured directory
```

#### Sensitive Information

**Never include sensitive information in:**
- Research queries
- Report titles or metadata
- Configuration files committed to version control
- GitHub published reports (if public)

```python
# Bad - includes sensitive info
project.add_query("Confidential project X competitive analysis")

# Good - generic query
project.add_query("Competitive analysis for automotive sector")
```

### Data Retention

Implement data retention policies:

```python
import os
from datetime import datetime, timedelta
from pathlib import Path

def cleanup_old_reports(report_dir, days_to_keep=90):
    """Remove reports older than specified days."""
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    report_path = Path(report_dir)
    for file in report_path.glob("**/*.md"):
        if file.stat().st_mtime < cutoff_date.timestamp():
            print(f"Removing old report: {file}")
            file.unlink()

# Run periodically
cleanup_old_reports("./reports", days_to_keep=90)
```

## Security Best Practices

### API Key Management

#### 1. Never Commit API Keys

Add to `.gitignore`:

```gitignore
# API Keys and Secrets
.env
.env.local
.env.*.local
config.yaml
config.prod.yaml
secrets/
*.key
*.pem
```

#### 2. Use Environment Variables

```bash
# Set in environment
export PERPLEXITY_API_KEY="your-key"
export GITHUB_TOKEN="your-token"

# Or use .env file (not committed)
echo "PERPLEXITY_API_KEY=your-key" > .env
echo "GITHUB_TOKEN=your-token" >> .env
```

```python
from perplSDK.core.config import Config

# Loads from environment automatically
config = Config.from_env()
```

#### 3. Use Secret Management Services

**AWS Secrets Manager:**

```python
import boto3
import json
from perplSDK.core.config import Config

def get_secrets_from_aws(secret_name):
    """Retrieve secrets from AWS Secrets Manager."""
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Load secrets
secrets = get_secrets_from_aws('perplsdk/production')

config = Config(
    perplexity_api_key=secrets['perplexity_api_key'],
    github_token=secrets['github_token']
)
```

**Azure Key Vault:**

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secrets_from_azure(vault_url):
    """Retrieve secrets from Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    return {
        'perplexity_api_key': client.get_secret('perplexity-api-key').value,
        'github_token': client.get_secret('github-token').value
    }

secrets = get_secrets_from_azure("https://myvault.vault.azure.net/")
config = Config(**secrets)
```

**HashiCorp Vault:**

```python
import hvac

def get_secrets_from_vault(vault_url, token):
    """Retrieve secrets from HashiCorp Vault."""
    client = hvac.Client(url=vault_url, token=token)
    
    secret = client.secrets.kv.v2.read_secret_version(
        path='perplsdk/production'
    )
    
    return secret['data']['data']

secrets = get_secrets_from_vault('http://vault:8200', vault_token)
config = Config(**secrets)
```

#### 4. Rotate API Keys Regularly

```python
from datetime import datetime, timedelta

class APIKeyManager:
    """Manage API key rotation."""
    
    def __init__(self):
        self.last_rotation = datetime.now()
        self.rotation_interval = timedelta(days=90)
    
    def should_rotate(self):
        """Check if key should be rotated."""
        return datetime.now() - self.last_rotation > self.rotation_interval
    
    def rotate_key(self):
        """Rotate API key."""
        if self.should_rotate():
            # Notify administrators
            send_alert("API key rotation required")
            # Update key in secret manager
            # Update configuration
            self.last_rotation = datetime.now()

key_manager = APIKeyManager()
```

### Access Control

#### User Permissions

Implement role-based access control:

```python
class AccessControl:
    """Manage user access to SDK features."""
    
    ROLES = {
        'admin': ['read', 'write', 'publish', 'configure'],
        'researcher': ['read', 'write'],
        'viewer': ['read']
    }
    
    def __init__(self, user_role):
        self.user_role = user_role
        self.permissions = self.ROLES.get(user_role, [])
    
    def can_publish(self):
        """Check if user can publish to GitHub."""
        return 'publish' in self.permissions
    
    def can_configure(self):
        """Check if user can modify configuration."""
        return 'configure' in self.permissions
    
    def can_conduct_research(self):
        """Check if user can conduct research."""
        return 'write' in self.permissions

# Use access control
access = AccessControl('researcher')

if access.can_conduct_research():
    research = ResearchAutomation()
    # Conduct research
else:
    raise PermissionError("User does not have research permissions")
```

#### API Key Scoping

Create API keys with minimal required permissions:

```python
# GitHub token with minimal scopes
# Only grant: repo (if publishing) or read:repo (if only reading)

config = Config(
    github_token="token_with_minimal_scope",
    # Other config...
)
```

### Network Security

#### HTTPS Only

Ensure all API connections use HTTPS:

```python
config = Config(
    perplexity_api_key="your-key",
    perplexity_base_url="https://api.perplexity.ai"  # Always HTTPS
)

# Verify SSL certificates
import requests
session = requests.Session()
session.verify = True  # Always verify SSL
```

#### Proxy Configuration

For corporate environments:

```python
import os

# Set proxy environment variables
os.environ['HTTPS_PROXY'] = 'https://proxy.company.com:8080'
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'

# Configure certificate bundle
os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/company/ca-bundle.crt'
```

### Logging Security

#### Secure Logging

```python
import logging
import re

class SecureFormatter(logging.Formatter):
    """Formatter that redacts sensitive information."""
    
    REDACT_PATTERNS = [
        (r'api_key[=:]\s*[\'"]?([^\s\'"]+)', 'api_key=***REDACTED***'),
        (r'token[=:]\s*[\'"]?([^\s\'"]+)', 'token=***REDACTED***'),
        (r'password[=:]\s*[\'"]?([^\s\'"]+)', 'password=***REDACTED***'),
    ]
    
    def format(self, record):
        """Format log record and redact sensitive info."""
        message = super().format(record)
        
        for pattern, replacement in self.REDACT_PATTERNS:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        
        return message

# Configure secure logging
handler = logging.FileHandler('perplsdk.log')
handler.setFormatter(SecureFormatter())

logger = logging.getLogger('perplSDK')
logger.addHandler(handler)
```

#### Log Access Control

```python
import os
import stat

def secure_log_file(log_path):
    """Set secure permissions on log file."""
    # Owner read/write only
    os.chmod(log_path, stat.S_IRUSR | stat.S_IWUSR)

secure_log_file('/var/log/perplsdk/app.log')
```

## Compliance

### GDPR Compliance

If processing EU personal data:

#### 1. Data Minimization

```python
# Only collect necessary data
project = research.create_project("Market Analysis")
# Don't include personal identifiers in queries
project.add_query("General market trends")  # Good
# Avoid: project.add_query("John Doe's preferences")  # Bad
```

#### 2. Right to Erasure

Implement data deletion:

```python
def delete_user_data(user_id):
    """Delete all data for a user."""
    # Delete user's research projects
    # Delete user's reports
    # Remove from logs
    # Confirm deletion
    pass
```

#### 3. Data Portability

Export user data:

```python
def export_user_data(user_id):
    """Export user's data in portable format."""
    user_data = {
        "projects": get_user_projects(user_id),
        "reports": get_user_reports(user_id),
        "settings": get_user_settings(user_id)
    }
    
    import json
    with open(f"user_{user_id}_data.json", "w") as f:
        json.dump(user_data, f, indent=2)
```

### SOC 2 Compliance

For enterprise deployments:

#### Access Logging

```python
class AccessLogger:
    """Log all access to sensitive operations."""
    
    def log_access(self, user, operation, resource):
        """Log access attempt."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "operation": operation,
            "resource": resource,
            "ip_address": get_client_ip()
        }
        
        # Write to audit log
        with open("audit.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

access_logger = AccessLogger()
access_logger.log_access("user@company.com", "conduct_research", "project_123")
```

#### Encryption at Rest

```python
from cryptography.fernet import Fernet

class EncryptedStorage:
    """Encrypt sensitive data at rest."""
    
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def save_encrypted(self, data, filename):
        """Save encrypted data."""
        encrypted = self.cipher.encrypt(data.encode())
        with open(filename, 'wb') as f:
            f.write(encrypted)
    
    def load_encrypted(self, filename):
        """Load and decrypt data."""
        with open(filename, 'rb') as f:
            encrypted = f.read()
        return self.cipher.decrypt(encrypted).decode()

# Use encryption for sensitive reports
key = Fernet.generate_key()  # Store securely
storage = EncryptedStorage(key)
storage.save_encrypted(sensitive_report, "report.enc")
```

## Incident Response

### Security Incident Handling

```python
class SecurityIncidentHandler:
    """Handle security incidents."""
    
    def __init__(self):
        self.incidents = []
    
    def report_incident(self, incident_type, details):
        """Report a security incident."""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "type": incident_type,
            "details": details,
            "severity": self.calculate_severity(incident_type)
        }
        
        self.incidents.append(incident)
        
        # Alert security team
        if incident["severity"] in ["high", "critical"]:
            self.alert_security_team(incident)
        
        # Log incident
        self.log_incident(incident)
    
    def calculate_severity(self, incident_type):
        """Calculate incident severity."""
        severity_map = {
            "api_key_exposed": "critical",
            "unauthorized_access": "high",
            "data_leak": "critical",
            "rate_limit_exceeded": "low"
        }
        return severity_map.get(incident_type, "medium")
    
    def alert_security_team(self, incident):
        """Alert security team of incident."""
        # Send email, Slack notification, PagerDuty alert, etc.
        pass
    
    def log_incident(self, incident):
        """Log incident details."""
        with open("security_incidents.log", "a") as f:
            f.write(json.dumps(incident) + "\n")

# Use incident handler
incident_handler = SecurityIncidentHandler()

try:
    # Some operation
    pass
except Exception as e:
    if "authentication failed" in str(e).lower():
        incident_handler.report_incident(
            "unauthorized_access",
            {"error": str(e), "user": current_user}
        )
```

### API Key Compromise

If API key is compromised:

1. **Immediately revoke the key**
2. **Generate new key**
3. **Update all systems**
4. **Review access logs**
5. **Notify affected parties**

```python
def handle_key_compromise():
    """Handle compromised API key."""
    # 1. Revoke old key (in Perplexity/GitHub)
    
    # 2. Generate new key
    new_key = generate_new_api_key()
    
    # 3. Update configuration
    update_secret_manager("perplexity_api_key", new_key)
    
    # 4. Review logs
    suspicious_activity = review_access_logs()
    
    # 5. Notify
    if suspicious_activity:
        notify_security_team(suspicious_activity)
    
    # 6. Document incident
    document_incident("API key compromised and rotated")
```

## Security Checklist

### Deployment Checklist

- [ ] API keys stored in secure secret management
- [ ] No credentials in version control
- [ ] HTTPS enforced for all API connections
- [ ] SSL certificate verification enabled
- [ ] Logging configured with sensitive data redaction
- [ ] Access control implemented
- [ ] Data retention policy configured
- [ ] Backup and disaster recovery plan in place
- [ ] Security incident response plan documented
- [ ] Regular security audits scheduled

### Code Review Checklist

- [ ] No hardcoded credentials
- [ ] Sensitive data properly encrypted
- [ ] Input validation implemented
- [ ] Error messages don't leak sensitive info
- [ ] Logging doesn't expose credentials
- [ ] Proper exception handling
- [ ] Access control checks in place

### Operational Checklist

- [ ] API keys rotated regularly
- [ ] Access logs reviewed regularly
- [ ] Security patches applied
- [ ] Dependencies updated
- [ ] Vulnerability scans performed
- [ ] Penetration testing conducted
- [ ] Incident response drills conducted

## Additional Resources

### Security Tools

- **Secret scanning**: Use tools like git-secrets, truffleHog
- **Dependency scanning**: Use Snyk, Dependabot
- **SAST**: Use Bandit, SonarQube for Python
- **DAST**: Use OWASP ZAP for deployed applications

### Security Standards

- OWASP Top 10
- NIST Cybersecurity Framework
- ISO 27001
- SOC 2
- GDPR
- CCPA

## See Also

- [Configuration Guide](configuration.md)
- [Access Control Documentation](user_access.md)
- [Deployment Guide](deployment.md)
