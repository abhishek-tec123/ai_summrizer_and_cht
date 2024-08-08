from flask import Flask
import logging
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logging.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    exit(1)

# Import and register blueprints
from document_routes import document_bp
from audio_routes import audio_bp
from video_routes import video_bp
from doc_cht import document_chat_bp

app.register_blueprint(document_bp, url_prefix='/document-for-summary')
app.register_blueprint(audio_bp, url_prefix='/audio')
app.register_blueprint(video_bp, url_prefix='/video')
# app.register_blueprint(document_chat_bp, url_prefix='/document-chat')
app.register_blueprint(document_chat_bp, url_prefix='/document_chat')

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the AI-Powered Document Summarization API!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)



# without document chat route--------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------



# from flask import Flask
# import logging
# from dotenv import load_dotenv
# import os

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize Flask app
# app = Flask(__name__)

# # Load environment variables
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     logging.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
#     exit(1)

# # Import and register blueprints
# from document_routes import document_bp
# from audio_routes import audio_bp
# from video_routes import video_bp

# app.register_blueprint(document_bp, url_prefix='/document')
# app.register_blueprint(audio_bp, url_prefix='/audio')
# app.register_blueprint(video_bp, url_prefix='/video')

# @app.route('/', methods=['GET'])
# def home():
#     return "Welcome to the AI-Powered Document Summarization API!"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)
