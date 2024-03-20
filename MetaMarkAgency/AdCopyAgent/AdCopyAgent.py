from agency_swarm.agents import Agent


class AdCopyAgent(Agent):
    def __init__(self):
        super().__init__(
            name="AdCopyAgent",
            description="Specializes in generating creative and engaging ad copy using AI tools. Assesses the target audience and product/service features to craft compelling messages.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
