from agency_swarm import Agency
from BrowsingAgent import BrowsingAgent
from Devid import Devid
from PlannerAgent import PlannerAgent

from dotenv import load_dotenv
load_dotenv()

planner = PlannerAgent()
devid = Devid()
browsingAgent = BrowsingAgent()

agency = Agency([planner, devid, browsingAgent, [planner, devid],
                 [planner, browsingAgent],
                 [devid, browsingAgent]],
                shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    agency.demo_gradio(server_name="0.0.0.0")