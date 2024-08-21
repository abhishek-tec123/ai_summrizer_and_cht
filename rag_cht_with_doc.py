# ------------------------------------------------------------------------------------------------
#   with chroma vector databas
# ------------------------------------------------------------------------------------------------

# import os
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# import bs4
# from langchain import hub
# from langchain_chroma import Chroma
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# import google.generativeai as genai
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


# loader = WebBaseLoader(
#     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
#     bs_kwargs=dict(
#         parse_only=bs4.SoupStrainer(
#             class_=("post-content", "post-title", "post-header")
#         )
#     ),
# )
# docs = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(docs)
# # print(splits)
# vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
# print(vectorstore)

# retriever = vectorstore.as_retriever()
# prompt = hub.pull("rlm/rag-prompt")

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)


# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# print(rag_chain.invoke("What is mango?"))




# ------------------------------------------------------------------------------------------------
#   with faiss vector databas
# ------------------------------------------------------------------------------------------------


# from langchain_community.document_loaders import WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import CacheBackedEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.storage import LocalFileStore
# from langchain.chains import RetrievalQA
# from langchain.callbacks import StdOutCallbackHandler
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# # Load documents from web sources
# yolo_nas_loader = WebBaseLoader("https://deci.ai/blog/yolo-nas-object-detection-foundation-model/").load()
# decicoder_loader = WebBaseLoader("https://deci.ai/blog/decicoder-efficient-and-accurate-code-generation-llm/#:~:text=DeciCoder's%20unmatched%20throughput%20and%20low,re%20obsessed%20with%20AI%20efficiency.").load()
# yolo_newsletter_loader = WebBaseLoader("https://deeplearningdaily.substack.com/p/unleashing-the-power-of-yolo-nas").load()

# # Split documents into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# yolo_nas_chunks = text_splitter.split_documents(yolo_nas_loader)
# decicoder_chunks = text_splitter.split_documents(decicoder_loader)
# yolo_newsletter_chunks = text_splitter.split_documents(yolo_newsletter_loader)

# # Initialize cache-backed embeddings and vector store
# store = LocalFileStore("./cache/")
# embedder = CacheBackedEmbeddings.from_bytes_store(
#     embeddings,
#     store,
#     namespace=embeddings.model
# )

# # Store embeddings in vector store
# vectorstore = FAISS.from_documents(yolo_nas_chunks, embedder)
# vectorstore.add_documents(decicoder_chunks)
# vectorstore.add_documents(yolo_newsletter_chunks)

# # Instantiate a retriever
# retriever = vectorstore.as_retriever()

# # Setup the retrieval QA system
# handler = StdOutCallbackHandler()
# qa_with_sources_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     callbacks=[handler],
#     return_source_documents=True
# )

# # Query the retrieval system
# response = qa_with_sources_chain.invoke({"query": "give summary of this document"})
# print(response['result'])

# # Function to print vector store details
# def print_vector_store_details(vector_store):
#     index = vector_store.index
#     print("Vector Store Index Details:")
#     print(f"Number of vectors: {index.ntotal}")
#     print(f"Dimension of vectors: {index.d}")

#     # Assuming vectors are stored with metadata, print some metadata examples
#     if hasattr(vector_store, 'docstore'):
#         docstore = vector_store.docstore
#         print("\nExample document metadata and content:")
#         for i, (key, doc) in enumerate(docstore._dict.items()):
#             print(f"Document {i+1}:")
#             # print(f"Content: {doc.page_content}")
#             print(f"Metadata: {doc.metadata}")
#             if i >= 2:  # Limit output to first few documents for brevity
#                 break

# # Print vector store index details
# print_vector_store_details(vectorstore)

# # Function to print vector data
# def print_vector_data(vector_store):
#     index = vector_store.index
#     for i in range(min(3, index.ntotal)):  # Limit output to first few vectors for brevity
#         vector = index.reconstruct(i)
#         print(f"Vector {i+1}: {vector}")

# # Print vector data
# print_vector_data(vectorstore)


# ------------------------------------------------------------------------------------------------
#   with speedup response faiss vector databas
# ------------------------------------------------------------------------------------------------


# import os
# import time
# from dotenv import load_dotenv
# from concurrent.futures import ThreadPoolExecutor
# from langchain_community.document_loaders import WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import CacheBackedEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.storage import LocalFileStore
# from langchain.chains import RetrievalQA
# from langchain.callbacks import StdOutCallbackHandler
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# # Initialize LLM and embeddings
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# # Function to load documents concurrently
# def load_document(url):
#     return WebBaseLoader(url).load()

# # URLs of the documents to be loaded
# urls = [
#     "https://deci.ai/blog/yolo-nas-object-detection-foundation-model/",
#     "https://deci.ai/blog/decicoder-efficient-and-accurate-code-generation-llm/#:~:text=DeciCoder's%20unmatched%20throughput%20and%20low,re%20obsessed%20with%20AI%20efficiency.",
#     "https://deeplearningdaily.substack.com/p/unleashing-the-power-of-yolo-nas"
# ]

# # Measure the start time for document loading
# start_time_loading = time.time()

# # Load documents concurrently
# with ThreadPoolExecutor() as executor:
#     documents = list(executor.map(load_document, urls))

# # Measure the end time for document loading
# end_time_loading = time.time()
# print(f"Document loading time: {end_time_loading - start_time_loading:.2f} seconds")

# # Measure the start time for text splitting
# start_time_splitting = time.time()

# # Split documents into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# chunks = [chunk for doc in documents for chunk in text_splitter.split_documents(doc)]

# # Measure the end time for text splitting
# end_time_splitting = time.time()
# print(f"Text splitting time: {end_time_splitting - start_time_splitting:.2f} seconds")

