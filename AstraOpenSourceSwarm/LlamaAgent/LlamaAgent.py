from agency_swarm.agents import Agent


class LlamaAgent(Agent):
    def __init__(self):
        super().__init__(
            name="LlamaAgent",
            description="Llama agent that uses the latest llama3 model.",
            instructions="./instructions.md",
            tools=[],
            tools_folder="./tools",
            files_folder="./files",
            model="ollama/llama3.1:8b"
        )
        
    def response_validator(self, message):
        return message
