from dotenv import load_dotenv
# from CEO import CEO
from LlamaAgent import LlamaAgent
# from GroqAgent import GroqAgent

load_dotenv()

from openai import OpenAI
from astra_assistants import patch
from agency_swarm import Agency, set_openai_client

client = patch(OpenAI(
    base_url="http://127.0.0.1:8000/v1/",
))

set_openai_client(client)

# ceo = CEO()
llama = LlamaAgent()
# groq = GroqAgent()

agency = Agency([llama])

if __name__ == "__main__":
    agency.demo_gradio()
