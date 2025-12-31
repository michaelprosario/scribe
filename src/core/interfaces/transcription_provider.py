"""Transcription provider interface."""
from abc import ABC, abstractmethod
from typing import Optional
from ..models.transcription import Transcription
from ..models.app_result import AppResult


class ITranscriptionProvider(ABC):
    """Interface for audio transcription providers."""
    
    @abstractmethod
    def transcribe(self, audio_file_path: str, model: Optional[str] = None) -> AppResult[Transcription]:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_file_path: Path to the audio file
            model: Optional model specification
            
        Returns:
            AppResult containing Transcription or error details
        """
        pass
