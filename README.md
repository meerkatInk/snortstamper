



# Snortstamper Web UI - Setup Guide

Snortstamper uses a locally-installed AI model to generate timestamps for any length of youtube transcripts.

## Installation Steps

### 1. Prerequisites
Ensure you have:
- Python 3.8+
- [Ollama installed](https://ollama.com/download)
- Ollama running with Mistral model: `ollama pull mistral`

- Get the transcript
    - For the correct timestamp format, you need the VidIQ plugin.
https://app.vidiq.com/

- Go to any youtube video
    - Go to the description -> transcript
    - Now you will see the VidIQ plugin button to copy the transcript
    - Press the dropdown button and copy the transcript with timestamps
    - Paste the whole transcript into the transcript.txt file

### 2. Create and Activate Virtual Environment

**On Windows (PowerShell/CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line when activated.

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Easiest Way: One-Click Startup (Recommended)

**Windows:**
1. Double-click `startup.bat`
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
Go to: `http://localhost:5000`

## Usage

1. Click on the upload area to select your transcript file (`.txt`)
2. The file should contain timestamps in `[M:SS]` or `[H:MM:SS]` format
3. Click "Generate Timestamps"
4. Wait for processing (will print progress in terminal)
5. View the generated chapters in the preview
6. Click "Download Chapters" to save as `youtube_chapters.txt`

## Command-Line Usage (Still Supported)

If you want to use the script from the command line without the web UI:

```python
from snortstamper_core import ChapterGenerator
import json

with open('transcript.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

generator = ChapterGenerator(model="mistral")
chapters = generator.generate_chapters(transcript)
formatted = generator.format_chapters(chapters)

print(formatted)

# Optionally save
with open('youtube_chapters.txt', 'w', encoding='utf-8') as f:
    f.write(formatted)

with open('chapters.json', 'w', encoding='utf-8') as f:
    json.dump(chapters, f, indent=2, ensure_ascii=False)
```

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

## API Endpoint

```
POST /api/generate-timestamps

Request:
- Form data with file field named "transcript" (multipart/form-data)

Response:
{
  "timestamps": "[0:00] Chapter Title\n[1:30] Another Chapter\n..."
}

Error Response:
{
  "error": "Error message"
}
```
