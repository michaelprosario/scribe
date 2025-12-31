"""Transcription service - core business logic."""
from ..interfaces.transcription_provider import ITranscriptionProvider
from ..models.commands import TranscribeAudioCommand
from ..models.transcription import Transcription
from ..models.app_result import AppResult


class TranscriptionService:
    """Service for transcribing audio files."""
    
    def __init__(self, transcription_provider: ITranscriptionProvider):
        """
        Initialize the service.
        
        Args:
            transcription_provider: Provider for audio transcription
        """
        self._transcription_provider = transcription_provider
    
    def transcribe_audio(self, command: TranscribeAudioCommand) -> AppResult[Transcription]:
        """
        Transcribe an audio file.
        
        Args:
            command: Command containing transcription parameters
            
        Returns:
            AppResult containing Transcription or error details
        """
        # Validate command
        validation_errors = command.validate()
        if validation_errors:
            return AppResult.validation_error(validation_errors)
        
        # Delegate to provider
        return self._transcription_provider.transcribe(
            audio_file_path=command.audio_file_path,
            model=command.model
        )