# # Measure the start time for embedding and vector store creation
# start_time_embedding = time.time()

# # Initialize cache-backed embeddings and vector store
# store = LocalFileStore("./cache/")
# embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, store, namespace=embeddings.model)
# vectorstore = FAISS.from_documents(chunks, embedder)

# # Measure the end time for embedding and vector store creation
# end_time_embedding = time.time()
# print(f"Embedding and vector store creation time: {end_time_embedding - start_time_embedding:.2f} seconds")

# # Instantiate a retriever
# retriever = vectorstore.as_retriever()

# # Setup the retrieval QA system
# handler = StdOutCallbackHandler()
# qa_with_sources_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     callbacks=[handler],
#     return_source_documents=True
# )

# # Measure the start time for query response
# start_time_query = time.time()

# # Query the retrieval system
# response = qa_with_sources_chain.invoke({"query": "give summary of this document"})
# print(response['result'])

# # Measure the end time for query response
# end_time_query = time.time()
# print(f"Query response time: {end_time_query - start_time_query:.2f} seconds")

# # Function to print vector store details
# def print_vector_store_details(vector_store):
#     index = vector_store.index
#     print("Vector Store Index Details:")
#     print(f"Number of vectors: {index.ntotal}")
#     print(f"Dimension of vectors: {index.d}")

#     if hasattr(vector_store, 'docstore'):
#         docstore = vector_store.docstore
#         print("\nExample document metadata and content:")
#         for i, (key, doc) in enumerate(docstore._dict.items()):
#             print(f"Document {i+1}:")
#             print(f"Metadata: {doc.metadata}")
#             if i >= 2:
#                 break

# # Print vector store index details
# print_vector_store_details(vectorstore)

# # Function to print vector data
# def print_vector_data(vector_store):
#     index = vector_store.index
#     for i in range(min(3, index.ntotal)):
#         vector = index.reconstruct(i)
#         print(f"Vector {i+1}: {vector}")

# # Print vector data
# # print_vector_data(vectorstore)


# ------------------------------------------------------------------------------------------------
#   chat with pdf and text doc speedup response faiss vector databas
# ------------------------------------------------------------------------------------------------

import os
import time
from concurrent.futures import ThreadPoolExecutor
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
start_time_total = time.time()

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize LLM and embeddings
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Function to load PDF documents
def load_pdf_document(filepath):
    loader = PyMuPDFLoader(filepath)
    return loader.load()

# Function to load text documents
def load_text_document(filepath):
    loader = TextLoader(filepath)
    return loader.load()

# Paths of the documents to be loaded
filepaths = [
    "/Users/macbook/Desktop/llama3.1/summary/docs/python.pdf"
    ]

# Function to load documents based on file extension
def load_document(filepath):
    if filepath.endswith('.pdf'):
        return load_pdf_document(filepath)
    elif filepath.endswith('.txt'):
        return load_text_document(filepath)
    else:
        raise ValueError("Unsupported file format")

# Measure the start time for document loading
start_time_loading = time.time()

# Load documents concurrently
with ThreadPoolExecutor() as executor:
    documents = list(executor.map(load_document, filepaths))

# Measure the end time for document loading
end_time_loading = time.time()
print(f"Document loading time: {end_time_loading - start_time_loading:.2f} seconds")

# Measure the start time for text splitting
start_time_splitting = time.time()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = [chunk for doc in documents for chunk in text_splitter.split_documents(doc)]

# Measure the end time for text splitting
end_time_splitting = time.time()
print(f"Text splitting time: {end_time_splitting - start_time_splitting:.2f} seconds")

# Cache folder path
cache_folder = "./cache/"

# Check if cache folder exists, create if not
if not os.path.exists(cache_folder):
    os.makedirs(cache_folder)
    print(f"Cache folder created at {cache_folder}")
    
# Measure the start time for embedding and vector store creation
start_time_embedding = time.time()

# Initialize cache-backed embeddings and vector store
store = LocalFileStore(cache_folder)
embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, store, namespace=embeddings.model)
vectorstore = FAISS.from_documents(chunks, embedder)

# Measure the end time for embedding and vector store creation
end_time_embedding = time.time()
print(f"Embedding and vector store creation time: {end_time_embedding - start_time_embedding:.2f} seconds")

# Instantiate a retriever
retriever = vectorstore.as_retriever()

# Setup the retrieval QA system
handler = StdOutCallbackHandler()
qa_with_sources_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    callbacks=[handler],
    return_source_documents=True
)

# Measure the start time for query response
start_time_query = time.time()

# Query the retrieval system
response = qa_with_sources_chain.invoke({"query": "what is python"})
print(response['result'])

# Measure the end time for query response
end_time_query = time.time()
print(f"Query response time: {end_time_query - start_time_query:.2f} seconds")



# Function to print vector store details
def print_vector_store_details(vector_store):
    index = vector_store.index
    print("Vector Store Index Details:")
    print(f"Number of vectors: {index.ntotal}")
    print(f"Dimension of vectors: {index.d}")

    if hasattr(vector_store, 'docstore'):
        docstore = vector_store.docstore
        print("\nExample document metadata and content:")
        for i, (key, doc) in enumerate(docstore._dict.items()):
            # print(f"Document {i+1}:")
            # print(f"Metadata: {doc.metadata}")
            if i >= 10:
                break

# Print vector store index details
print_vector_store_details(vectorstore)

# Function to print vector data
def print_vector_data(vector_store):
    index = vector_store.index
    for i in range(min(1, index.ntotal)):
        vector = index.reconstruct(i)
        print(f"Vector {i+1}: {vector}")
        
end_time_total = time.time()
print(f"Total time taken: {end_time_total - start_time_total:.2f} seconds")

# Print vector data
# print_vector_data(vectorstore)