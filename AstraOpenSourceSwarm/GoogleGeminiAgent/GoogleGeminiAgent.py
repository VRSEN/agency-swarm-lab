from agency_swarm.agents import Agent


class GoogleGeminiAgent(Agent):
    def __init__(self):
        super().__init__(
            name="GoogleGeminiAgent",
            description="Agent based on the google gemini model",
            instructions="./instructions.md",
            tools=[],
            model="gemini/gemini-1.5-pro-latest"
        )
        
    def response_validator(self, message):
        return message
