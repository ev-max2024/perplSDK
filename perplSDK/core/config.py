"""Configuration management for perplSDK."""

import os
from typing import Optional, Dict, Any
from pathlib import Path
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from .exceptions import ConfigurationError


class Config(BaseModel):
    """Configuration model for perplSDK."""
    
    # Perplexity API settings
    perplexity_api_key: Optional[str] = Field(default=None, description="Perplexity API key")
    perplexity_base_url: str = Field(default="https://api.perplexity.ai", description="Perplexity API base URL")
    perplexity_model: str = Field(default="llama-3.1-sonar-small-128k-online", description="Default model to use")
    
    # GitHub integration settings
    github_token: Optional[str] = Field(default=None, description="GitHub access token")
    github_repo: Optional[str] = Field(default=None, description="GitHub repository (owner/repo)")
    github_branch: str = Field(default="main", description="Default branch for GitHub operations")
    
    # Report settings
    default_output_dir: str = Field(default="./reports", description="Default directory for report outputs")
    report_format: str = Field(default="markdown", description="Default report format")
    
    # Rate limiting
    api_rate_limit: int = Field(default=60, description="API requests per minute")
    retry_attempts: int = Field(default=3, description="Number of retry attempts for failed requests")
    retry_delay: float = Field(default=1.0, description="Delay between retry attempts (seconds)")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        load_dotenv()
        
        return cls(
            perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
            github_token=os.getenv("GITHUB_TOKEN"),
            github_repo=os.getenv("GITHUB_REPO"),
            github_branch=os.getenv("GITHUB_BRANCH", "main"),
            default_output_dir=os.getenv("OUTPUT_DIR", "./reports"),
            api_rate_limit=int(os.getenv("API_RATE_LIMIT", "60")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE"),
        )
    
    @classmethod
    def from_file(cls, config_path: str) -> "Config":
        """Create configuration from YAML file."""
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            return cls(**config_data)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML configuration: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {e}")
    
    def save_to_file(self, config_path: str) -> None:
        """Save configuration to YAML file."""
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                yaml.dump(self.model_dump(), f, default_flow_style=False)
        except Exception as e:
            raise ConfigurationError(f"Error saving configuration: {e}")
    
    def validate_required_fields(self) -> None:
        """Validate that required fields are set."""
        if not self.perplexity_api_key:
            raise ConfigurationError("Perplexity API key is required")