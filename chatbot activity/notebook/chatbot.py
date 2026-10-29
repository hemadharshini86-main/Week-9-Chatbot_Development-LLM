import os
import csv
from datetime import datetime
import ollama

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")

os.makedirs(DATASET_DIR, exist_ok=True)

MODEL = "llama3.2:latest"
LOG_FILE = os.path.join(DATASET_DIR, "chatbot_logs.txt")
HISTORY_FILE = os.path.join(DATASET_DIR, "chat_history.csv")


def save_chat(user_message, bot_response):
    os.makedirs("../dataset", exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"[{datetime.now()}]\n"
            f"User: {user_message}\n"
            f"Bot: {bot_response}\n\n"
        )

    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp", "user_message", "bot_response"])

        writer.writerow([
            datetime.now(),
            user_message,
            bot_response
        ])


def chatbot():
    print("===================================")
    print("      Week 9 Ollama Chatbot")
    print("===================================")
    print("Type 'exit' to stop the chatbot.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        try:
            response = ollama.chat(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            bot_response = response["message"]["content"]

            print("Chatbot:", bot_response)
            print()

            save_chat(user_message, bot_response)

        except Exception as e:
            print("Error:", e)
            print("Make sure Ollama is running and the model is installed.")


if __name__ == "__main__":
    chatbot()