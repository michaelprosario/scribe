"""Audio processing service - orchestrates transcription and summarization."""
from typing import Tuple
from ..interfaces.transcription_provider import ITranscriptionProvider
from ..interfaces.summarization_provider import ISummarizationProvider
from ..models.commands import ProcessAudioFileCommand, GenerateSummaryCommand
from ..models.transcription import Transcription
from ..models.summary import Summary
from ..models.app_result import AppResult


class AudioProcessingService:
    """Service for processing audio files (transcription + summarization)."""
    
    def __init__(
        self,
        transcription_provider: ITranscriptionProvider,
        summarization_provider: ISummarizationProvider
    ):
        """
        Initialize the service.
        
        Args:
            transcription_provider: Provider for audio transcription
            summarization_provider: Provider for text summarization
        """
        self._transcription_provider = transcription_provider
        self._summarization_provider = summarization_provider
    
    def process_audio_file(
        self,
        command: ProcessAudioFileCommand
    ) -> AppResult[Tuple[Transcription, Summary]]:
        """
        Process an audio file: transcribe and optionally summarize.
        
        Args:
            command: Command containing processing parameters
            
        Returns:
            AppResult containing tuple of (Transcription, Summary) or error details
        """
        # Validate command
        validation_errors = command.validate()
        if validation_errors:
            return AppResult.validation_error(validation_errors)
        
        # Step 1: Transcribe audio
        transcription_result = self._transcription_provider.transcribe(
            audio_file_path=command.audio_file_path,
            model=command.model
        )
        
        if not transcription_result.success:
            return AppResult.fail(
                f"Transcription failed: {transcription_result.message}",
                errors=transcription_result.errors
            )
        
        transcription = transcription_result.value
        
        # Step 2: Generate summary (if not skipped)
        if command.skip_summary:
            # Return transcription with empty summary
            empty_summary = Summary(
                conversation_summary="Summary skipped by user",
                action_items=[]
            )
            return AppResult.ok(
                (transcription, empty_summary),
                "Transcription completed (summary skipped)"
            )
        
        summary_result = self.generate_summary(
            GenerateSummaryCommand(text=transcription.text)
        )
        
        if not summary_result.success:
            return AppResult.fail(
                f"Summarization failed: {summary_result.message}",
                errors=summary_result.errors
            )
        
        return AppResult.ok(
            (transcription, summary_result.value),
            "Audio processing completed successfully"
        )
    
    def generate_summary(self, command: GenerateSummaryCommand) -> AppResult[Summary]:
        """
        Generate a summary from text.
        
        Args:
            command: Command containing text to summarize
            
        Returns:
            AppResult containing Summary or error details
        """
        # Validate command
        validation_errors = command.validate()
        if validation_errors:
            return AppResult.validation_error(validation_errors)
        
        # Delegate to provider
        return self._summarization_provider.summarize(command.text)
