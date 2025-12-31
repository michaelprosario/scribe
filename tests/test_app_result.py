"""Unit tests for AppResult model."""
import unittest
from src.core.models.app_result import AppResult


class TestAppResult(unittest.TestCase):
    """Test cases for AppResult."""
    
    def test_ok_creates_successful_result(self):
        """Test creating a successful result."""
        result = AppResult.ok("test value", "Success message")
        
        self.assertTrue(result.success)
        self.assertEqual(result.value, "test value")
        self.assertEqual(result.message, "Success message")
        self.assertEqual(result.errors, [])
    
    def test_fail_creates_failed_result(self):
        """Test creating a failed result."""
        result = AppResult.fail("Error message", errors=["Error 1", "Error 2"])
        
        self.assertFalse(result.success)
        self.assertIsNone(result.value)
        self.assertEqual(result.message, "Error message")
        self.assertEqual(result.errors, ["Error 1", "Error 2"])
    
    def test_validation_error_creates_validation_result(self):
        """Test creating a validation error result."""
        result = AppResult.validation_error(["Validation error 1", "Validation error 2"])
        
        self.assertFalse(result.success)
        self.assertIsNone(result.value)
        self.assertEqual(result.message, "Validation failed")
        self.assertEqual(result.errors, ["Validation error 1", "Validation error 2"])


if __name__ == '__main__':
    unittest.main()
