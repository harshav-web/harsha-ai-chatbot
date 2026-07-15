from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
import os

load_dotenv()
console = Console()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def detect_language(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Detect the language of the text and reply with ONLY one word: 'spanish', 'telugu', or 'english'."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip().lower()

def spanish_agent(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You only speak Spanish."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

def english_agent(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You only speak English."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

def telugu_agent(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content":"text"},
            {"role": "user", "content": "text"} ,"You are a helpful assistant. You only speak Telugu but write responses in English letters (transliteration). Example: 'Nenu bagunnanu' instead of 'నేను బాగున్నాను'."
        ]
    )
    return response.choices[0].message.content.strip()

def triage_agent(text):
    language = detect_language(text)
    console.print(f"[yellow]Triage: Detected language → {language}[/yellow]")

    if "spanish" in language:
        console.print("[cyan]Triage: Handing off to Spanish Agent...[/cyan]")
        return spanish_agent(text)
    elif "telugu" in language:
        console.print("[cyan]Triage: Handing off to Telugu Agent...[/cyan]")
        return telugu_agent(text)
    else:
        console.print("[cyan]Triage: Handing off to English Agent...[/cyan]")
        return english_agent(text)

def main():
    if not os.environ.get("GROQ_API_KEY"):
        console.print("[red]ERROR: GROQ_API_KEY not set in .env file![/red]")
        return

    console.print("[bold green]=====================================[/bold green]")
    console.print("[bold green]  Language Triage Agent (Groq)      [/bold green]")
    console.print("[bold green]  Type exit to stop.                [/bold green]")
    console.print("[bold green]=====================================[/bold green]")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            console.print("[yellow]Goodbye![/yellow]")
            break
        try:
            result = triage_agent(user_input)
            console.print(f"[bold green]Agent:[/bold green] {result}")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
