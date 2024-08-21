# from flask import Blueprint, request, jsonify
# import os
# import logging
# import requests
# import google.generativeai as genai

# # # Blueprint for audio routes
# audio_bp = Blueprint('audio_bp', __name__)

# # # Load environment variables
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# --------------------------------------------------------------------------------------------------------------------
# storing the file in memory
# --------------------------------------------------------------------------------------------------------------------

# def extract_transcript(audio_file_path):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     audio = genai.upload_file(path=audio_file_path)
#     response = model.generate_content(['extract well structured transcript from audio', audio])
#     return response.text

# @audio_bp.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'file' in request.files:
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
#         file_type = file.filename.rsplit('.', 1)[-1].lower()
#         if file_type not in ['wav', 'mp3', 'flac']:
#             return jsonify({'error': 'Unsupported audio format'}), 400
#         audio_path = f"/tmp/{file.filename}"
#         file.save(audio_path)
#     elif 'url' in request.json:
#         url = request.json['url']
#         if not url:
#             return jsonify({'error': 'No URL provided'}), 400
#         try:
#             response = requests.get(url, stream=True)
#             response.raise_for_status()
#             content_type = response.headers.get('Content-Type', '')
#             if 'audio' not in content_type:
#                 return jsonify({'error': 'Unsupported audio format from URL'}), 400
#             audio_path = f"/tmp/{url.split('/')[-1]}"
#             with open(audio_path, 'wb') as f:
#                 f.write(response.content)
#         except requests.RequestException as e:
#             logging.error(f"Error fetching audio from URL: {e}")
#             return jsonify({'error': 'Error fetching audio from URL'}), 500
#     else:
#         return jsonify({'error': 'No file or URL provided'}), 400

#     try:
#         transcript = extract_transcript(audio_path)
#         return jsonify({'transcript': transcript})
#     except Exception as e:
#         logging.error(f"An error occurred during transcript extraction: {e}")
#         return jsonify({'error': str(e)}), 500


# --------------------------------------------------------------------------------------------------------------------
# without url
# --------------------------------------------------------------------------------------------------------------------


# from flask import Blueprint, request, jsonify
# import os
# import logging
# import google.generativeai as genai

# # Blueprint for audio routes
# audio_bp = Blueprint('audio_bp', __name__)

# # Load environment variables
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# # Function to extract transcript
# def extract_transcript(audio_file_path):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     audio = genai.upload_file(path=audio_file_path)
#     response = model.generate_content(['extract well structured transcript from audio', audio])
#     return response.text

# @audio_bp.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'file' in request.files:
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
#         file_type = file.filename.rsplit('.', 1)[-1].lower()
#         if file_type not in ['wav', 'mp3', 'flac']:
#             return jsonify({'error': 'Unsupported audio format'}), 400
#         audio_path = f"/tmp/{file.filename}"
#         file.save(audio_path)
#     else:
#         return jsonify({'error': 'No file provided'}), 400

#     try:
#         transcript = extract_transcript(audio_path)
#         return jsonify({'transcript': transcript})
#     except Exception as e:
#         logging.error(f"An error occurred during transcript extraction: {e}")
#         return jsonify({'error': str(e)}), 500


# --------------------------------------------------------------------------------------------------------------------
# read in bytes
# --------------------------------------------------------------------------------------------------------------------



# from flask import Blueprint, request, jsonify
# import os
# import logging
# import google.generativeai as genai
# from io import BytesIO
# import base64

# # Blueprint for audio routes
# audio_bp = Blueprint('audio_bp', __name__)

# # Load environment variables
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# # Function to extract transcript
# def extract_transcript(audio_bytes, mime_type):
#     model = genai.GenerativeModel('models/gemini-1.5-flash')
#     response = model.generate_content([
#         "Please summarize the audio.",
#         {
#             "mime_type": mime_type,
#             "data": audio_bytes
#         }
#     ])
#     return response.text

# @audio_bp.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     file_type = file.filename.rsplit('.', 1)[-1].lower()
#     mime_type = f"audio/{file_type}"
#     if file_type not in ['wav', 'mp3', 'flac']:
#         return jsonify({'error': 'Unsupported audio format'}), 400

#     # Read file bytes
#     audio_bytes = file.read()

