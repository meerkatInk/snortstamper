@echo off
echo.
echo ========================================
echo   Snortstamper Startup Script
echo ========================================
echo.

REM Check if venv exists, if not create it
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if ollama is installed
where ollama >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Ollama is not installed or not in PATH
    echo Please install Ollama from: https://ollama.com/download
    pause
    exit /b 1
)

REM Check if mistral model exists (try to pull it)
echo Ensuring Mistral model is available...
ollama pull mistral >nul 2>nul

REM Start Ollama in background
echo Starting Ollama server...
start "" ollama serve

REM Give ollama a moment to start
timeout /t 3 /nobreak

REM Start Flask app
echo.
echo ========================================
echo   Starting Flask Server
echo ========================================
echo.
echo Open your browser to: http://localhost:5000
echo.
python app.py

pause