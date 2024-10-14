# from flask import Flask, request, jsonify
# import io
# import os
# import time
# import fitz
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import CacheBackedEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.storage import LocalFileStore
# from langchain.chains import RetrievalQA
# from langchain.callbacks import StdOutCallbackHandler
# from langchain.docstore.document import Document
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# import google.generativeai as genai

# app = Flask(__name__)

# # Load environment variables
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# # Initialize LLM and embeddings
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# # Initialize cache folder
# cache_folder = "./cache/"
# if not os.path.exists(cache_folder):
#     os.makedirs(cache_folder)

# # Global variables for document processing
# vectorstore = None

# def load_pdf_document_from_stream(byte_stream):
#     doc_texts = []
#     with fitz.open(stream=byte_stream, filetype='pdf') as doc:
#         for page in doc:
#             doc_texts.append(page.get_text())
#     # Convert to list of Document objects
#     return [Document(page_content=text) for text in doc_texts]

# def load_text_document_from_stream(byte_stream):
#     loader = TextLoader(io.BytesIO(byte_stream))
#     documents = loader.load()
#     # Convert to list of Document objects
#     return [Document(page_content=text) for text in documents]

# def load_document_from_stream(byte_stream, extension):
#     if extension == '.pdf':
#         return load_pdf_document_from_stream(byte_stream)
#     elif extension == '.txt':
#         return load_text_document_from_stream(byte_stream)
#     else:
#         raise ValueError("Unsupported file format")

# @app.route('/upload', methods=['POST'])
# def upload_document():
#     global vectorstore
#     file = request.files['file']
#     extension = os.path.splitext(file.filename)[1]
#     byte_stream = file.read()

#     # Load and process the document
#     documents = load_document_from_stream(byte_stream, extension)
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     chunks = text_splitter.split_documents(documents)

#     # Initialize cache-backed embeddings and vector store
#     store = LocalFileStore(cache_folder)
#     embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, store, namespace=embeddings.model)
#     vectorstore = FAISS.from_documents(chunks, embedder)

#     return jsonify({"message": "Document processed and vector store created"}), 200

# @app.route('/query', methods=['POST'])
# def query():
#     if vectorstore is None:
#         return jsonify({"error": "No documents loaded. Please upload a document first."}), 400

#     input_query = request.json.get('query')
#     if not input_query:
#         return jsonify({"error": "Query parameter is required."}), 400

#     # Setup the retrieval QA system
#     handler = StdOutCallbackHandler()
#     qa_with_sources_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         callbacks=[handler],
#         return_source_documents=True
#     )

#     # Process the query
#     start_time_query = time.time()
#     response = qa_with_sources_chain.invoke({"query": input_query})
#     end_time_query = time.time()
#     response_time = end_time_query - start_time_query

#     result = response.get('result', '')
#     return jsonify({"result": result, "response_time": response_time}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

# ------------------------------------------------------------------------------------------------
#   with file id...
# ------------------------------------------------------------------------------------------------

from flask import Flask, request, jsonify
import io
import os
import time
import fitz
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize LLM and embeddings
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Initialize cache folder
cache_folder = "./cache/"
if not os.path.exists(cache_folder):
    os.makedirs(cache_folder)

# Store for documents and vectorstores with expiration
document_store = {}

# Helper function to clean expired file_ids
def clean_expired_file_ids():
    current_time = datetime.now()
    expired_keys = [file_id for file_id, data in document_store.items() if data['expiry'] < current_time]
    for file_id in expired_keys:
        del document_store[file_id]

# Generate a unique file_id and store document/vectorstore with expiry
def generate_file_id():
    return str(uuid.uuid4())

def load_pdf_document_from_stream(byte_stream):
    doc_texts = []
    with fitz.open(stream=byte_stream, filetype='pdf') as doc:
        for page in doc:
            doc_texts.append(page.get_text())
    return [Document(page_content=text) for text in doc_texts]

def load_text_document_from_stream(byte_stream):
    loader = TextLoader(io.BytesIO(byte_stream))
    documents = loader.load()
    return [Document(page_content=text) for text in documents]

def load_document_from_stream(byte_stream, extension):
    if extension == '.pdf':
        return load_pdf_document_from_stream(byte_stream)
    elif extension == '.txt':
        return load_text_document_from_stream(byte_stream)
    else:
        raise ValueError("Unsupported file format")

@app.route('/upload', methods=['POST'])
def upload_document():
    global document_store
    file = request.files['file']
    extension = os.path.splitext(file.filename)[1]
    byte_stream = file.read()

    # Load and process the document
    documents = load_document_from_stream(byte_stream, extension)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)

    # Initialize cache-backed embeddings and vector store
    store = LocalFileStore(cache_folder)
    embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, store, namespace=embeddings.model)
    vectorstore = FAISS.from_documents(chunks, embedder)

    # Generate a file_id
    file_id = generate_file_id()

    # Set expiration time (15 minutes from now)
    expiry_time = datetime.now() + timedelta(minutes=15)

    # Store the vectorstore and expiry time in the document store
    document_store[file_id] = {
        'vectorstore': vectorstore,
        'expiry': expiry_time
    }

    return jsonify({"message": "Document processed and vector store created", "file_id": file_id}), 200

@app.route('/query', methods=['POST'])
def query():
    global document_store
    # Clean up any expired file_ids
    clean_expired_file_ids()

    # Get file_id and query from request
    file_id = request.json.get('file_id')
    input_query = request.json.get('query')

    if not file_id or not input_query:
        return jsonify({"error": "file_id and query parameters are required."}), 400

    # Check if file_id exists and is still valid
    if file_id not in document_store:
        return jsonify({"error": "Invalid or expired file_id."}), 400

    # Check if the file_id is expired
    if document_store[file_id]['expiry'] < datetime.now():
        del document_store[file_id]  # Clean up expired file_id
        return jsonify({"error": "file_id has expired."}), 400

    # Get the vectorstore for the given file_id
    vectorstore = document_store[file_id]['vectorstore']

    # Setup the retrieval QA system
    handler = StdOutCallbackHandler()
    qa_with_sources_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        callbacks=[handler],
        return_source_documents=True
    )

    # Process the query
    start_time_query = time.time()
    response = qa_with_sources_chain.invoke({"query": input_query})
    end_time_query = time.time()
    response_time = end_time_query - start_time_query

    result = response.get('result', '')
    return jsonify({"result": result, "response_time": response_time}), 200

if __name__ == '__main__':
    app.run(debug=True)
