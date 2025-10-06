# PerplexityClient API

The `PerplexityClient` is the core interface for interacting with the Perplexity API, providing both synchronous and asynchronous methods for AI-powered research queries.

## Overview

The client handles:
- API authentication and authorization
- Rate limiting and request throttling
- Error handling and automatic retries
- Response parsing and validation

## Installation

```python
from perplSDK import PerplexityClient
from perplSDK.core.config import Config
```

## Initialization

### Basic Initialization

```python
# Using environment variables
client = PerplexityClient()

# With explicit configuration
config = Config(perplexity_api_key="your-api-key")
client = PerplexityClient(config)
```

### Configuration Options

The client accepts a `Config` object with the following settings:

- `perplexity_api_key`: Your Perplexity API key (required)
- `perplexity_base_url`: API base URL (default: "https://api.perplexity.ai")
- `perplexity_model`: Default model to use (default: "llama-3.1-sonar-small-128k-online")
- `api_rate_limit`: Maximum requests per minute (default: 60)
- `retry_attempts`: Number of retry attempts for failed requests (default: 3)
- `retry_delay`: Delay between retry attempts in seconds (default: 1.0)

## Methods

### search()

Perform a synchronous search query.

**Signature:**
```python
def search(
    query: str,
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: float = 0.2,
    top_p: float = 0.9,
    return_citations: bool = True,
    return_images: bool = False,
    recency_filter: Optional[str] = None
) -> SearchResult
```

**Parameters:**
- `query` (str): The search query or question
- `model` (str, optional): Model to use, overrides default
- `max_tokens` (int, optional): Maximum tokens in response
- `temperature` (float): Sampling temperature (0.0-1.0, default: 0.2)
- `top_p` (float): Nucleus sampling parameter (default: 0.9)
- `return_citations` (bool): Include citations in response (default: True)
- `return_images` (bool): Include images in response (default: False)
- `recency_filter` (str, optional): Filter by recency ("month", "week", "day")

**Returns:**
- `SearchResult`: Object containing content, sources, citations, model info, and usage statistics

**Example:**
```python
result = client.search("Latest developments in EV battery technology")
print(result.content)
print(f"Sources: {len(result.sources)}")
```

### async_search()

Perform an asynchronous search query.

**Signature:**
```python
async def async_search(
    query: str,
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: float = 0.2,
    top_p: float = 0.9,
    return_citations: bool = True,
    return_images: bool = False,
    recency_filter: Optional[str] = None
) -> SearchResult
```

**Parameters:** Same as `search()`

**Returns:** Same as `search()`

**Example:**
```python
import asyncio

async def main():
    result = await client.async_search("EV market trends 2024")
    print(result.content)

asyncio.run(main())
```

### batch_search()

Perform multiple searches in parallel.

**Signature:**
```python
def batch_search(
    queries: List[str],
    parallel: bool = True,
    **kwargs
) -> List[SearchResult]
```

**Parameters:**
- `queries` (List[str]): List of search queries
- `parallel` (bool): Execute queries in parallel (default: True)
- `**kwargs`: Additional parameters passed to each search

**Returns:**
- `List[SearchResult]`: List of search results

**Example:**
```python
queries = [
    "EV battery technology trends",
    "Charging infrastructure developments",
    "EV market share by manufacturer"
]
results = client.batch_search(queries, parallel=True)
for result in results:
    print(result.content[:100])
```

## SearchResult Model

The `SearchResult` object contains:

```python
class SearchResult:
    content: str              # Main response content
    sources: List[str]        # List of source URLs
    citations: List[Dict]     # Detailed citation information
    model: str               # Model used for the query
    usage: Dict[str, Any]    # API usage statistics
```

## Rate Limiting

The client automatically enforces rate limiting based on the configured `api_rate_limit`:

- Tracks requests per minute
- Automatically sleeps when limit is reached
- Cleans up old request timestamps

## Error Handling

The client raises specific exceptions for different error conditions:

### APIError

General API errors, including:
- Network errors
- Server errors (5xx)
- Client errors (4xx)

```python
from perplSDK.core.exceptions import APIError

try:
    result = client.search("query")
except APIError as e:
    print(f"API error: {e}")
```

### AuthenticationError

Raised when API key is invalid or missing:

```python
from perplSDK.core.exceptions import AuthenticationError

try:
    result = client.search("query")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

### RateLimitError

Raised when rate limit is exceeded:

```python
from perplSDK.core.exceptions import RateLimitError

try:
    result = client.search("query")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
```

## Best Practices

### 1. Reuse Client Instances

Create one client instance and reuse it for multiple queries:

```python
client = PerplexityClient()

# Good - reuses connection
result1 = client.search("query 1")
result2 = client.search("query 2")
```

### 2. Use Batch Operations

For multiple queries, use `batch_search()` for better performance:

```python
# Good - parallel execution
results = client.batch_search(queries, parallel=True)

# Less efficient - sequential execution
results = [client.search(q) for q in queries]
```

### 3. Handle Errors Gracefully

Always handle potential exceptions:

```python
try:
    result = client.search("query")
except AuthenticationError:
    print("Check your API key")
except RateLimitError:
    print("Slow down, rate limit exceeded")
except APIError as e:
    print(f"API error: {e}")
```

### 4. Use Appropriate Parameters

Choose parameters based on your use case:

```python
# For factual queries - lower temperature
result = client.search(
    "EV sales statistics 2024",
    temperature=0.0,
    return_citations=True
)

# For creative queries - higher temperature
result = client.search(
    "Future of electric vehicles",
    temperature=0.7,
    return_citations=True
)
```

## Advanced Usage

### Custom Configuration

```python
config = Config(
    perplexity_api_key="your-key",
    api_rate_limit=30,  # Slower rate
    retry_attempts=5,   # More retries
    retry_delay=2.0     # Longer delay
)
client = PerplexityClient(config)
```

### With Context Manager

```python
with PerplexityClient() as client:
    result = client.search("query")
    print(result.content)
```

### Async Operations

```python
import asyncio

async def research():
    client = PerplexityClient()
    
    # Concurrent async searches
    tasks = [
        client.async_search("query 1"),
        client.async_search("query 2"),
        client.async_search("query 3")
    ]
    
    results = await asyncio.gather(*tasks)
    return results

results = asyncio.run(research())
```

## See Also

- [Configuration Guide](../guides/configuration.md)
- [Research Automation](research.md)
- [Error Handling Best Practices](../guides/error_handling.md)
