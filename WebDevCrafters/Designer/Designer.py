from agency_swarm.agents import Agent


class Designer(Agent):
    def __init__(self):
        super().__init__(
            name="Designer",
            description="An agent that analyzes the current browser window for WebDevCrafters.",
            instructions="./instructions.md",
            # files_folder="./files",
            # schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
