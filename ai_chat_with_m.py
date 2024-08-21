# import google.generativeai as genai
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import ConversationChain
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Configure Google Generative AI with the API key
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# # Initialize the chat model
# chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# # Import necessary modules for memory and conversation
# from langchain.chains.conversation.memory import ConversationEntityMemory
# from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

# # Initialize ConversationEntityMemory with the LLM and a memory key
# memory = ConversationEntityMemory(llm=chat, memory_key="entity_memory")

# # Create the ConversationChain with the LLM, memory, and the conversation template
# conversation = ConversationChain(
#     llm=chat, 
#     verbose=False,
#     prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
#     memory=memory
# )

# import re

# # Function to remove emojis from the text
# def remove_emojis(text):
#     emoji_pattern = re.compile(
#         "["  
#         u"\U0001F600-\U0001F64F"  # emoticons
#         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#         u"\U0001F680-\U0001F6FF"  # transport & map symbols
#         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#         "]+", flags=re.UNICODE)
#     return emoji_pattern.sub(r'', text)

# # Continuous conversation loop
# while True:
#     user_input = input("You: ")  # Get input from user

#     if user_input.lower() in ['exit', 'quit', 'bye']:
#         print("Ending conversation.")
#         break  # Exit the loop to end the conversation

#     response = conversation.predict(input=user_input)
#     clean_response = remove_emojis(response)
#     print(f"AI: {clean_response}") 


# ---------------------------------------------------------------------------------------------------------------------------------------------
# with routes
# ---------------------------------------------------------------------------------------------------------------------------------------------

from flask import Blueprint, request, jsonify
import logging
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
import re
import os
from dotenv import load_dotenv

# Create a Blueprint for AI chat
ai_chat_bp = Blueprint('ai_chat', __name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

# Configure Google Generative AI with the API key
genai.configure(api_key=api_key)

# Initialize the chat model
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Initialize ConversationEntityMemory with the LLM and a memory key
memory = ConversationEntityMemory(llm=chat, memory_key="entity_memory")

# Create the ConversationChain with the LLM, memory, and the conversation template
conversation = ConversationChain(
    llm=chat, 
    verbose=False,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=memory
)

# Function to remove emojis from the text
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["  
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Route for AI conversation
@ai_chat_bp.route('/cht_with_ai', methods=['POST'])
def cht_with_ai():
    try:
        # Get the user input from the POST request
        user_input = request.json.get("input")
        print('request : ',user_input)

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Generate AI response
        response = conversation.predict(input=user_input)
        clean_response = remove_emojis(response)
        print('response : ',clean_response)
        
        # Return the AI's response
        return jsonify({"response": clean_response}), 200

    except Exception as e:
        logging.error(f"Error during AI conversation: {e}")
        return jsonify({"error": "Something went wrong"}), 500
