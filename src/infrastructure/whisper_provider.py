"""Whisper transcription provider implementation."""
import os
from typing import Optional
from ..core.interfaces.transcription_provider import ITranscriptionProvider
from ..core.models.transcription import Transcription
from ..core.models.app_result import AppResult


class WhisperTranscriptionProvider(ITranscriptionProvider):
    """Implementation of transcription provider using OpenAI Whisper."""
    
    def __init__(self):
        """Initialize the provider."""
        self._model_cache = {}
    
    def transcribe(self, audio_file_path: str, model: Optional[str] = None) -> AppResult[Transcription]:
        """
        Transcribe an audio file using Whisper.
        
        Args:
            audio_file_path: Path to the audio file
            model: Whisper model size (tiny, base, small, medium, large)
            
        Returns:
            AppResult containing Transcription or error details
        """
        try:
            # Validate file exists
            if not os.path.exists(audio_file_path):
                return AppResult.fail(f"Audio file not found: {audio_file_path}")
            
            # Import whisper only when needed (lazy loading)
            try:
                import whisper
            except ImportError:
                return AppResult.fail(
                    "Whisper is not installed. Please install with: pip install openai-whisper",
                    errors=["Missing dependency: openai-whisper"]
                )
            
            # Default to base model
            model_name = model or "base"
            
            # Load model (cache it for reuse)
            if model_name not in self._model_cache:
                try:
                    self._model_cache[model_name] = whisper.load_model(model_name)
                except Exception as e:
                    return AppResult.fail(
                        f"Failed to load Whisper model '{model_name}': {str(e)}",
                        errors=[str(e)]
                    )
            
            whisper_model = self._model_cache[model_name]
            
            # Perform transcription
            result = whisper_model.transcribe(audio_file_path)
            
            # Create transcription object
            transcription = Transcription(
                text=result["text"].strip(),
                audio_file_path=audio_file_path,
                model_used=model_name,
                language=result.get("language"),
                duration_seconds=None  # Whisper doesn't provide this directly
            )
            
            return AppResult.ok(transcription, "Transcription completed successfully")
            
        except Exception as e:
            return AppResult.fail(
                f"Transcription failed: {str(e)}",
                errors=[str(e)]
            )
