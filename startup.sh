#!/bin/bash

echo ""
echo "========================================"
echo "   Snortstamper Startup Script"
echo "========================================"
echo ""

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Check if ollama is installed
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "ERROR: Ollama is not installed"
    echo "Please install Ollama from: https://ollama.com/download"
    exit 1
fi

# Check if mistral model exists (try to pull it)
echo "Ensuring Mistral model is available..."
ollama pull mistral > /dev/null 2>&1

# Start Ollama in background
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Give ollama a moment to start
sleep 3

# Start Flask app
echo ""
echo "========================================"
echo "   Starting Flask Server"
echo "========================================"
echo ""
echo "Open your browser to: http://localhost:5000"
echo ""
python app.py

# Cleanup: kill ollama when flask closes
kill $OLLAMA_PID 2>/dev/null || true