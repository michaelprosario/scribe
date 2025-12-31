"""Command and Query objects for core services."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TranscribeAudioCommand:
    """Command to transcribe an audio file."""
    
    audio_file_path: str
    model: Optional[str] = "base"
    
    def validate(self) -> list[str]:
        """Validate the command."""
        errors = []
        if not self.audio_file_path:
            errors.append("Audio file path is required")
        if self.model not in ["tiny", "base", "small", "medium", "large", None]:
            errors.append(f"Invalid model: {self.model}. Must be one of: tiny, base, small, medium, large")
        return errors


@dataclass
class GenerateSummaryCommand:
    """Command to generate a summary from text."""
    
    text: str
    
    def validate(self) -> list[str]:
        """Validate the command."""
        errors = []
        if not self.text or not self.text.strip():
            errors.append("Text is required for summarization")
        return errors


@dataclass
class ProcessAudioFileCommand:
    """Command to process an audio file (transcribe and summarize)."""
    
    audio_file_path: str
    model: Optional[str] = "base"
    skip_summary: bool = False
    
    def validate(self) -> list[str]:
        """Validate the command."""
        errors = []
        if not self.audio_file_path:
            errors.append("Audio file path is required")
        if self.model not in ["tiny", "base", "small", "medium", "large", None]:
            errors.append(f"Invalid model: {self.model}. Must be one of: tiny, base, small, medium, large")
        return errors
