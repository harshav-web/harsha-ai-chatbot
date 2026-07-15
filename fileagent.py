from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
import os
import json

load_dotenv()
console = Console()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """You are a file management assistant. Convert user commands into file operations.
Respond with ONLY a JSON object in this format:

{
  "action": "create_file" | "read_file" | "delete_file" | "create_folder" | "list_files",
  "filename": "<full path or just filename>",
  "content": "<content if creating a file, else empty string>"
}

Examples:
- "create a file called hello.txt with content Hello World" -> {"action": "create_file", "filename": "hello.txt", "content": "Hello World"}
- "create a file in desktop called test.txt with content hi" -> {"action": "create_file", "filename": "C:/Users/vatti/Desktop/test.txt", "content": "hi"}
- "read hello.txt" -> {"action": "read_file", "filename": "hello.txt", "content": ""}
- "delete hello.txt" -> {"action": "delete_file", "filename": "hello.txt", "content": ""}
- "create folder called myproject" -> {"action": "create_folder", "filename": "myproject", "content": ""}
- "list all files" -> {"action": "list_files", "filename": "", "content": ""}

Always return ONLY the JSON, nothing else."""

def execute_action(action, filename, content):
    if action == "create_file":
        folder = os.path.dirname(filename)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(filename, "w") as f:
            f.write(content)
        console.print(f"[green]File created: {filename}[/green] - fileagent.py:40")

    elif action == "read_file":
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = f.read()
            console.print(f"[cyan]{filename} contents:[/cyan]\n{data} - fileagent.py:46")
        else:
            console.print(f"[red]File not found: {filename}[/red] - fileagent.py:48")

    elif action == "delete_file":
        if os.path.exists(filename):
            os.remove(filename)
            console.print(f"[yellow]Deleted: {filename}[/yellow] - fileagent.py:53")
        else:
            console.print(f"[red]File not found: {filename}[/red] - fileagent.py:55")

    elif action == "create_folder":
        os.makedirs(filename, exist_ok=True)
        console.print(f"[green]Folder created: {filename}[/green] - fileagent.py:59")

    elif action == "list_files":
        files = os.listdir(".")
        console.print("[cyan]Files in current folder:[/cyan] - fileagent.py:63")
        for f in files:
            console.print(f"{f} - fileagent.py:65")

    else:
        console.print(f"[red]Unknown action: {action}[/red] - fileagent.py:68")

def run_command(command):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": command}
            ]
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        execute_action(result["action"], result["filename"], result["content"])
    except Exception as e:
        console.print(f"[red]Error: {e}[/red] - fileagent.py:84")

def main():
    console.print("[bold green]=====================================[/bold green] - fileagent.py:87")
    console.print("[bold green]  File Agent  Type your commands!  [/bold green] - fileagent.py:88")
    console.print("[bold green]  Type exit to stop.                [/bold green] - fileagent.py:89")
    console.print("[bold green]=====================================[/bold green] - fileagent.py:90")

    if not os.environ.get("GROQ_API_KEY"):
        console.print("[red]ERROR: GROQ_API_KEY not set in .env file![/red] - fileagent.py:93")
        return

    while True:
        try:
            command = input("\nCommand: ").strip()
            if not command:
                continue
            if command.lower() == "exit":
                console.print("[yellow]Goodbye![/yellow] - fileagent.py:102")
                break
            run_command(command)
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow] - fileagent.py:106")
            break

if __name__ == "__main__":
    main()