#     # Print the first 100 bytes of the audio data in base64 for readability
#     # print("Audio bytes :", audio_bytes[:1000])
#     print("Type of audio_bytes:", type(audio_bytes))
#     print("Total bytes:", len(audio_bytes))

#     # Extract the transcript
#     try:
#         transcript = extract_transcript(audio_bytes, mime_type)
#         return jsonify({'transcript': transcript})
#     except Exception as e:
#         logging.error(f"An error occurred during transcript extraction: {e}")
#         return jsonify({'error': str(e)}), 500



# --------------------------------------------------------------------------------------------------------------------
# read in buffer
# --------------------------------------------------------------------------------------------------------------------


from flask import Blueprint, request, jsonify
import os
import logging
import google.generativeai as genai
from io import BytesIO

# Blueprint for audio routes
audio_bp = Blueprint('audio_bp', __name__)

# Load environment variables
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to extract transcript
def extract_transcript(audio_buffer, mime_type):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([
        "extract transcript from audio",
        {
            "mime_type": mime_type,
            "data": audio_buffer.read()
        }
    ])
    # Check if the response contains valid content
    if not response or not hasattr(response, 'text') or not response.text:
        logging.error(f"Invalid response: {response}")
        raise ValueError("Invalid operation: The response does not contain valid text data.")
    return response.text

@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_type = file.filename.rsplit('.', 1)[-1].lower()
    mime_type = f"audio/{file_type}"
    if file_type not in ['wav', 'mp3', 'flac']:
        return jsonify({'error': 'Unsupported audio format'}), 400

    # Read file bytes
    audio_bytes = file.read()

    # Convert audio bytes to BytesIO buffer
    audio_buffer = BytesIO(audio_bytes)

    # Print buffer information
    print("Audio bytes (first 1000):", audio_bytes[:1000])
    print("Type of audio_bytes:", type(audio_bytes))
    print("Total bytes:", len(audio_bytes))
    print("Buffer type:", type(audio_buffer))
    print("Buffer size:", audio_buffer.getbuffer().nbytes)

    # Extract the transcript
    try:
        # Reset the buffer position to the beginning before passing it to the function
        audio_buffer.seek(0)
        transcript = extract_transcript(audio_buffer, mime_type)
        return jsonify({'transcript': transcript})
    except Exception as e:
        logging.error(f"An error occurred during transcript extraction: {e}")
        return jsonify({'error': str(e)}), 500



# from flask import Blueprint, request, jsonify
# import os
# import logging
# import google.generativeai as genai
# from io import BytesIO

# # Blueprint for audio routes
# audio_bp = Blueprint('audio_bp', __name__)

# # Load environment variables
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# # Function to extract transcript
# def extract_transcript(audio_buffer, mime_type):
#     model = genai.GenerativeModel('models/gemini-1.5-flash')
#     response = model.generate_content([
#         "extract transcript from audio",
#         {
#             "mime_type": mime_type,
#             "data": audio_buffer.read()
#         }
#     ])
#     if not response or not hasattr(response, 'text') or not response.text:
#         logging.error(f"Invalid response: {response}")
#         raise ValueError("Invalid operation: The response does not contain valid text data.")
#     return response.text

# @audio_bp.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     file_type = file.filename.rsplit('.', 1)[-1].lower()
#     mime_type = f"audio/{file_type}"
#     if file_type not in ['wav', 'mp3', 'flac']:
#         return jsonify({'error': 'Unsupported audio format'}), 400

#     # Limit file size (e.g., 10 MB)
#     if len(file.read()) > 10 * 1024 * 1024:
#         return jsonify({'error': 'File size exceeds limit'}), 400
    
#     # Rewind file pointer to start
#     file.seek(0)
#     audio_bytes = file.read()

#     # Convert audio bytes to BytesIO buffer
#     audio_buffer = BytesIO(audio_bytes)

#     try:
#         # Reset the buffer position to the beginning before passing it to the function
#         audio_buffer.seek(0)
#         transcript = extract_transcript(audio_buffer, mime_type)
#         return jsonify({'transcript': transcript})
#     except Exception as e:
#         logging.error(f"An error occurred during transcript extraction: {e}")
#         return jsonify({'error': str(e)}), 500
