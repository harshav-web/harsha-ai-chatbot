from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
import os
import json
from datetime import datetime

load_dotenv()
console = Console()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

HISTORY_FILE = "chat_history.json"

SYSTEM_PROMPT = """You are a helpful and friendly assistant named Harsha Bot.
You remember everything the user tells you in the conversation.
Always reply in the same language the user uses."""

# History file nundi load cheyyadam
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# History file lo save cheyyadam
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def chat(user_message, conversation_history):
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

    # Save cheyyi prathi message tarvata
    save_history(conversation_history)

    return reply

def main():
    if not os.environ.get("GROQ_API_KEY"):
        console.print("[red]ERROR: GROQ_API_KEY not set in .env file![/red] - chatbot.py:62")
        return

    # Previous history load cheyyi
    conversation_history = load_history()

    console.print(Panel.fit(
        "[bold green]Harsha Bot - Chatbot with Memory[/bold green]\n"
        f"[cyan]Loaded {len(conversation_history)} previous messages[/cyan]\n"
        "[yellow]Type 'exit' to stop[/yellow]\n"
        "[yellow]Type 'clear' to clear memory[/yellow]\n"
        "[yellow]Type 'history' to see past chats[/yellow]",
        border_style="green"
    ))

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue

            if user_input.lower() == "exit":
                console.print("[yellow]Goodbye! Chat saved![/yellow] - chatbot.py:84")
                break

            if user_input.lower() == "clear":
                conversation_history.clear()
                save_history(conversation_history)
                console.print("[cyan]Memory cleared![/cyan] - chatbot.py:90")
                continue

            if user_input.lower() == "history":
                if not conversation_history:
                    console.print("[yellow]No history yet![/yellow] - chatbot.py:95")
                else:
                    for msg in conversation_history:
                        role = "You" if msg["role"] == "user" else "Harsha Bot"
                        color = "green" if msg["role"] == "assistant" else "cyan"
                        console.print(f"[{color}]{role}:[/{color}] {msg['content']} - chatbot.py:100")
                continue

            reply = chat(user_input, conversation_history)
            console.print(f"\n[bold green]Harsha Bot:[/bold green] {reply} - chatbot.py:104")

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! Chat saved![/yellow] - chatbot.py:107")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red] - chatbot.py:110")

if __name__ == "__main__":
    main()