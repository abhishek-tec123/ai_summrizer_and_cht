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
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai

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

# Global variables for document processing
vectorstore = None

def load_pdf_document_from_stream(byte_stream):
    doc_texts = []
    with fitz.open(stream=byte_stream, filetype='pdf') as doc:
        for page in doc:
            doc_texts.append(page.get_text())
    return doc_texts

def load_text_document_from_stream(byte_stream):
    loader = TextLoader(io.BytesIO(byte_stream))
    return loader.load()

def load_document_from_stream(byte_stream, extension):
    if extension == '.pdf':
        return load_pdf_document_from_stream(byte_stream)
    elif extension == '.txt':
        return load_text_document_from_stream(byte_stream)
    else:
        raise ValueError("Unsupported file format")

@app.route('/upload', methods=['POST'])
def upload_document():
    global vectorstore
    file = request.files['file']
    extension = os.path.splitext(file.filename)[1]
    byte_stream = file.read()

    # Load and process the document
    documents = load_document_from_stream(byte_stream, extension)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = [chunk for doc in documents for chunk in text_splitter.split_documents(doc)]

    # Initialize cache-backed embeddings and vector store
    store = LocalFileStore(cache_folder)
    embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, store, namespace=embeddings.model)
    vectorstore = FAISS.from_documents(chunks, embedder)

    return jsonify({"message": "Document processed and vector store created"}), 200

@app.route('/query', methods=['POST'])
def query():
    if vectorstore is None:
        return jsonify({"error": "No documents loaded. Please upload a document first."}), 400

    input_query = request.json.get('query')
    if not input_query:
        return jsonify({"error": "Query parameter is required."}), 400

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
