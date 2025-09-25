"""Text formatting utilities for perplSDK."""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime


class TextFormatter:
    """Utility class for text formatting and cleaning."""
    
    @staticmethod
    def clean_content(text: str) -> str:
        """Clean and normalize text content.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_key_points(text: str, max_points: int = 5) -> List[str]:
        """Extract key points from text content.
        
        Args:
            text: Text content to analyze
            max_points: Maximum number of points to extract
            
        Returns:
            List of key points
        """
        if not text:
            return []
        
        # Simple extraction based on sentence structure
        sentences = re.split(r'[.!?]+', text)
        
        # Filter and rank sentences
        key_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:  # Reasonable length
                # Prioritize sentences with key indicators
                score = 0
                key_indicators = [
                    'important', 'significant', 'key', 'major', 'critical',
                    'trend', 'growth', 'increase', 'decrease', 'market',
                    'technology', 'innovation', 'development', 'future'
                ]
                
                for indicator in key_indicators:
                    if indicator.lower() in sentence.lower():
                        score += 1
                
                key_sentences.append((sentence, score))
        
        # Sort by score and return top points
        key_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, _ in key_sentences[:max_points]]
    
    @staticmethod
    def create_summary(text: str, max_length: int = 300) -> str:
        """Create a summary of the text content.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summary text
        """
        if not text:
            return ""
        
        if len(text) <= max_length:
            return text
        
        # Extract first few sentences up to max_length
        sentences = re.split(r'[.!?]+', text)
        summary = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if len(summary + sentence) + 1 <= max_length - 3:  # Leave room for "..."
                    summary += sentence + ". "
                else:
                    break
        
        if len(summary) < len(text):
            summary += "..."
        
        return summary.strip()
    
    @staticmethod
    def format_sources(sources: List[str], max_sources: int = 10) -> str:
        """Format sources list for display.
        
        Args:
            sources: List of source URLs or citations
            max_sources: Maximum number of sources to include
            
        Returns:
            Formatted sources string
        """
        if not sources:
            return ""
        
        formatted_sources = []
        for i, source in enumerate(sources[:max_sources], 1):
            # Clean and format source
            source = source.strip()
            if source:
                formatted_sources.append(f"{i}. {source}")
        
        return "\n".join(formatted_sources)
    
    @staticmethod
    def format_timestamp(timestamp: Optional[datetime] = None) -> str:
        """Format timestamp for display.
        
        Args:
            timestamp: Datetime object (defaults to now)
            
        Returns:
            Formatted timestamp string
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to maximum length.
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add when truncating
            
        Returns:
            Truncated text
        """
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text.
        
        Args:
            text: Text content
            
        Returns:
            List of URLs found
        """
        if not text:
            return []
        
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        return list(set(urls))  # Remove duplicates
    
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """Extract numerical values from text.
        
        Args:
            text: Text content
            
        Returns:
            List of numerical values
        """
        if not text:
            return []
        
        # Pattern to match numbers (including decimals and percentages)
        number_pattern = r'-?\d+(?:\.\d+)?(?:%|\s*(?:billion|million|thousand|k|m|b))?'
        matches = re.findall(number_pattern, text.lower())
        
        numbers = []
        for match in matches:
            try:
                # Convert to float, handling suffixes
                match = match.replace('%', '').strip()
                
                multiplier = 1
                if match.endswith(('k', 'thousand')):
                    multiplier = 1000
                    match = match.replace('k', '').replace('thousand', '').strip()
                elif match.endswith(('m', 'million')):
                    multiplier = 1000000
                    match = match.replace('m', '').replace('million', '').strip()
                elif match.endswith(('b', 'billion')):
                    multiplier = 1000000000
                    match = match.replace('b', '').replace('billion', '').strip()
                
                if match:
                    numbers.append(float(match) * multiplier)
            except ValueError:
                continue
        
        return numbers