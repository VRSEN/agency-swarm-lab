from agency_swarm.agents import Agent


class Copywriter(Agent):
    def __init__(self):
        super().__init__(
            name="Copywriter",
            description="Responsible for creating compelling content for the web applications. Collaborates with the Web Developer for content integration.",
            instructions="./instructions.md",
            # files_folder="./files",
            # schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
