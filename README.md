



# Snortstamper Web UI - Setup Guide

Snortstamper uses a locally-installed AI model to generate timestamps for any length of youtube transcripts.

## Installation Steps

### 1. Prerequisites
Ensure you have:
- Python 3.8+
- [Ollama installed](https://ollama.com/download)
- Ollama running with Mistral model: `ollama pull mistral`

- Get the transcript

VidIQ broke/disabled the transcript+timestamp download using their addon, so the current workaround is to manually copypaste the transcript into a txt file. The transcript only needs to have the timecodes, format  doesn't matter.

## Running the Application

### Easiest Way: One-Click Startup (Recommended)

**Windows:**
1. Double-click `Run Snortstamper.ink`
2. Wait for browser to prompt
3. Open `http://localhost:5000`

**macOS/Linux:**
1. Open terminal in the project folder
2. Run: `chmod +x startup.sh && ./startup.sh`
3. Wait for Flask to start
4. Open `http://localhost:5000`

The startup script will:
- Create virtual environment (if needed)
- Activate it
- Check for Ollama and Mistral model
- Start Ollama server
- Start Flask server
- Open the UI

---

### Manual Setup (if you prefer)

**Step 1: Activate Virtual Environment**

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

**Step 2: Start Ollama** (in one terminal)
```bash
ollama serve
```

**Step 3: Start Flask Server** (in another terminal)
```bash
python app.py
```

**Step 4: Open in Browser**
Go to: http://localhost:5000

## Usage

1. Click on the upload area to select your transcript file (`.txt`)
2. The file should contain timestamps in `[M:SS]` or `[H:MM:SS]` format
3. Click "Generate Timestamps"
4. Wait for processing (will print progress in terminal)
5. View the generated chapters in the preview
6. Click "Download Chapters" to save as `youtube_chapters.txt`

## Command-Line Usage (Still Supported)

## Troubleshooting

**Error: "Connection refused" on port 5000**
- Flask server isn't running. Run `python app.py`

**Error: "Could not connect to Ollama"**
- Ollama isn't running. Run `ollama serve` in another terminal
- Make sure Mistral is pulled: `ollama pull mistral`

**Error: "No transcript file provided"**
- Make sure you selected a `.txt` file before clicking Generate

**Long processing time**
- This is normal! LLM processing takes time. Check the terminal for progress logs.

