"""Core interfaces module."""
from .transcription_provider import ITranscriptionProvider
from .summarization_provider import ISummarizationProvider

__all__ = ['ITranscriptionProvider', 'ISummarizationProvider']
