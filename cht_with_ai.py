# from dotenv import load_dotenv
# import os
# import textwrap
# import google.generativeai as genai

# # Load environment variables from .env
# load_dotenv()

# # Configure Google API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return textwrap.indent(text, '> ', predicate=lambda _: True)

# # Function to get response from Gemini model
# def get_gemini_response(question):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(question)
#     return response.text

# def main():
#     while True:
#         question = input("Enter your question (or /q to quit): ")
#         if question.strip() == "/q":
#             print("Exiting...")
#             break
        
#         response = get_gemini_response(question)
        
#         # Print question and answer
#         print(f"**Question:** {question}")
#         print(to_markdown(response))

# if __name__ == "__main__":
#     main()



# from dotenv import load_dotenv
# import os
# import textwrap
# import google.generativeai as genai

# # Load environment variables from .env
# load_dotenv()

# # Configure Google API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return textwrap.indent(text, '> ', predicate=lambda _: True)

# def save_history_to_file(history, filename="history.txt"):
#     with open(filename, "w") as file:
#         for question, answer in history:
#             file.write(f"Q: {question}\n")
#             file.write(f"A: {answer}\n\n")

# def load_history_from_file(filename="history.txt"):
#     history = []
#     if os.path.exists(filename):
#         with open(filename, "r") as file:
#             content = file.read().strip()
#             if content:
#                 entries = content.split("\n\n")
#                 for entry in entries:
#                     if entry:
#                         q, a = entry.split("\nA: ")
#                         question = q.replace("Q: ", "").strip()
#                         answer = a.strip()
#                         history.append((question, answer))
#     return history

# def get_gemini_response(question):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(question)
#     return response.text

# def find_similar_question(question, history):
#     for q, a in history:
#         if question.lower() == q.lower():  # Simple comparison, can be improved with more advanced similarity checks
#             return a
#     return None

# def main():
#     history = load_history_from_file()  # Load history from file

#     while True:
#         question = input("Enter your question (or /q to quit, /h to view history): ")
        
#         if question.strip() == "/q":
#             print("Exiting...")
#             break

#         elif question.strip() == "/h":
#             # Print history
#             if not history:
#                 print("No history available.")
#             else:
#                 for idx, (q, a) in enumerate(history):
#                     print(f"\n**Q{idx + 1}:** {q}")
#                     print(f"**A{idx + 1}:**\n{to_markdown(a)}")
#             continue

#         # Check if the question already exists in the history
#         existing_answer = find_similar_question(question, history)
        
#         if existing_answer:
#             response = existing_answer
#             print("Found similar question in history.")
#         else:
#             # Get response from Gemini model
#             response = get_gemini_response(question)
#             # Store the question and response in history
#             history.append((question, response))
#             # Save history to file
#             save_history_to_file(history)
        
#         # Print question and answer
#         print(f"**Question:** {question}")
#         print(to_markdown(response))

# if __name__ == "__main__":
#     main()



