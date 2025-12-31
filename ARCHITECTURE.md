# Scribe Architecture Documentation

## Clean Architecture Compliance

This document demonstrates how Scribe follows the Clean Architecture principles outlined in `prompt/001-cleanArchitecture`.

### ✅ Dependency Rule
**Rule**: Dependencies point inward towards the Core project.

**Implementation**: 
- Core modules (`src/core/`) have NO imports from Infrastructure
- Infrastructure modules (`src/infrastructure/`) import from Core interfaces
- The CLI entry point (`transcriber.py`) depends on both Core and Infrastructure

```python
# Core defines the interface
from src.core.interfaces.transcription_provider import ITranscriptionProvider

# Infrastructure implements it
from src.infrastructure.whisper_provider import WhisperTranscriptionProvider
```

### ✅ Project Structure
**Rule**: Architecture structured in concentric layers: Core (innermost), Infrastructure, and UI/CLI (outermost).

**Implementation**:
```
Core Layer (innermost):
  - src/core/models/        # Domain models
  - src/core/interfaces/    # Abstractions
  - src/core/services/      # Business logic

Infrastructure Layer:
  - src/infrastructure/     # Concrete implementations

UI/CLI Layer (outermost):
  - transcriber.py          # CLI entry point
```

### ✅ Core Independence
**Rule**: Core has minimal dependencies, zero direct dependencies on external frameworks or Infrastructure.

**Implementation**:
- Core only uses standard Python libraries (dataclasses, abc, typing)
- No imports of whisper, google.generativeai, or other external frameworks in Core
- Core defines interfaces; Infrastructure provides implementations

### ✅ Interface Definition
**Rule**: Inner projects define interfaces; outer projects implement them.

**Implementation**:
```python
# Core defines the abstraction
class ITranscriptionProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_file_path: str, model: Optional[str] = None) -> AppResult[Transcription]:
        pass

# Infrastructure implements it
class WhisperTranscriptionProvider(ITranscriptionProvider):
    def transcribe(self, audio_file_path: str, model: Optional[str] = None) -> AppResult[Transcription]:
        # Implementation using Whisper library
```

### ✅ Infrastructure Role
**Rule**: Infrastructure contains all out-of-process concerns (data access, external services, file system).

**Implementation**:
- `whisper_provider.py` - External service (Whisper library)
- `gemini_provider.py` - External API (Google Gemini)
- `output_formatter.py` - File system I/O

### ✅ CLI Role
**Rule**: CLI handles external interaction, routing, serialization, and orchestration. No business logic.

**Implementation**:
- `transcriber.py` only handles:
  - Argument parsing
  - Provider initialization
  - Service orchestration
  - Output display
- All business logic is in Core services

### ✅ Testability
**Rule**: Extreme testability for Core, isolated from infrastructure dependencies.

**Implementation**:
- All Core services have unit tests
- Tests use mocks for infrastructure providers
- No external dependencies required for testing
- Example: `tests/test_audio_processing_service.py`

### ✅ Services Depend on Interfaces
**Rule**: Core business logic services depend on providers and repositories through interfaces.

**Implementation**:
```python
class AudioProcessingService:
    def __init__(
        self,
        transcription_provider: ITranscriptionProvider,  # Interface, not concrete class
        summarization_provider: ISummarizationProvider   # Interface, not concrete class
    ):
        self._transcription_provider = transcription_provider
        self._summarization_provider = summarization_provider
```

### ✅ Command/Query Objects
**Rule**: Core services use command or query objects as method inputs.

**Implementation**:
```python
@dataclass
class ProcessAudioFileCommand:
    audio_file_path: str
    model: Optional[str] = "base"
    skip_summary: bool = False
    
    def validate(self) -> list[str]:
        # Validation logic
        pass

# Service method signature
def process_audio_file(self, command: ProcessAudioFileCommand) -> AppResult[Tuple[Transcription, Summary]]:
    # Implementation
```

### ✅ AppResult Pattern
**Rule**: Services return an app result object that reports success, failure, messages, and validation errors.

**Implementation**:
```python
@dataclass
class AppResult(Generic[T]):
    success: bool
    value: Optional[T] = None
    message: str = ""
    errors: List[str] = None
    
    @staticmethod
    def ok(value: T, message: str = "") -> 'AppResult[T]':
        return AppResult(success=True, value=value, message=message)
    
    @staticmethod
    def fail(message: str, errors: List[str] = None) -> 'AppResult[T]':
        return AppResult(success=False, message=message, errors=errors or [])
```

All service methods return `AppResult[T]`:
```python
def transcribe_audio(self, command: TranscribeAudioCommand) -> AppResult[Transcription]:
    # Returns AppResult.ok() or AppResult.fail()
```

## Feature Requirements Compliance

This section demonstrates compliance with `prompt/002-baseRequirements`.

### ✅ CLI Argument Support
```python
parser.add_argument("audio_file", help="Path to the MP3/audio file")
parser.add_argument("--model", choices=["tiny", "base", "small", "medium", "large"])
parser.add_argument("--output", help="Save output to file")
parser.add_argument("--no-summary", action="store_true")
```

### ✅ Local Whisper Transcription
- Uses `openai-whisper` library
- Completely free, local processing
- Model caching for efficiency
- Supports all 5 model sizes

### ✅ Gemini API Integration
- Uses `google-generativeai` library
- Extracts summaries and action items
- Proper error handling
- API key from environment variables

### ✅ Multiple Output Formats
- Console output
- Text file (.txt)
- JSON file (.json)
- Markdown file (.md)

### ✅ Progress Display
The CLI shows:
- Initialization status
- Processing parameters
- Processing stages
- Results

## Testing Strategy

### Unit Tests Coverage
1. **AppResult Tests** (`test_app_result.py`)
   - Success result creation
   - Failure result creation
   - Validation error handling

2. **TranscriptionService Tests** (`test_transcription_service.py`)
   - Successful transcription
   - Command validation
   - Provider failure handling

3. **AudioProcessingService Tests** (`test_audio_processing_service.py`)
   - Full processing pipeline
   - Skip summary option
   - Transcription failure handling
   - Summarization failure handling
   - Command validation

### Test Independence
All tests use mocks for infrastructure providers, ensuring:
- No external API calls during testing
- No file system dependencies
- Fast test execution
- Predictable results

## Dependency Graph

```
transcriber.py (CLI)
    ↓ depends on
src/core/services/
    ↓ depends on
src/core/interfaces/
    ↑ implemented by
src/infrastructure/
```

This ensures:
- Core is independent
- Infrastructure can be swapped
- Easy to test
- Clear separation of concerns
