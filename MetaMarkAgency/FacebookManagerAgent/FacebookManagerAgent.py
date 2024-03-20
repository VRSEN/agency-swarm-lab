from agency_swarm.agents import Agent


class FacebookManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="FacebookManagerAgent",
            description="Handles the scheduling and posting of the ads on Facebook. Ensures that each ad is posted according to the best practices for timing and audience targeting.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
