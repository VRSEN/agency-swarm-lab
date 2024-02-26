from agency_swarm import Agency, set_openai_key
from CEO import CEO
from Copywriter import Copywriter
from WebDeveloper import WebDeveloper
from Designer import Designer
import os

# load env from .env
from dotenv import load_dotenv
load_dotenv()

set_openai_key(os.environ["OPENAI_API_KEY"])

ceo = CEO()
designer = Designer()
web_developer = WebDeveloper()
copywriter = Copywriter()

agency = Agency([ceo, designer, web_developer,
                 [ceo, designer],
                 [designer, web_developer],
                 [designer, copywriter]],
                shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    # agency.demo_gradio(height=400)
    agency.run_demo()