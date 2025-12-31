"""Unit tests for AudioProcessingService."""
import unittest
from unittest.mock import Mock
from src.core.services.audio_processing_service import AudioProcessingService
from src.core.models.commands import ProcessAudioFileCommand, GenerateSummaryCommand
from src.core.models.transcription import Transcription
from src.core.models.summary import Summary
from src.core.models.app_result import AppResult


class TestAudioProcessingService(unittest.TestCase):
    """Test cases for AudioProcessingService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_transcription_provider = Mock()
        self.mock_summarization_provider = Mock()
        self.service = AudioProcessingService(
            self.mock_transcription_provider,
            self.mock_summarization_provider
        )
    
    def test_process_audio_file_success(self):
        """Test successful audio processing."""
        # Arrange
        command = ProcessAudioFileCommand(
            audio_file_path="/path/to/audio.mp3",
            model="base",
            skip_summary=False
        )
        
        transcription = Transcription(
            text="Test transcription text",
            audio_file_path="/path/to/audio.mp3",
            model_used="base"
        )
        
        summary = Summary(
            conversation_summary="Test summary",
            action_items=["Action 1", "Action 2"]
        )
        
        self.mock_transcription_provider.transcribe.return_value = AppResult.ok(transcription)
        self.mock_summarization_provider.summarize.return_value = AppResult.ok(summary)
        
        # Act
        result = self.service.process_audio_file(command)
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.value[0].text, "Test transcription text")
        self.assertEqual(result.value[1].conversation_summary, "Test summary")
        self.mock_transcription_provider.transcribe.assert_called_once()
        self.mock_summarization_provider.summarize.assert_called_once()
    
    def test_process_audio_file_skip_summary(self):
        """Test audio processing with summary skipped."""
        # Arrange
        command = ProcessAudioFileCommand(
            audio_file_path="/path/to/audio.mp3",
            model="base",
            skip_summary=True
        )
        
        transcription = Transcription(
            text="Test transcription text",
            audio_file_path="/path/to/audio.mp3",
            model_used="base"
        )
        
        self.mock_transcription_provider.transcribe.return_value = AppResult.ok(transcription)
        
        # Act
        result = self.service.process_audio_file(command)
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.value[0].text, "Test transcription text")
        self.assertEqual(result.value[1].conversation_summary, "Summary skipped by user")
        self.mock_transcription_provider.transcribe.assert_called_once()
        self.mock_summarization_provider.summarize.assert_not_called()
    
    def test_process_audio_file_transcription_fails(self):
        """Test handling of transcription failure."""
        # Arrange
        command = ProcessAudioFileCommand(
            audio_file_path="/path/to/audio.mp3",
            model="base",
            skip_summary=False
        )
        
        self.mock_transcription_provider.transcribe.return_value = AppResult.fail(
            "File not found",
            errors=["Audio file does not exist"]
        )
        
        # Act
        result = self.service.process_audio_file(command)
        
        # Assert
        self.assertFalse(result.success)
        self.assertIn("Transcription failed", result.message)
        self.mock_summarization_provider.summarize.assert_not_called()
    
    def test_process_audio_file_summarization_fails(self):
        """Test handling of summarization failure."""
        # Arrange
        command = ProcessAudioFileCommand(
            audio_file_path="/path/to/audio.mp3",
            model="base",
            skip_summary=False
        )
        
        transcription = Transcription(
            text="Test transcription text",
            audio_file_path="/path/to/audio.mp3",
            model_used="base"
        )
        
        self.mock_transcription_provider.transcribe.return_value = AppResult.ok(transcription)
        self.mock_summarization_provider.summarize.return_value = AppResult.fail(
            "API error",
            errors=["Invalid API key"]
        )
        
        # Act
        result = self.service.process_audio_file(command)
        
        # Assert
        self.assertFalse(result.success)
        self.assertIn("Summarization failed", result.message)
    
    def test_process_audio_file_validation_error(self):
        """Test validation error for invalid command."""
        # Arrange
        command = ProcessAudioFileCommand(
            audio_file_path="",
            model="base",
            skip_summary=False
        )
        
        # Act
        result = self.service.process_audio_file(command)
        
        # Assert
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Validation failed")
        self.assertIn("Audio file path is required", result.errors)
        self.mock_transcription_provider.transcribe.assert_not_called()
    
    def test_generate_summary_success(self):
        """Test successful summary generation."""
        # Arrange
        command = GenerateSummaryCommand(text="Long text to summarize")
        
        summary = Summary(
            conversation_summary="Summary text",
            action_items=["Action 1"]
        )
        
        self.mock_summarization_provider.summarize.return_value = AppResult.ok(summary)
        
        # Act
        result = self.service.generate_summary(command)
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.value.conversation_summary, "Summary text")
        self.mock_summarization_provider.summarize.assert_called_once_with("Long text to summarize")
    
    def test_generate_summary_validation_error_empty_text(self):
        """Test validation error for empty text."""
        # Arrange
        command = GenerateSummaryCommand(text="")
        
        # Act
        result = self.service.generate_summary(command)
        
        # Assert
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Validation failed")
        self.assertIn("Text is required for summarization", result.errors)
        self.mock_summarization_provider.summarize.assert_not_called()


if __name__ == '__main__':
    unittest.main()
