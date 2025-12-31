"""Summarization provider interface."""
from abc import ABC, abstractmethod
from ..models.summary import Summary
from ..models.app_result import AppResult


class ISummarizationProvider(ABC):
    """Interface for text summarization providers."""
    
    @abstractmethod
    def summarize(self, text: str) -> AppResult[Summary]:
        """
        Generate a summary and action items from text.
        
        Args:
            text: The text to summarize
            
        Returns:
            AppResult containing Summary or error details
        """
        pass
