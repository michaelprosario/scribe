"""Transcription domain model."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Transcription:
    """Represents a transcription of an audio file."""
    
    text: str
    audio_file_path: str
    model_used: str
    language: Optional[str] = None
    duration_seconds: Optional[float] = None
    
    def __post_init__(self):
        if not self.text:
            raise ValueError("Transcription text cannot be empty")
        if not self.audio_file_path:
            raise ValueError("Audio file path cannot be empty")
