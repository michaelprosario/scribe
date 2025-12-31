"""Unit tests for TranscriptionService."""
import unittest
from unittest.mock import Mock
from src.core.services.transcription_service import TranscriptionService
from src.core.models.commands import TranscribeAudioCommand
from src.core.models.transcription import Transcription
from src.core.models.app_result import AppResult


class TestTranscriptionService(unittest.TestCase):
    """Test cases for TranscriptionService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_provider = Mock()
        self.service = TranscriptionService(self.mock_provider)
    
    def test_transcribe_audio_success(self):
        """Test successful transcription."""
        # Arrange
        command = TranscribeAudioCommand(
            audio_file_path="/path/to/audio.mp3",
            model="base"
        )
        
        expected_transcription = Transcription(
            text="Test transcription",
            audio_file_path="/path/to/audio.mp3",
            model_used="base"
        )
        
        self.mock_provider.transcribe.return_value = AppResult.ok(expected_transcription)
        
        # Act
        result = self.service.transcribe_audio(command)
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.value.text, "Test transcription")
        self.mock_provider.transcribe.assert_called_once_with(
            audio_file_path="/path/to/audio.mp3",
            model="base"
        )
    
    def test_transcribe_audio_validation_error_empty_path(self):
        """Test validation error for empty audio path."""
        # Arrange
        command = TranscribeAudioCommand(
            audio_file_path="",
            model="base"
        )
        
        # Act
        result = self.service.transcribe_audio(command)
        
        # Assert
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Validation failed")
        self.assertIn("Audio file path is required", result.errors)
        self.mock_provider.transcribe.assert_not_called()
    
    def test_transcribe_audio_validation_error_invalid_model(self):
        """Test validation error for invalid model."""
        # Arrange
        command = TranscribeAudioCommand(
            audio_file_path="/path/to/audio.mp3",
            model="invalid"
        )
        
        # Act
        result = self.service.transcribe_audio(command)
        
        # Assert
        self.assertFalse(result.success)
        self.assertIn("Invalid model", result.errors[0])
        self.mock_provider.transcribe.assert_not_called()
    
    def test_transcribe_audio_provider_failure(self):
        """Test handling of provider failure."""
        # Arrange
        command = TranscribeAudioCommand(
            audio_file_path="/path/to/audio.mp3",
            model="base"
        )
        
        self.mock_provider.transcribe.return_value = AppResult.fail(
            "Transcription failed",
            errors=["File not found"]
        )
        
        # Act
        result = self.service.transcribe_audio(command)
        
        # Assert
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Transcription failed")
        self.assertIn("File not found", result.errors)


if __name__ == '__main__':
    unittest.main()
