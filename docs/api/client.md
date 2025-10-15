# PerplexityClient API Reference

The `PerplexityClient` is the core client for interacting with the Perplexity API, providing both synchronous and asynchronous search capabilities with built-in rate limiting and error handling.

## Installation

```python
from perplSDK import PerplexityClient
from perplSDK.core.config import Config
```

## Initialization

### `PerplexityClient(config=None)`

Initialize the Perplexity client.

**Parameters:**
- `config` (Optional[Config]): Configuration object. If None, loads from environment variables.

**Example:**

```python
# Using default configuration (from environment)
client = PerplexityClient()

# Using custom configuration
config = Config(
    perplexity_api_key="your-api-key",
    perplexity_model="llama-3.1-sonar-small-128k-online"
)
client = PerplexityClient(config)
```

## Methods

### `search(query, model=None, **kwargs)`

Execute a synchronous search query.

**Parameters:**
- `query` (str): The search query or question
- `model` (Optional[str]): Model to use (defaults to config model)
- `**kwargs`: Additional parameters:
  - `return_images` (bool): Whether to return images
  - `return_related_questions` (bool): Whether to return related questions
  - `search_domain_filter` (List[str]): Domains to filter results
  - `search_recency_filter` (str): Time filter (e.g., "day", "week", "month")

**Returns:**
- `SearchResult`: Result object containing:
  - `content` (str): The response content
  - `sources` (List[str]): Source URLs
  - `citations` (List[Dict]): Citation information
  - `model` (str): Model used
  - `usage` (Dict): Token usage statistics

**Example:**

```python
result = client.search("Latest EV battery technology")
print(result.content)
print(f"Sources: {result.sources}")
```

### `search_async(query, model=None, **kwargs)`

Execute an asynchronous search query.

**Parameters:**
Same as `search()` method.

**Returns:**
- `SearchResult`: Result object (same as synchronous version)

**Example:**

```python
import asyncio

async def main():
    result = await client.search_async("EV market trends")
    print(result.content)

asyncio.run(main())
```

### `batch_search(queries, parallel=True, max_concurrent=5)`

Execute multiple search queries.

**Parameters:**
- `queries` (List[str]): List of query strings
- `parallel` (bool): Whether to execute queries in parallel
- `max_concurrent` (int): Maximum concurrent requests (for parallel execution)

**Returns:**
- `List[SearchResult]`: List of search results

**Example:**

```python
queries = [
    "EV battery innovations 2024",
    "Charging infrastructure trends",
    "Electric vehicle market share"
]
results = client.batch_search(queries, parallel=True)
```

## Data Models

### SearchResult

```python
class SearchResult:
    content: str              # Response content
    sources: List[str]        # Source URLs
    citations: List[Dict]     # Citation details
    model: str               # Model used
    usage: Dict[str, Any]    # Token usage stats
```

## Rate Limiting

The client automatically handles rate limiting based on configuration:

```python
config = Config(
    perplexity_api_key="your-key",
    api_rate_limit=60  # Requests per minute
)
```

## Error Handling

The client raises specific exceptions for different error types:

- `AuthenticationError`: Invalid API key
- `RateLimitError`: Rate limit exceeded
- `APIError`: General API errors

**Example:**

```python
from perplSDK.core.exceptions import APIError, AuthenticationError

try:
    result = client.search("query")
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(f"API error: {e}")
```

## Advanced Usage

### Custom Headers and Parameters

```python
result = client.search(
    "EV trends",
    return_related_questions=True,
    search_recency_filter="week",
    search_domain_filter=["reuters.com", "bloomberg.com"]
)
```

### Async Batch Processing

```python
import asyncio

async def batch_async():
    queries = ["query1", "query2", "query3"]
    tasks = [client.search_async(q) for q in queries]
    results = await asyncio.gather(*tasks)
    return results

results = asyncio.run(batch_async())
```

## Best Practices

1. **Use environment variables** for API keys rather than hardcoding
2. **Enable rate limiting** to avoid API throttling
3. **Use async methods** for better performance with multiple queries
4. **Handle exceptions** appropriately for production use
5. **Reuse client instances** rather than creating new ones for each request

## See Also

- [Configuration Guide](../guides/configuration.md)
- [Research Automation](research.md)
- [Report Generation](reports.md)
