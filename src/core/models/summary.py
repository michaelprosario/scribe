"""Summary domain model."""
from dataclasses import dataclass
from typing import List


@dataclass
class Summary:
    """Represents a summary of a transcription with action items."""
    
    conversation_summary: str
    action_items: List[str]
    
    def __post_init__(self):
        if not self.conversation_summary:
            raise ValueError("Conversation summary cannot be empty")
        if self.action_items is None:
            self.action_items = []
