# from flask import Flask, jsonify, request, render_template
# from main import take_command, Command
# import os
# import threading
# import sys

# app = Flask(__name__)

# CHAT_FILE = 'chat.txt'

# # Route for your AI assistant's interface
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route('/api/get_chat')
# def get_chat():
#     if os.path.exists(CHAT_FILE):
#         try:
#             with open(CHAT_FILE, 'r') as file:
#                 chat_data = file.read()
#             return jsonify(chat=chat_data)
#         except Exception as e:
#             print(f"Error reading chat file: {e}")  # Debugging line
#             return jsonify(chat="Error reading chat file."), 500
#     else:
#         print("Chat file not found.")  # Debugging line
#         return jsonify(chat="No chat available."), 404

# @app.route('/api/log_message', methods=['POST'])
# def log_message_route():
#     data = request.get_json()
#     message = data.get('message', '')
#     print(f"Logging message: {message}")  # Debugging line
#     try:
#         with open(CHAT_FILE, 'a') as file:
#             file.write(message + '\n')
#         # Keep only the last 4 lines
#         with open(CHAT_FILE, 'r') as file:
#             lines = file.readlines()
#         with open(CHAT_FILE, 'w') as file:
#             file.writelines(lines[-4:])
#     except Exception as e:
#         print(f"Error writing to chat file: {e}")  # Debugging line
#     return jsonify(success=True)

# def run_flask():
#     app.run(host='0.0.0.0', port=4444, debug=True)

# def main():
#     # Initialize your Command class and other necessary components
#     jarvis = Command()  # Assuming Command is your assistant class
#     while True:
#         command = take_command().lower()
#         if command != "none":
#             if "exit" in command or "goodbye" in command:
#                 print("Exiting...")
#                 os._exit(0)  # Forcefully exit the server
#             jarvis.system_task(command)
#             jarvis.startup(command)
#             jarvis.phone(command)
#     print("Main function is running")

# if __name__ == "__main__":
#     # Start the main logic in a separate thread
#     main_thread = threading.Thread(target=main)
#     main_thread.start()

#     # Run Flask in the main thread
#     run_flask()

#     # Join the main thread if needed
#     main_thread.join()



from main import main

main()