"""Output formatting utilities."""
import json
from typing import Tuple
from ..core.models.transcription import Transcription
from ..core.models.summary import Summary


class OutputFormatter:
    """Formats output for display and file export."""
    
    @staticmethod
    def format_console_output(transcription: Transcription, summary: Summary) -> str:
        """
        Format transcription and summary for console display.
        
        Args:
            transcription: The transcription object
            summary: The summary object
            
        Returns:
            Formatted string for console display
        """
        output = []
        output.append("=" * 80)
        output.append("TRANSCRIPTION RESULTS")
        output.append("=" * 80)
        output.append(f"File: {transcription.audio_file_path}")
        output.append(f"Model: {transcription.model_used}")
        if transcription.language:
            output.append(f"Language: {transcription.language}")
        output.append("")
        output.append("TRANSCRIPTION:")
        output.append("-" * 80)
        output.append(transcription.text)
        output.append("")
        output.append("=" * 80)
        output.append("SUMMARY")
        output.append("=" * 80)
        output.append(summary.conversation_summary)
        output.append("")
        output.append("ACTION ITEMS:")
        output.append("-" * 80)
        if summary.action_items:
            for i, item in enumerate(summary.action_items, 1):
                output.append(f"{i}. {item}")
        else:
            output.append("No action items identified")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    @staticmethod
    def save_to_txt(transcription: Transcription, summary: Summary, output_path: str) -> None:
        """Save results to text file."""
        content = OutputFormatter.format_console_output(transcription, summary)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def save_to_json(transcription: Transcription, summary: Summary, output_path: str) -> None:
        """Save results to JSON file."""
        data = {
            "transcription": {
                "text": transcription.text,
                "audio_file_path": transcription.audio_file_path,
                "model_used": transcription.model_used,
                "language": transcription.language,
                "duration_seconds": transcription.duration_seconds
            },
            "summary": {
                "conversation_summary": summary.conversation_summary,
                "action_items": summary.action_items
            }
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def save_to_markdown(transcription: Transcription, summary: Summary, output_path: str) -> None:
        """Save results to Markdown file."""
        output = []
        output.append("# Transcription Results")
        output.append("")
        output.append("## Metadata")
        output.append(f"- **File:** {transcription.audio_file_path}")
        output.append(f"- **Model:** {transcription.model_used}")
        if transcription.language:
            output.append(f"- **Language:** {transcription.language}")
        output.append("")
        output.append("## Transcription")
        output.append("")
        output.append(transcription.text)
        output.append("")
        output.append("## Summary")
        output.append("")
        output.append(summary.conversation_summary)
        output.append("")
        output.append("## Action Items")
        output.append("")
        if summary.action_items:
            for item in summary.action_items:
                output.append(f"- {item}")
        else:
            output.append("- No action items identified")
        output.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(output))
