# from flask import Blueprint, request, jsonify
# import io
# import logging
# import requests

# # Import your existing functions here
# from qa_export_model import (
#     answer_question_from_pdf_with_retry,
# )

# document_chat_bp = Blueprint('document_chat', __name__)

# # In-memory storage for uploaded files
# uploaded_files = {}

# @document_chat_bp.route('/upload', methods=['POST'])
# def upload_document():
#     """
#     Handles document upload via POST request.
#     The document is processed in-memory without saving to disk.
#     """
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     # Process the uploaded file in-memory
#     file_stream = io.BytesIO(file.read())
#     file_id = 'uploaded_file'  # Unique identifier for the file

#     # Store the file stream in the dictionary
#     uploaded_files[file_id] = file_stream

#     return jsonify({'message': 'File uploaded successfully', 'file_id': file_id}), 200

# @document_chat_bp.route('/ask', methods=['POST'])
# def ask_question():
#     """
#     Handles user questions about the uploaded document.
#     """
#     data = request.json
#     if not data or 'question' not in data or 'file_id' not in data:
#         return jsonify({'error': 'Invalid input'}), 400

#     user_question = data['question']
#     file_id = data['file_id']

#     if file_id not in uploaded_files:
#         return jsonify({'error': 'File not found'}), 404

#     file_stream = uploaded_files[file_id]

#     try:
#         answer = answer_question_from_pdf_with_retry(file_stream, user_question)
#         return jsonify({'answer': answer}), 200
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return jsonify({'error': 'An error occurred while processing the question'}), 500

# @document_chat_bp.route('/url', methods=['POST'])
# def handle_url():
#     """
#     Handles document URL via POST request.
#     """
#     data = request.json
#     if not data or 'url' not in data:
#         return jsonify({'error': 'Invalid input'}), 400

#     url = data['url']
#     try:
#         temp_file_stream = stream_pdf_from_url(url)
#         file_id = 'streamed_file'  # Unique identifier for the file

#         # Store the streamed file in-memory
#         uploaded_files[file_id] = temp_file_stream

#         return jsonify({'message': 'File streamed and processed', 'file_id': file_id}), 200
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return jsonify({'error': 'An error occurred while processing the URL'}), 500

# def stream_pdf_from_url(url):
#     """
#     Streams a PDF file from the given URL.
#     """
#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         return io.BytesIO(response.content)
#     else:
#         raise Exception("Failed to stream file from URL")




# storing the pdf document in local----------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------


# from flask import Flask, request, jsonify,Blueprint
# import logging
# import io
# import requests
# import PyPDF2

# # Import your existing functions here
# from qa_export_model import (
#     answer_question_from_pdf_with_retry,
# )

# document_chat_bp = Blueprint('document_chat', __name__)

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# @document_chat_bp.route('/upload_doc_for_cht', methods=['POST'])
# def upload_document():
#     """
#     Handles document upload via POST request.
#     The document can be uploaded as a local file.
#     """
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     # Process the uploaded file
#     file_stream = io.BytesIO(file.read())

#     # Store the file stream temporarily
#     file_path = 'temp_uploaded_file.pdf'
#     with open(file_path, 'wb') as f:
#         f.write(file_stream.read())

#     return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

# @document_chat_bp.route('/ask', methods=['POST'])
# def ask_question():
#     """
#     Handles user questions about the uploaded document.
#     """
#     data = request.json
#     if not data or 'question' not in data or 'file_path' not in data:
#         return jsonify({'error': 'Invalid input'}), 400

#     user_question = data['question']
#     file_path = data['file_path']

#     try:
#         answer = answer_question_from_pdf_with_retry(file_path, user_question)
#         return jsonify({'answer': answer}), 200
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return jsonify({'error': 'An error occurred while processing the question'}), 500

# @document_chat_bp.route('/url', methods=['POST'])
# def handle_url():
#     """
#     Handles document URL via POST request.
#     """
#     data = request.json
#     if not data or 'url' not in data:
#         return jsonify({'error': 'Invalid input'}), 400

#     url = data['url']
#     try:
#         temp_file_stream = stream_pdf_from_url(url)
#         temp_file_path = 'temp_streamed_file.pdf'
#         with open(temp_file_path, 'wb') as f:
#             f.write(temp_file_stream.read())
#         return jsonify({'message': 'File streamed and processed', 'file_path': temp_file_path}), 200
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return jsonify({'error': 'An error occurred while processing the URL'}), 500

