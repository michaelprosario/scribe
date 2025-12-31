# Scribe - MP3 Transcription & Summary CLI Tool

A clean architecture CLI application that transcribes audio files using OpenAI Whisper (local processing) and generates summaries with action items using Google Gemini API.

## Features

- 🎙️ **Local Transcription**: Uses OpenAI Whisper for 100% free, local audio transcription
- 🤖 **AI Summarization**: Leverages Google Gemini API to generate conversation summaries and extract action items
- 🏗️ **Clean Architecture**: Follows Ardalis clean architecture principles with clear separation of concerns
- ✅ **Testable Core**: Business logic is fully tested and independent of infrastructure
- 📊 **Multiple Output Formats**: Save results as TXT, JSON, or Markdown
- ⚙️ **Flexible Models**: Choose from 5 Whisper model sizes (tiny to large)

## Architecture

This project follows **Clean Architecture** principles as advocated by Steve Smith (Ardalis):

```
src/
├── core/                    # Core business logic (no external dependencies)
│   ├── models/             # Domain models, commands, queries, AppResult
│   ├── interfaces/         # Provider interfaces (abstractions)
│   └── services/           # Business logic services
└── infrastructure/          # Implementation details
    ├── whisper_provider.py  # Whisper transcription implementation
    ├── gemini_provider.py   # Gemini summarization implementation
    └── output_formatter.py  # Output formatting utilities
```

### Key Architecture Principles

1. ✅ **Dependency Rule**: Dependencies point inward towards Core
2. ✅ **Core Independence**: Core has minimal dependencies, no direct infrastructure references
3. ✅ **Interface Definitions**: Core defines interfaces, Infrastructure implements them
4. ✅ **Command/Query Pattern**: Services use command objects as inputs
5. ✅ **AppResult Pattern**: Services return consistent result objects with success/failure info
6. ✅ **Testability**: Core services are fully unit tested without infrastructure dependencies

## Installation

### Prerequisites

- Python 3.8 or higher
- pip
- (Optional) GPU for faster transcription

### Setup

1. Clone the repository:
```bash
git clone https://github.com/michaelprosario/scribe.git
cd scribe
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

4. Get your Gemini API key from: https://makersuite.google.com/app/apikey

## Usage

### Basic Usage

Transcribe and summarize an audio file:
```bash
python transcriber.py recording.mp3
```

### Advanced Usage

Choose a different Whisper model:
```bash
python transcriber.py recording.mp3 --model small
```

Skip summarization (transcription only):
```bash
python transcriber.py recording.mp3 --no-summary
```

Save output to a file:
```bash
# Text format
python transcriber.py recording.mp3 --output results.txt

# JSON format
python transcriber.py recording.mp3 --output results.json

# Markdown format
python transcriber.py recording.mp3 --output results.md
```

### Whisper Model Options

| Model | Size | Speed | Accuracy | RAM Required |
|-------|------|-------|----------|--------------|
| tiny  | ~75MB | Fastest | Lowest | ~1GB |
| base  | ~140MB | Fast | Good | ~1GB |
| small | ~460MB | Medium | Better | ~2GB |
| medium | ~1.5GB | Slow | High | ~5GB |
| large | ~3GB | Slowest | Best | ~10GB |

**Recommendation**: Start with `base` for a good balance of speed and accuracy.

## Testing

Run all unit tests:
```bash
python -m pytest tests/
```

Run tests with coverage:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

The core business logic has comprehensive unit tests that run without external dependencies.

## Project Structure

```
scribe/
├── src/
│   ├── core/                       # Core business logic
│   │   ├── models/                 # Domain models
│   │   │   ├── app_result.py      # Result object pattern
│   │   │   ├── commands.py        # Command/Query objects
│   │   │   ├── transcription.py   # Transcription model
│   │   │   └── summary.py         # Summary model
│   │   ├── interfaces/             # Provider interfaces
│   │   │   ├── transcription_provider.py
│   │   │   └── summarization_provider.py
│   │   └── services/               # Business logic services
│   │       ├── transcription_service.py
│   │       └── audio_processing_service.py
│   └── infrastructure/             # Implementation details
│       ├── whisper_provider.py     # Whisper implementation
│       ├── gemini_provider.py      # Gemini implementation
│       └── output_formatter.py     # Output formatting
├── tests/                          # Unit tests
│   ├── test_app_result.py
│   ├── test_transcription_service.py
│   └── test_audio_processing_service.py
├── prompt/                         # Architecture documentation
│   ├── 001-cleanArchitecture
│   └── 002-baseRequirements
├── transcriber.py                  # CLI entry point
├── requirements.txt                # Dependencies
├── .env.example                    # Environment variables template
├── .gitignore
└── README.md
```

## Cost & Performance

### Transcription (Whisper)
- **Cost**: 100% FREE (runs locally)
- **First run**: Downloads model (~100MB-3GB depending on size)
- **Processing time**: 
  - `base` model: ~1x real-time (10min audio = ~10min processing on CPU)
  - Faster with GPU if available

### Summarization (Gemini)
- **Cost**: Free tier available (60 requests/minute)
- **Processing time**: Usually < 5 seconds

## Contributing

Contributions are welcome! This project follows clean architecture principles, so please ensure:

1. Core business logic remains independent of infrastructure
2. New services use command/query objects as inputs
3. Services return AppResult objects
4. Add unit tests for all core services
5. Infrastructure implementations follow defined interfaces

## License

MIT License - See LICENSE file for details

## Acknowledgments

- OpenAI Whisper for excellent local transcription
- Google Gemini for powerful AI summarization
- Steve Smith (Ardalis) for clean architecture guidance
CLI tool to transcribe mp3
