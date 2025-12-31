#!/bin/bash
# Setup script for Scribe

echo "Setting up Scribe - MP3 Transcription & Summary Tool"
echo "======================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment (optional but recommended)
read -p "Create a virtual environment? (recommended) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file and add your Gemini API key"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Run: python transcriber.py your_audio_file.mp3"
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Remember to activate the virtual environment before running:"
    echo "   source venv/bin/activate"
    echo ""
fi
