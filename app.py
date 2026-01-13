from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from snortstamper_core import ChapterGenerator
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_file('index.html')

@app.route('/api/generate-timestamps', methods=['POST'])
def generate_timestamps():
    if 'transcript' not in request.files:
        return jsonify({'error': 'No transcript file provided'}), 400
    
    file = request.files['transcript']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.txt'):
        return jsonify({'error': 'Please upload a .txt file'}), 400
    
    try:
        # Read the transcript content
        transcript_text = file.read().decode('utf-8')
        
        if not transcript_text.strip():
            return jsonify({'error': 'Transcript file is empty'}), 400
        
        # Generate chapters using the ChapterGenerator
        generator = ChapterGenerator(model="mistral")
        chapters = generator.generate_chapters(transcript_text)
        formatted = generator.format_chapters(chapters)
        
        return jsonify({'timestamps': formatted})
    
    except Exception as e:
        return jsonify({'error': f'Error generating timestamps: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)