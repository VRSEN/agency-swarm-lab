import os
import json

from agency_swarm import Agency, set_openai_key

from CEO import CEO
from Copywriter import Copywriter
from WebDeveloper import WebDeveloper
from Designer import Designer

# load env from .env
from dotenv import load_dotenv
load_dotenv()

set_openai_key(os.environ["OPENAI_API_KEY"])

def load_threads(chat_id):
    if os.path.exists(f"{chat_id}_threads.json"):
        with open(f"{chat_id}_threads.json", "r") as file:
            threads = json.load(file)
    else:
        threads = []
    return threads

def save_threads(new_threads, chat_id):
    # Save threads to a file or database using the chat_id
    with open(f"{chat_id}_threads.json", "w") as file:
        json.dump(new_threads, file)

ceo = CEO()
designer = Designer()
web_developer = WebDeveloper()
copywriter = Copywriter()

chat_id = '1234'

agency = Agency([ceo, designer, web_developer,
                 [ceo, designer],
                 [designer, ceo],
                 [designer, web_developer],
                 [web_developer, designer],
                 [designer, copywriter]],
                shared_instructions='./agency_manifesto.md',
                threads_callbacks={
                    'load': lambda: load_threads(chat_id=chat_id),
                    'save': lambda new_threads: save_threads(new_threads, chat_id=chat_id)
                })

if __name__ == '__main__':
    agency.demo_gradio(height=400)
