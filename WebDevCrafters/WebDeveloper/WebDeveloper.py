from agency_swarm.agents import Agent


class WebDeveloper(Agent):
    def __init__(self):
        super().__init__(
            name="WebDeveloper",
            description="A versatile agent for WebDevCrafters capable of navigating directories, reading, writing, modifying files, and executing terminal commands.",
            instructions="./instructions.md",
            # files_folder="./files",
            # schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
