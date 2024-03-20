from agency_swarm.agents import Agent


class MetaMarkCEO(Agent):
    def __init__(self):
        super().__init__(
            name="MetaMarkCEO",
            description="Oversees the entire operation, maintains the workflow among agents, and ensures the agency's goals are met. Acts as the strategic overseer and initiator of the advertising campaign process.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