# def stream_pdf_from_url(url):
#     """
#     Streams a PDF file from the given URL.
#     """
#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         return io.BytesIO(response.content)
#     else:
#         raise Exception("Failed to stream file from URL")




# with single endpoint each time to upload for asking question------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------

# from flask import Blueprint, request, jsonify
# import io
# import logging
# import requests

# # Import your existing functions here
# from qa_export_model import answer_question_from_pdf_with_retry

# # Initialize the Flask blueprint
# document_chat_bp = Blueprint('document_chat', __name__)

# # In-memory storage for uploaded files
# uploaded_files = {}

# @document_chat_bp.route('/document_chat', methods=['POST'])
# def document_chat():
#     """
#     Handles document upload and user questions about the uploaded document via POST request.
#     The document is processed in-memory without saving to disk.
#     """
#     if 'file' in request.files:
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         try:
#             # Process the uploaded file in-memory
#             file_stream = io.BytesIO(file.read())
#             file_id = 'uploaded_file'  # Unique identifier for the file

#             # Store the file stream in the dictionary
#             uploaded_files[file_id] = file_stream

#             return jsonify({'message': 'File uploaded successfully', 'file_id': file_id}), 200
#         except Exception as e:
#             logging.error(f"An error occurred while uploading the file: {e}")
#             return jsonify({'error': 'An error occurred while uploading the file'}), 500

#     data = request.json
#     if data and 'question' in data and 'file_id' in data:
#         user_question = data['question']
#         file_id = data['file_id']

#         if file_id not in uploaded_files:
#             return jsonify({'error': 'File not found'}), 404

#         file_stream = uploaded_files[file_id]

#         try:
#             answer = answer_question_from_pdf_with_retry(file_stream, user_question)
#             return jsonify({'answer': answer}), 200
#         except Exception as e:
#             logging.error(f"An error occurred while processing the question: {e}")
#             return jsonify({'error': 'An error occurred while processing the question'}), 500

#     return jsonify({'error': 'Invalid input'}), 400

# @document_chat_bp.route('/document_chat_url', methods=['POST'])
# def document_chat_url():
#     """
#     Handles document URL via POST request and subsequent user questions.
#     """
#     data = request.json
#     if 'url' in data:
#         url = data['url']
#         try:
#             temp_file_stream = stream_pdf_from_url(url)
#             file_id = 'streamed_file'  # Unique identifier for the file

#             # Store the streamed file in-memory
#             uploaded_files[file_id] = temp_file_stream

#             return jsonify({'message': 'File streamed and processed', 'file_id': file_id}), 200
#         except Exception as e:
#             logging.error(f"An error occurred while processing the URL: {e}")
#             return jsonify({'error': 'An error occurred while processing the URL'}), 500

#     elif 'question' in data and 'file_id' in data:
#         user_question = data['question']
#         file_id = data['file_id']

#         if file_id not in uploaded_files:
#             return jsonify({'error': 'File not found'}), 404

#         file_stream = uploaded_files[file_id]

#         try:
#             answer = answer_question_from_pdf_with_retry(file_stream, user_question)
#             return jsonify({'answer': answer}), 200
#         except Exception as e:
#             logging.error(f"An error occurred while processing the question: {e}")
#             return jsonify({'error': 'An error occurred while processing the question'}), 500

#     return jsonify({'error': 'Invalid input'}), 400

# def stream_pdf_from_url(url):
#     """
#     Streams a PDF file from the given URL.
#     """
#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         return io.BytesIO(response.content)
#     else:
#         raise Exception(f"Failed to stream file from URL, status code: {response.status_code}")




# with single endpoint each time to no upload for asking question--------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------


from flask import Blueprint, request, jsonify
import io
import logging
import requests
import uuid
from datetime import datetime, timedelta

# Import your existing functions here
from qa_export_model import answer_question_from_pdf_with_retry

# Initialize the Flask blueprint

document_chat_bp = Blueprint('document_chat', __name__)

# In-memory storage for uploaded files with timestamps
uploaded_files = {}

# Expiration time for UUIDs (e.g., 5 minutes)
EXPIRATION_TIME = timedelta(minutes=5)

# Configure logging to print to the terminal
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_expired_files():
    """Remove files that have expired based on the current time."""
    current_time = datetime.now()
    expired_keys = [file_id for file_id, (file_stream, timestamp) in uploaded_files.items()
                    if current_time - timestamp > EXPIRATION_TIME]
    for file_id in expired_keys:
        del uploaded_files[file_id]
        logging.info(f"File with file_id {file_id} has session expired and been removed.")

