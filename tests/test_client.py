"""Tests for Perplexity API client."""

import pytest
from unittest.mock import Mock, patch

from perplSDK.core.client import PerplexityClient, SearchResult
from perplSDK.core.config import Config
from perplSDK.core.exceptions import APIError, AuthenticationError


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = Config(
        perplexity_api_key="test-api-key",
        api_rate_limit=100
    )
    return config


@pytest.fixture
def client(mock_config):
    """Create a client with mock configuration."""
    return PerplexityClient(mock_config)


def test_client_initialization(mock_config):
    """Test client initialization."""
    client = PerplexityClient(mock_config)
    
    assert client.config.perplexity_api_key == "test-api-key"
    assert client.config.api_rate_limit == 100
    assert "Authorization" in client.session.headers
    assert "Bearer test-api-key" in client.session.headers["Authorization"]


def test_search_result_model():
    """Test SearchResult model."""
    result = SearchResult(
        content="Test content",
        sources=["http://example.com"],
        model="test-model"
    )
    
    assert result.content == "Test content"
    assert result.sources == ["http://example.com"]
    assert result.model == "test-model"
    assert result.citations == []
    assert result.usage == {}


@patch('requests.Session.post')
def test_search_success(mock_post, client):
    """Test successful search."""
    # Mock API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Test response content"
                },
                "sources": ["http://example.com"],
                "citations": []
            }
        ],
        "model": "test-model",
        "usage": {"total_tokens": 100}
    }
    mock_post.return_value = mock_response
    
    result = client.search("test query")
    
    assert isinstance(result, SearchResult)
    assert result.content == "Test response content"
    assert result.sources == ["http://example.com"]
    assert result.model == "test-model"
    assert result.usage == {"total_tokens": 100}


@patch('requests.Session.post')
def test_search_authentication_error(mock_post, client):
    """Test authentication error handling."""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_post.return_value = mock_response
    
    with pytest.raises(AuthenticationError):
        client.search("test query")


@patch('requests.Session.post')
def test_search_api_error(mock_post, client):
    """Test API error handling."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.content = b'{"error": "Server error"}'
    mock_response.json.return_value = {"error": "Server error"}
    mock_post.return_value = mock_response
    
    with pytest.raises(APIError):
        client.search("test query")


def test_batch_search(client):
    """Test batch search functionality."""
    with patch.object(client, 'search') as mock_search:
        # Mock individual search results
        mock_search.side_effect = [
            SearchResult(content="Result 1", model="test-model"),
            SearchResult(content="Result 2", model="test-model"),
        ]
        
        queries = ["query 1", "query 2"]
        results = client.batch_search(queries)
        
        assert len(results) == 2
        assert results[0].content == "Result 1"
        assert results[1].content == "Result 2"
        assert mock_search.call_count == 2


def test_rate_limiting(client):
    """Test rate limiting functionality."""
    # This is a basic test - in practice, rate limiting would need more complex testing
    import time
    
    # Record initial time
    start_time = time.time()
    
    # Call rate limit check (should not delay for first call)
    client._check_rate_limit()
    
    elapsed = time.time() - start_time
    assert elapsed < 0.1  # Should be very fast for first call