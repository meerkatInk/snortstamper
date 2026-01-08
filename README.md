

BEFORE YOU BEGIN:

- Get the transcript
    - For the correct timestamp format, you need the VidIQ plugin.
https://app.vidiq.com/

- Go to any youtube video
    - Go to the description -> transcript
    - Now you will see the VidIQ plugin button to copy the transcript
    - Press the dropdown button and copy the transcript with timestamps
    - Paste the whole transcript into the transcript.txt file


bash# 1. Install Ollama
Windows (PowerShell in VS Code)

Ollama on Windows is installer-based, not curl.

Option A — Recommended

Download installer:
https://ollama.com/download

Run it

Restart VS Code

# 2. Start Ollama (in one terminal)
ollama serve

# 3. Open NEW terminal, pull Mistral model
ollama pull mistral

# 4. Install Python library
pip install ollama

# 5. Set up your project
mkdir youtube-chapters
cd youtube-chapters
# (Save the Python script as snortstamper.py.py)
# (Save your transcript as transcript.txt)

# 6. Run the script
python snortstamper.py transcript.txt