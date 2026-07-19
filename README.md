# Harsha AI Chatbot 🤖

An AI-powered chatbot built with Python, Flask, and Groq API (Llama 3.3). Includes both a terminal-based chatbot and a full website chat interface with persistent memory.

## Features

- 💬 Chat with AI powered by Groq's Llama 3.3 model
- 🧠 Conversation memory — remembers what you told it earlier
- 💾 Chat history saved to a JSON file
- 🌐 Web interface with a clean, modern chat UI
- 💻 Terminal chatbot option for quick testing

## Project Structure

```
harsha-ai-chatbot/
├── app.py                 # Flask website backend
├── chatbot.py             # Terminal-based chatbot (with memory)
├── templates/
│   └── index.html         # Website chat interface (HTML/CSS/JS)
├── chat_history.json      # Saved conversation history
└── .env                   # API keys (not uploaded — kept private)
```

## Requirements

```
pip install flask openai python-dotenv rich
```

## Setup

1. Clone this repository
2. Create a `.env` file in the project folder with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Get a free API key from [console.groq.com](https://console.groq.com)

## How to Run

**Website version:**
```
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

**Terminal version:**
```
python chatbot.py
```

## Tech Stack

- **Backend:** Python, Flask
- **AI Model:** Groq API (Llama 3.3 70B)
- **Frontend:** HTML, CSS, JavaScript
- **Storage:** JSON file

## Notes

This is a learning project built to understand AI agents, APIs, and full-stack development basics.
