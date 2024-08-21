# from flask import Blueprint, request, jsonify
# import os
# import logging
# import requests
# import google.generativeai as genai
# import time

# # Blueprint for video routes
# video_bp = Blueprint('video_bp', __name__)

# # Load environment variables
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# def get_transcript_from_video(video_path):
#     try:
#         video = genai.upload_file(path=video_path)
        
#         while video.state.name != 'ACTIVE':
#             print('.', end="")
#             time.sleep(10)
#             video = genai.get_file(video.name)
            
#             if video.state.name not in ['processing', 'ACTIVE']:
#                 raise Exception(f"Unexpected video state: {video.state.name}")

#         print('\nVideo uploaded successfully and is in ACTIVE state')

#         model = genai.GenerativeModel('gemini-1.5-flash')
#         prompt = "write transcript of video"
#         response = model.generate_content([prompt, video])
        
#         return response.text

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# @video_bp.route('/upload', methods=['POST'])
# def upload_video():
#     if 'file' in request.files:
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
#         file_type = file.filename.rsplit('.', 1)[-1].lower()
#         if file_type not in ['mp4', 'avi', 'mov']:
#             logging.error(f"Unsupported video format: {file_type}")
#             return jsonify({'error': 'Unsupported video format'}), 400
#         video_path = f"/tmp/{file.filename}"
#         file.save(video_path)
#     elif 'url' in request.json:
#         url = request.json['url']
#         if not url:
#             return jsonify({'error': 'No URL provided'}), 400
#         try:
#             response = requests.get(url, stream=True)
#             response.raise_for_status()
#             content_type = response.headers.get('Content-Type', '')
#             if 'video' not in content_type:
#                 logging.error(f"Unsupported content type from URL: {content_type}")
#                 return jsonify({'error': 'Unsupported video format from URL'}), 400
#             video_path = f"/tmp/{url.split('/')[-1]}"
#             with open(video_path, 'wb') as f:
#                 f.write(response.content)
#         except requests.RequestException as e:
#             logging.error(f"Error fetching video from URL: {e}")
#             return jsonify({'error': 'Error fetching video from URL'}), 500
#     else:
#         return jsonify({'error': 'No file or URL provided'}), 400

#     try:
#         transcript = get_transcript_from_video(video_path)
#         return jsonify({'transcript': transcript})
#     except Exception as e:
#         logging.error(f"An error occurred during transcript extraction: {e}")
#         return jsonify({'error': str(e)}), 500


# ------------------------------------------------------------------------------------------------------------------------
# without url 
# ------------------------------------------------------------------------------------------------------------------------



# from flask import Blueprint, request, jsonify
# import os
# import logging
# import google.generativeai as genai
# import time

# # Blueprint for video routes
# video_bp = Blueprint('video_bp', __name__)

# # Load environment variables
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# def get_transcript_from_video(video_path):
#     try:
#         video = genai.upload_file(path=video_path)
        
#         while video.state.name != 'ACTIVE':
#             print('.', end="")
#             time.sleep(10)
#             video = genai.get_file(video.name)
            
#             if video.state.name not in ['processing', 'ACTIVE']:
#                 raise Exception(f"Unexpected video state: {video.state.name}")

#         print('\nVideo uploaded successfully and is in ACTIVE state')

#         model = genai.GenerativeModel('gemini-1.5-flash')
#         prompt = "write transcript of video"
#         response = model.generate_content([prompt, video])
        
#         return response.text

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# @video_bp.route('/upload', methods=['POST'])
# def upload_video():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     file_type = file.filename.rsplit('.', 1)[-1].lower()
#     if file_type not in ['mp4', 'avi', 'mov']:
#         logging.error(f"Unsupported video format: {file_type}")
#         return jsonify({'error': 'Unsupported video format'}), 400

#     video_path = f"/tmp/{file.filename}"
#     file.save(video_path)

#     try:
#         transcript = get_transcript_from_video(video_path)
#         return jsonify({'transcript': transcript})
#     except Exception as e:
#         logging.error(f"An error occurred during transcript extraction: {e}")
#         return jsonify({'error': str(e)}), 500


# --------------------------------------------------------------------------------------------------------------------
# using buffer file format
# --------------------------------------------------------------------------------------------------------------------

from flask import Blueprint, request, jsonify
import os
import logging
import google.generativeai as genai
import time
import tempfile
import io

# Blueprint for video routes
video_bp = Blueprint('video_bp', __name__)

# Load environment variables
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_transcript_from_video(video_buffer, original_filename):
    try:
        # Print debug information about the video buffer
        print(f"Video buffer type: {type(video_buffer)}")
        print(f"Video buffer length: {len(video_buffer.getvalue())} bytes")
        
        # Print the first 1000 bytes of the video buffer (or less if the buffer is smaller)
        video_buffer.seek(0)  # Ensure we are at the beginning of the buffer
        preview_data = video_buffer.read(1000)
        # print(f"Video buffer preview: {preview_data[:100]}...")  # Print the first 100 bytes of the preview data
        
        # Use a temporary file to store the video with the correct extension
        _, file_extension = os.path.splitext(original_filename)
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            temp_file.write(video_buffer.getvalue())
            temp_file_path = temp_file.name

        # Print debug information about the temporary file
        # print(f"Temporary file path: {temp_file_path}")

        # Upload the video using the file path
        video = genai.upload_file(path=temp_file_path)
        
        while video.state.name != 'ACTIVE':
            print('.', end="")
            time.sleep(10)
            video = genai.get_file(video.name)
            
            if video.state.name not in ['processing', 'ACTIVE']:
                raise Exception(f"Unexpected video state: {video.state.name}")

        print('\nVideo uploaded successfully and is in ACTIVE state')

        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "write transcript of video"
        response = model.generate_content([prompt, video])
        
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_type = file.filename.rsplit('.', 1)[-1].lower()
    if file_type not in ['mp4', 'avi', 'mov']:
        logging.error(f"Unsupported video format: {file_type}")
        return jsonify({'error': 'Unsupported video format'}), 400

    # Use BytesIO to handle the file in memory
    video_buffer = io.BytesIO(file.read())

    # Print debug information about the video buffer
    print(f"Video buffer type: {type(video_buffer)}")
    print(f"Video buffer length: {len(video_buffer.getvalue())} bytes")
    
    # Print the first 1000 bytes of the video buffer (or less if the buffer is smaller)
    video_buffer.seek(0)  # Ensure we are at the beginning of the buffer
    preview_data = video_buffer.read(1000)
    # print(f"Video buffer preview: {preview_data[:100]}...")  # Print the first 100 bytes of the preview data

    try:
        transcript = get_transcript_from_video(video_buffer, file.filename)
        print("transcription successfully")
        return jsonify({'transcript': transcript})
    except Exception as e:
        logging.error(f"An error occurred during transcript extraction: {e}")
        return jsonify({'error': str(e)}), 500
