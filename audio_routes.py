from flask import Blueprint, request, jsonify
import os
import logging
import requests
import google.generativeai as genai

# Blueprint for audio routes
audio_bp = Blueprint('audio_bp', __name__)

# Load environment variables
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_transcript(audio_file_path):
    model = genai.GenerativeModel('gemini-1.5-flash')
    audio = genai.upload_file(path=audio_file_path)
    response = model.generate_content(['extract well structured transcript from audio', audio])
    return response.text

@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        file_type = file.filename.rsplit('.', 1)[-1].lower()
        if file_type not in ['wav', 'mp3', 'flac']:
            return jsonify({'error': 'Unsupported audio format'}), 400
        audio_path = f"/tmp/{file.filename}"
        file.save(audio_path)
    elif 'url' in request.json:
        url = request.json['url']
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            if 'audio' not in content_type:
                return jsonify({'error': 'Unsupported audio format from URL'}), 400
            audio_path = f"/tmp/{url.split('/')[-1]}"
            with open(audio_path, 'wb') as f:
                f.write(response.content)
        except requests.RequestException as e:
            logging.error(f"Error fetching audio from URL: {e}")
            return jsonify({'error': 'Error fetching audio from URL'}), 500
    else:
        return jsonify({'error': 'No file or URL provided'}), 400

    try:
        transcript = extract_transcript(audio_path)
        return jsonify({'transcript': transcript})
    except Exception as e:
        logging.error(f"An error occurred during transcript extraction: {e}")
        return jsonify({'error': str(e)}), 500
