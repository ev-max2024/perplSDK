"""Custom exceptions for perplSDK."""


class PerplSDKError(Exception):
    """Base exception for perplSDK errors."""
    pass


class APIError(PerplSDKError):
    """Exception raised for API-related errors."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(APIError):
    """Exception raised for authentication errors."""
    pass


class RateLimitError(APIError):
    """Exception raised when API rate limits are exceeded."""
    pass


class ConfigurationError(PerplSDKError):
    """Exception raised for configuration-related errors."""
    pass