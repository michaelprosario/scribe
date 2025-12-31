# Developer Quick Start Guide

## Running the Application

### Basic Usage
```bash
python transcriber.py audio.mp3
```

### With Options
```bash
# Use small model
python transcriber.py audio.mp3 --model small

# Skip summary
python transcriber.py audio.mp3 --no-summary

# Save to file
python transcriber.py audio.mp3 --output results.json
```

## Development Setup

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y ffmpeg

# macOS
brew install ffmpeg
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_audio_processing_service.py -v
```

## Project Structure

```
src/
├── core/                           # Business logic (testable, no external deps)
│   ├── models/                    # Domain models
│   │   ├── app_result.py         # Result pattern
│   │   ├── commands.py           # Command/Query objects
│   │   ├── transcription.py      # Transcription model
│   │   └── summary.py            # Summary model
│   ├── interfaces/                # Abstractions
│   │   ├── transcription_provider.py
│   │   └── summarization_provider.py
│   └── services/                  # Business logic
│       ├── transcription_service.py
│       └── audio_processing_service.py
└── infrastructure/                 # External implementations
    ├── whisper_provider.py        # Whisper implementation
    ├── gemini_provider.py         # Gemini implementation
    └── output_formatter.py        # Output formatting
```

## Adding a New Feature

### 1. Define the Command (Core)
```python
# src/core/models/commands.py
@dataclass
class YourNewCommand:
    param: str
    
    def validate(self) -> list[str]:
        errors = []
        # Validation logic
        return errors
```

### 2. Add Service Method (Core)
```python
# src/core/services/your_service.py
def your_method(self, command: YourNewCommand) -> AppResult[YourModel]:
    # Validate
    validation_errors = command.validate()
    if validation_errors:
        return AppResult.validation_error(validation_errors)
    
    # Business logic
    result = self._provider.do_something(command.param)
    
    if not result.success:
        return AppResult.fail(result.message, result.errors)
    
    return AppResult.ok(result.value)
```

### 3. Write Tests (Tests)
```python
# tests/test_your_service.py
def test_your_method_success(self):
    # Arrange
    command = YourNewCommand(param="test")
    self.mock_provider.do_something.return_value = AppResult.ok("result")
    
    # Act
    result = self.service.your_method(command)
    
    # Assert
    self.assertTrue(result.success)
```

### 4. Implement Provider (Infrastructure)
```python
# src/infrastructure/your_provider.py
class YourProvider(IYourInterface):
    def do_something(self, param: str) -> AppResult[str]:
        try:
            # Implementation using external library
            return AppResult.ok(result)
        except Exception as e:
            return AppResult.fail(str(e))
```

## Clean Architecture Rules

✅ **DO**: 
- Keep Core independent of Infrastructure
- Use interfaces in Core, implementations in Infrastructure
- Use Command/Query objects for service inputs
- Return AppResult from all service methods
- Write unit tests for Core services

❌ **DON'T**:
- Import Infrastructure modules in Core
- Put business logic in CLI or Infrastructure
- Use concrete classes in Core service constructors
- Return raw values or throw exceptions from services
- Skip validation in commands

## Common Tasks

### Add a New Provider Interface
1. Create interface in `src/core/interfaces/`
2. Implement in `src/infrastructure/`
3. Inject via service constructor

### Add a New Model
1. Create in `src/core/models/`
2. Use dataclasses
3. Add validation in `__post_init__`

### Add Output Format
1. Add method to `OutputFormatter` class
2. Update CLI argument parser
3. Add file extension handling in `transcriber.py`

## Debugging

### Check Imports
```bash
python -c "from src.core.models.app_result import AppResult; print('OK')"
```

### Verify Provider
```python
from src.infrastructure.whisper_provider import WhisperTranscriptionProvider
provider = WhisperTranscriptionProvider()
result = provider.transcribe("test.mp3", model="tiny")
print(result.success, result.message)
```

### Test Command Validation
```python
from src.core.models.commands import TranscribeAudioCommand
cmd = TranscribeAudioCommand(audio_file_path="", model="invalid")
errors = cmd.validate()
print(errors)
```

## Performance Tips

### Whisper Model Selection
- `tiny`: Fast, less accurate
- `base`: **Recommended** - Good balance
- `small`: Better accuracy, slower
- `medium`: High accuracy, much slower
- `large`: Best accuracy, very slow

### Optimization
- Model is cached after first load
- Use GPU if available (automatic)
- Process multiple files in batch
- Consider skip-summary for faster processing

## Troubleshooting

### "No module named whisper"
```bash
pip install openai-whisper
```

### "No module named google.generativeai"
```bash
pip install google-generativeai
```

### "Gemini API key not provided"
Check `.env` file has:
```
GEMINI_API_KEY=your_actual_key_here
```

### "Audio file not found"
Use absolute path or verify file exists:
```bash
ls -l audio.mp3
python transcriber.py $(pwd)/audio.mp3
```
