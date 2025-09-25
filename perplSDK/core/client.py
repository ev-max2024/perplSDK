"""Perplexity API client for making research queries."""

import time
import asyncio
from typing import Dict, List, Optional, Union, Any
import requests
import aiohttp
from pydantic import BaseModel

from .config import Config
from .exceptions import APIError, AuthenticationError, RateLimitError


class SearchResult(BaseModel):
    """Model for search results from Perplexity API."""
    
    content: str
    sources: List[str] = []
    citations: List[Dict] = []
    model: str
    usage: Dict[str, Any] = {}


class PerplexityClient:
    """Client for interacting with Perplexity API."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the Perplexity client.
        
        Args:
            config: Configuration object. If None, loads from environment.
        """
        self.config = config or Config.from_env()
        self.config.validate_required_fields()
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.config.perplexity_api_key}",
            "Content-Type": "application/json",
            "User-Agent": "perplSDK/0.1.0"
        })
        
        # Rate limiting
        self._last_request_time = 0
        self._request_count = 0
        self._request_times = []
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        current_time = time.time()
        
        # Clean old request times (older than 1 minute)
        self._request_times = [t for t in self._request_times if current_time - t < 60]
        
        if len(self._request_times) >= self.config.api_rate_limit:
            sleep_time = 60 - (current_time - self._request_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self._request_times.append(current_time)
    
    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Perplexity API with error handling and retries."""
        self._check_rate_limit()
        
        url = f"{self.config.perplexity_base_url}/{endpoint}"
        
        for attempt in range(self.config.retry_attempts):
            try:
                response = self.session.post(url, json=payload, timeout=30)
                
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key or authentication failed")
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded", status_code=429)
                elif response.status_code >= 400:
                    raise APIError(
                        f"API request failed with status {response.status_code}",
                        status_code=response.status_code,
                        response_data=response.json() if response.content else None
                    )
                
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == self.config.retry_attempts - 1:
                    raise APIError(f"Request failed after {self.config.retry_attempts} attempts: {str(e)}")
                time.sleep(self.config.retry_delay * (2 ** attempt))  # Exponential backoff
    
    def search(
        self,
        query: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.2,
        top_p: float = 0.9,
        return_citations: bool = True,
        return_images: bool = False,
        recency_filter: Optional[str] = None
    ) -> SearchResult:
        """Perform a search query using Perplexity API.
        
        Args:
            query: The search query or question
            model: Model to use (defaults to config default)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-2)
            top_p: Nucleus sampling parameter
            return_citations: Whether to return citations
            return_images: Whether to return images
            recency_filter: Time filter ("month", "week", "day", "hour")
            
        Returns:
            SearchResult object with the response
        """
        payload = {
            "model": model or self.config.perplexity_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful research assistant. Provide accurate, well-sourced information."
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "temperature": temperature,
            "top_p": top_p,
            "return_citations": return_citations,
            "return_images": return_images,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if recency_filter:
            payload["recency_filter"] = recency_filter
        
        response_data = self._make_request("chat/completions", payload)
        
        # Extract response content
        if "choices" in response_data and response_data["choices"]:
            choice = response_data["choices"][0]
            content = choice.get("message", {}).get("content", "")
            
            return SearchResult(
                content=content,
                sources=choice.get("sources", []),
                citations=choice.get("citations", []),
                model=response_data.get("model", model or self.config.perplexity_model),
                usage=response_data.get("usage", {})
            )
        else:
            raise APIError("No response content received from API")
    
    async def async_search(
        self,
        query: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.2,
        top_p: float = 0.9,
        return_citations: bool = True,
        return_images: bool = False,
        recency_filter: Optional[str] = None
    ) -> SearchResult:
        """Async version of search method."""
        payload = {
            "model": model or self.config.perplexity_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful research assistant. Provide accurate, well-sourced information."
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "temperature": temperature,
            "top_p": top_p,
            "return_citations": return_citations,
            "return_images": return_images,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if recency_filter:
            payload["recency_filter"] = recency_filter
        
        url = f"{self.config.perplexity_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.perplexity_api_key}",
            "Content-Type": "application/json",
            "User-Agent": "perplSDK/0.1.0"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 401:
                    raise AuthenticationError("Invalid API key or authentication failed")
                elif response.status == 429:
                    raise RateLimitError("Rate limit exceeded", status_code=429)
                elif response.status >= 400:
                    error_data = await response.json() if response.content_type == 'application/json' else None
                    raise APIError(
                        f"API request failed with status {response.status}",
                        status_code=response.status,
                        response_data=error_data
                    )
                
                response_data = await response.json()
                
                # Extract response content
                if "choices" in response_data and response_data["choices"]:
                    choice = response_data["choices"][0]
                    content = choice.get("message", {}).get("content", "")
                    
                    return SearchResult(
                        content=content,
                        sources=choice.get("sources", []),
                        citations=choice.get("citations", []),
                        model=response_data.get("model", model or self.config.perplexity_model),
                        usage=response_data.get("usage", {})
                    )
                else:
                    raise APIError("No response content received from API")
    
    def batch_search(self, queries: List[str], **kwargs) -> List[SearchResult]:
        """Perform multiple search queries in batch.
        
        Args:
            queries: List of search queries
            **kwargs: Additional arguments passed to search method
            
        Returns:
            List of SearchResult objects
        """
        results = []
        for query in queries:
            try:
                result = self.search(query, **kwargs)
                results.append(result)
            except Exception as e:
                # Create error result
                results.append(SearchResult(
                    content=f"Error: {str(e)}",
                    sources=[],
                    citations=[],
                    model=kwargs.get("model", self.config.perplexity_model)
                ))
        return results
    
    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()