# Snortstamper Web UI - Setup Guide

## File Structure

Create this folder structure in your project:

```
snortstamper-web/
├── venv/                      (created after step 2)
├── app.py
├── snortstamper_core.py
├── requirements.txt
├── index.html
├── transcript.txt (example, for CLI testing)
└── youtube_chapters.txt (generated output)
```

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

### 3. Files to Add/Replace

**Add these NEW files:**
- `app.py` - Flask web server
- `snortstamper_core.py` - Core logic (unchanged from original)
- `requirements.txt` - Python dependencies
- `index.html` - Web UI frontend

**Keep (unchanged):**
- `transcript.txt` - Your transcript file (for testing)

**You can remove:**
- The old `snortstamper.py` - functionality is split into `snortstamper_core.py` and `app.py`

## Running the Application

### 1. Activate Virtual Environment (do this first!)

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal.

### 2. Start Ollama (in one terminal)
```bash
ollama serve
```

### 3. Start Flask Server (in another terminal, with venv activated)
```bash
python app.py
```

The server will run at `http://localhost:5000`

### 4. Access the Web UI
Open your browser to: **http://localhost:5000**

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

## Changes from Original Script

✓ **Business logic unchanged** - All chapter generation code is identical
✓ **Modular structure** - Core logic separated from web server
✓ **API endpoint** - Added Flask endpoint for web requests
✓ **Frontend** - Added React UI with file upload and download
✓ **CLI still works** - Can still use `ChapterGenerator` class directly

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