from agency_swarm import Agency
from FacebookManagerAgent import FacebookManagerAgent
from ImageCreatorAgent import ImageCreatorAgent
from AdCopyAgent import AdCopyAgent
from MetaMarkCEO import MetaMarkCEO

from dotenv import load_dotenv
load_dotenv()

ceo = MetaMarkCEO()
adCopyAgent = AdCopyAgent()
imageCreatorAgent = ImageCreatorAgent()
facebookManagerAgent = FacebookManagerAgent()

agency = Agency([
                  ceo, facebookManagerAgent,
                 [ceo, adCopyAgent],
                 [adCopyAgent, imageCreatorAgent],
                 [ceo, facebookManagerAgent],
                 [ceo, imageCreatorAgent]],
                shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    agency.demo_gradio()