@document_chat_bp.route('/document_chat', methods=['POST'])
def document_chat():
    """
    Handles document upload and user questions about the uploaded document via POST request.
    The document is processed in-memory without saving to disk.
    """
    logging.debug("Received request to /document_chat")
    remove_expired_files()  # Clean up expired files before handling the request

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            logging.warning("No selected file in the upload request")
            return jsonify({'error': 'No selected file'}), 400

        try:
            # Process the uploaded file in-memory
            file_stream = io.BytesIO(file.read())
            file_id = str(uuid.uuid4())  # Generate a unique identifier for the file

            # Store the file stream in the dictionary with the current timestamp
            uploaded_files[file_id] = (file_stream, datetime.now())

            logging.info(f"File uploaded successfully with file_id: {file_id}")
            return jsonify({'message': 'File uploaded successfully', 'file_id': file_id}), 200
        except Exception as e:
            logging.error(f"An error occurred while uploading the file: {e}")
            return jsonify({'error': 'An error occurred while uploading the file'}), 500

    data = request.json
    if data and 'question' in data and 'file_id' in data:
        logging.debug(f"Received question: {data['question']} for file_id: {data['file_id']}")
        user_question = data['question']
        file_id = data['file_id']

        if file_id not in uploaded_files:
            logging.warning(f"File not found or session expired: {file_id}")
            return jsonify({'error': 'File not found or session expired'}), 404

        file_stream, timestamp = uploaded_files[file_id]

        # Check if the file has expired
        if datetime.now() - timestamp > EXPIRATION_TIME:
            logging.info(f"File with file_id {file_id} has expired")
            del uploaded_files[file_id]  # Remove the expired file
            return jsonify({'error': 'File has expired'}), 404

        try:
            answer = answer_question_from_pdf_with_retry(file_stream, user_question)
            # logging.info(f"Answer generated: {answer}")
            return jsonify({'answer': answer}), 200
        except Exception as e:
            logging.error(f"An error occurred while processing the question: {e}")
            return jsonify({'error': 'An error occurred while processing the question'}), 500

    logging.warning("Invalid input received")
    return jsonify({'error': 'Invalid input'}), 400

@document_chat_bp.route('/document_chat_url', methods=['POST'])
def document_chat_url():
    """
    Handles document URL via POST request and subsequent user questions.
    """
    logging.debug("Received request to /document_chat_url")
    remove_expired_files()  # Clean up expired files before handling the request

    data = request.json
    if 'url' in data:
        url = data['url']
        try:
            logging.info(f"Streaming PDF from URL: {url}")
            temp_file_stream = stream_pdf_from_url(url)
            file_id = str(uuid.uuid4())  # Generate a unique identifier for the file

            # Store the streamed file in-memory with the current timestamp
            uploaded_files[file_id] = (temp_file_stream, datetime.now())

            logging.info(f"File streamed and processed with file_id: {file_id}")
            return jsonify({'message': 'File streamed and processed', 'file_id': file_id}), 200
        except Exception as e:
            logging.error(f"An error occurred while processing the URL: {e}")
            return jsonify({'error': 'An error occurred while processing the URL'}), 500

    elif 'question' in data and 'file_id' in data:
        logging.debug(f"Received question: {data['question']} for file_id: {data['file_id']}")
        user_question = data['question']
        file_id = data['file_id']

        if file_id not in uploaded_files:
            logging.warning(f"File not found or has expired: {file_id}")
            return jsonify({'error': 'File not found or has expired'}), 404

        file_stream, timestamp = uploaded_files[file_id]

        # Check if the file has expired
        if datetime.now() - timestamp > EXPIRATION_TIME:
            logging.info(f"File with file_id {file_id} has expired")
            del uploaded_files[file_id]  # Remove the expired file
            return jsonify({'error': 'File has expired'}), 404

        try:
            answer = answer_question_from_pdf_with_retry(file_stream, user_question)
            # logging.info(f"Answer generated: {answer}")
            return jsonify({'answer': answer}), 200
        except Exception as e:
            logging.error(f"An error occurred while processing the question: {e}")
            return jsonify({'error': 'An error occurred while processing the question'}), 500

    logging.warning("Invalid input received")
    return jsonify({'error': 'Invalid input'}), 400

def stream_pdf_from_url(url):
    """
    Streams a PDF file from the given URL.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        logging.info(f"Successfully streamed PDF from URL: {url}")
        return io.BytesIO(response.content)
    else:
        logging.error(f"Failed to stream file from URL, status code: {response.status_code}")
        raise Exception(f"Failed to stream file from URL, status code: {response.status_code}")
