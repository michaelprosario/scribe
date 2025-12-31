#!/usr/bin/env python3
"""Main CLI entry point for Scribe - MP3 transcription and summarization tool."""
import argparse
import sys
import os
from dotenv import load_dotenv

from src.core.services.audio_processing_service import AudioProcessingService
from src.core.models.commands import ProcessAudioFileCommand
from src.infrastructure.whisper_provider import WhisperTranscriptionProvider
from src.infrastructure.gemini_provider import GeminiSummarizationProvider
from src.infrastructure.output_formatter import OutputFormatter


def main():
    """Main CLI entry point."""
    # Load environment variables
    load_dotenv()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Scribe - Transcribe and summarize audio files using Whisper and Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s recording.mp3
  %(prog)s recording.mp3 --model small
  %(prog)s recording.mp3 --output results.txt
  %(prog)s recording.mp3 --no-summary
  %(prog)s recording.mp3 --output results.json --model medium
        """
    )
    
    parser.add_argument(
        "audio_file",
        help="Path to the MP3/audio file to transcribe"
    )
    
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Whisper model size (default: base)"
    )
    
    parser.add_argument(
        "--output",
        help="Save output to file (format determined by extension: .txt, .json, .md)"
    )
    
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Skip Gemini summary generation (transcription only)"
    )
    
    args = parser.parse_args()
    
    # Validate audio file exists
    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize providers (Infrastructure layer)
    print("Initializing transcription and summarization providers...")
    transcription_provider = WhisperTranscriptionProvider()
    summarization_provider = GeminiSummarizationProvider()
    
    # Initialize service (Core layer)
    audio_service = AudioProcessingService(
        transcription_provider=transcription_provider,
        summarization_provider=summarization_provider
    )
    
    # Create command
    command = ProcessAudioFileCommand(
        audio_file_path=args.audio_file,
        model=args.model,
        skip_summary=args.no_summary
    )
    
    # Process audio file
    print(f"Processing audio file: {args.audio_file}")
    print(f"Using Whisper model: {args.model}")
    if args.no_summary:
        print("Summary generation: SKIPPED")
    else:
        print("Summary generation: ENABLED")
    print("")
    
    result = audio_service.process_audio_file(command)
    
    # Check result
    if not result.success:
        print(f"Error: {result.message}", file=sys.stderr)
        if result.errors:
            print("Details:", file=sys.stderr)
            for error in result.errors:
                print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    
    # Extract results
    transcription, summary = result.value
    
    # Display results to console
    print(OutputFormatter.format_console_output(transcription, summary))
    
    # Save to file if requested
    if args.output:
        try:
            ext = os.path.splitext(args.output)[1].lower()
            if ext == ".json":
                OutputFormatter.save_to_json(transcription, summary, args.output)
            elif ext == ".md":
                OutputFormatter.save_to_markdown(transcription, summary, args.output)
            else:
                # Default to txt
                OutputFormatter.save_to_txt(transcription, summary, args.output)
            
            print(f"\nResults saved to: {args.output}")
        except Exception as e:
            print(f"Warning: Failed to save output file: {e}", file=sys.stderr)
    
    print("\nProcessing completed successfully!")


if __name__ == "__main__":
    main()
