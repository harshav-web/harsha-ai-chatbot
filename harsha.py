
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
import os
console=Console()
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
def ask(q):

    response = client.responses.create(
        input=q,
        model="openai/gpt-oss-20b",
    )
    print(response.output_text)

while True:
    ask(input("ask a question "))
