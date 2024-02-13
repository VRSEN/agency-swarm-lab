from agency_swarm.agents import Agent


class CEO(Agent):
    def __init__(self):
        super().__init__(
            name="CEO",
            description="Acts as the overseer and communicator across the agency, ensuring alignment with the agency's goals.",
            instructions="./instructions.md",
            # files_folder="./files",
            # schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
