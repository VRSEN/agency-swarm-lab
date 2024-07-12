from agency_swarm.agents import Agent


class GroqAgent(Agent):
    def __init__(self):
        super().__init__(
            name="GroqAgent",
            description="uses llama3 with groq",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            model="groq/llama3-8b-8192"
        )
        
    def response_validator(self, message):
        return message
