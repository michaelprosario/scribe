"""Application result object for consistent error handling."""
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


@dataclass
class AppResult(Generic[T]):
    """Result object that reports success, failure, messages, and validation errors."""
    
    success: bool
    value: Optional[T] = None
    message: str = ""
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    @staticmethod
    def ok(value: T, message: str = "") -> 'AppResult[T]':
        """Create a successful result."""
        return AppResult(success=True, value=value, message=message)
    
    @staticmethod
    def fail(message: str, errors: List[str] = None) -> 'AppResult[T]':
        """Create a failed result."""
        return AppResult(success=False, message=message, errors=errors or [])
    
    @staticmethod
    def validation_error(errors: List[str]) -> 'AppResult[T]':
        """Create a validation error result."""
        return AppResult(success=False, message="Validation failed", errors=errors)
