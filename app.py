from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

HISTORY_FILE = "chat_history.json"

SYSTEM_PROMPT = """You are a helpful and friendly assistant named Harsha Bot.
You remember everything the user tells you in the conversation.
Always reply in the same language the user uses."""

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    conversation_history = load_history()
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + conversation_history
    )
    reply = response.choices[0].message.content.strip()
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })
    save_history(conversation_history)
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    save_history([])
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)