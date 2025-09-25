"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path
import pytest

from perplSDK.core.config import Config
from perplSDK.core.exceptions import ConfigurationError


def test_config_from_env():
    """Test configuration loading from environment variables."""
    # Set test environment variables
    test_api_key = "test-api-key"
    os.environ["PERPLEXITY_API_KEY"] = test_api_key
    
    config = Config.from_env()
    
    assert config.perplexity_api_key == test_api_key
    assert config.perplexity_base_url == "https://api.perplexity.ai"
    assert config.api_rate_limit == 60
    
    # Clean up
    del os.environ["PERPLEXITY_API_KEY"]


def test_config_validation():
    """Test configuration validation."""
    config = Config()
    
    # Should raise error for missing API key
    with pytest.raises(ConfigurationError):
        config.validate_required_fields()
    
    # Should pass with API key set
    config.perplexity_api_key = "test-key"
    config.validate_required_fields()  # Should not raise


def test_config_from_file():
    """Test configuration loading from YAML file."""
    config_data = {
        "perplexity_api_key": "test-file-key",
        "api_rate_limit": 30,
        "log_level": "DEBUG"
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        import yaml
        yaml.dump(config_data, f)
        config_file = f.name
    
    try:
        config = Config.from_file(config_file)
        assert config.perplexity_api_key == "test-file-key"
        assert config.api_rate_limit == 30
        assert config.log_level == "DEBUG"
    finally:
        os.unlink(config_file)


def test_config_save_to_file():
    """Test configuration saving to file."""
    config = Config(
        perplexity_api_key="test-save-key",
        api_rate_limit=45
    )
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_file = f.name
    
    try:
        config.save_to_file(config_file)
        
        # Load and verify
        loaded_config = Config.from_file(config_file)
        assert loaded_config.perplexity_api_key == "test-save-key"
        assert loaded_config.api_rate_limit == 45
    finally:
        os.unlink(config_file)