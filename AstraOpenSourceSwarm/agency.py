from dotenv import load_dotenv
from CEO import CEO
from GoogleGeminiAgent import GoogleGeminiAgent

load_dotenv("./.env")

from openai import OpenAI
from astra_assistants import patch
from agency_swarm import Agency, set_openai_client

client = patch(OpenAI())
set_openai_client(client)

ceo = CEO()
google_gemini = GoogleGeminiAgent()

agency = Agency([ceo, [ceo, google_gemini]])

if __name__ == "__main__":
    agency.demo_gradio()
