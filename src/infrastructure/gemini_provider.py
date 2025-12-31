"""Gemini summarization provider implementation."""
import os
from typing import Optional
from ..core.interfaces.summarization_provider import ISummarizationProvider
from ..core.models.summary import Summary
from ..core.models.app_result import AppResult


class GeminiSummarizationProvider(ISummarizationProvider):
    """Implementation of summarization provider using Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the provider.
        
        Args:
            api_key: Gemini API key. If None, will try to load from GEMINI_API_KEY env variable
        """
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._client = None
    
    def _initialize_model(self):
        """Initialize the Gemini client (lazy loading)."""
        if self._client is not None:
            return AppResult.ok(None)
        
        if not self._api_key:
            return AppResult.fail(
                "Gemini API key not provided. Set GEMINI_API_KEY environment variable or pass api_key parameter",
                errors=["Missing API key"]
            )
        
        try:
            import google.genai as genai
        except ImportError:
            return AppResult.fail(
                "Google GenAI library is not installed. Please install with: pip install google-genai",
                errors=["Missing dependency: google-genai"]
            )
        
        try:
            self._client = genai.Client(api_key=self._api_key)
            return AppResult.ok(None)
        except Exception as e:
            return AppResult.fail(
                f"Failed to initialize Gemini client: {str(e)}",
                errors=[str(e)]
            )
    
    def summarize(self, text: str) -> AppResult[Summary]:
        """
        Generate a summary and action items from text using Gemini.
        
        Args:
            text: The text to summarize
            
        Returns:
            AppResult containing Summary or error details
        """
        try:
            # Initialize client if needed
            init_result = self._initialize_model()
            if not init_result.success:
                return init_result
            
            # Create prompt for Gemini
            prompt = f"""
Analyze the following transcription and provide:
1. A concise summary of the conversation (2-3 paragraphs)
2. A list of action items (specific tasks mentioned or implied)

Format your response exactly as follows:
SUMMARY:
[Your summary here]

ACTION ITEMS:
- [Action item 1]
- [Action item 2]
- [etc.]

If there are no action items, write "- None identified"

Transcription:
{text}
"""
            
            # Generate response using the client
            response = self._client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            if not response or not response.text:
                return AppResult.fail("Gemini API returned empty response")
            
            # Parse response
            response_text = response.text.strip()
            
            # Extract summary and action items
            summary_text = ""
            action_items = []
            
            if "SUMMARY:" in response_text and "ACTION ITEMS:" in response_text:
                parts = response_text.split("ACTION ITEMS:")
                summary_part = parts[0].replace("SUMMARY:", "").strip()
                action_part = parts[1].strip()
                
                summary_text = summary_part
                
                # Parse action items
                for line in action_part.split("\n"):
                    line = line.strip()
                    if line.startswith("-") or line.startswith("*"):
                        item = line[1:].strip()
                        if item and item.lower() != "none identified":
                            action_items.append(item)
            else:
                # Fallback: use entire response as summary
                summary_text = response_text
            
            if not summary_text:
                return AppResult.fail("Failed to extract summary from Gemini response")
            
            summary = Summary(
                conversation_summary=summary_text,
                action_items=action_items
            )
            
            return AppResult.ok(summary, "Summary generated successfully")
            
        except Exception as e:
            return AppResult.fail(
                f"Summarization failed: {str(e)}",
                errors=[str(e)]
            )
