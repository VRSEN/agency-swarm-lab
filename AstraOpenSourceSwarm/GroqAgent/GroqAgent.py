from agency_swarm.agents import Agent


class GroqAgent(Agent):
    def __init__(self, model_id: str = 'llama-3.1-70b-versatile'):
        super().__init__(
            name="GroqAgent",
            description="uses any model available from groq",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            model=f"groq/{model_id}"
        )
        
    def response_validator(self, message):
        return message
