from agency_swarm.agents import Agent


class ImageCreatorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ImageCreatorAgent",
            description="Utilizes DALL-E 3 to generate images that are in sync with the ad copy. Tasked with creating visually appealing graphics that grab attention and convey the message effectively.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
