import time
from agency_swarm import Agency
from agency_swarm import set_openai_client
from dotenv import load_dotenv
from openai import OpenAI
from CEO import CEO
from LlamaAgent import LlamaAgent
from GoogleGeminiAgent import GoogleGeminiAgent
from demo_gradio import demo_gradio

load_dotenv()

client = OpenAI(
    base_url="http://127.0.0.1:8086/api/v1",
    api_key="xxx",
    max_retries=5,
    default_headers={
        "OpenAI-Beta": "assistants=v1"
    }
)
set_openai_client(client)

ceo = CEO()
llama = LlamaAgent()
google_gemini = GoogleGeminiAgent()

agency = Agency([ceo, [ceo, llama], [ceo, google_gemini]])

if __name__ == "__main__":
    demo_gradio(agency)


