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

def call_agent(system_prompt, text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

def detect_language(text):
    return call_agent(
        "Detect the language of the text and reply with ONLY one word: 'spanish', 'telugu', or 'english'.",
        text
    ).lower()

def triage_agent(text):
    language = detect_language(text)
    console.print(f"[yellow]Triage: Detected language → {language}[/yellow]")

    if "spanish" in language:
        console.print("[cyan]Triage: Handing off to Spanish Agent...[/cyan]")
        return call_agent("You are a helpful assistant. You only speak Spanish.", text)
    elif "telugu" in language:
        console.print("[cyan]Triage: Handing off to Telugu Agent...[/cyan]")
        return call_agent("You are a helpful assistant. Reply in Telugu but write using English letters only. Example: 'Nenu bagunnanu' not Telugu script.", text)
    else:
        console.print("[cyan]Triage: Handing off to English Agent...[/cyan]")
        return call_agent("You are a helpful assistant. You only speak English.", text)

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
