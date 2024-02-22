from agency_swarm import set_openai_key
set_openai_key("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")

from agency_swarm.tools import BaseTool
from pydantic import Field

class MyCustomTool(BaseTool):
    """
    A brief description of what the custom tool does. 
    The docstring should clearly explain the tool's purpose and functionality.
    """

    # Define the fields with descriptions using Pydantic Field
    example_field: str = Field(
        ..., description="Description of the example field, explaining its purpose and usage."
    )

    # Additional fields as required
    # ...

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform its task.
        Doc string description is not required for this method.
        """

        # Your custom tool logic goes here
        do_something(self.example_field)

        # Return the result of the tool's operation
        return "Result of MyCustomTool operation"
    from langchain.tools import YouTubeSearchTool
from agency_swarm.tools import ToolFactory

LangchainTool = ToolFactory.from_langchain_tool(YouTubeSearchTool)

# using local file
with open("schemas/your_schema.json") as f:
    ToolFactory.from_openapi_schema(
        f.read(),
    )

# using requests
ToolFactory.from_openapi_schema(
    requests.get("https://api.example.com/openapi.json").json(),
)
from agency_swarm import Agent

ceo = Agent(name="CEO",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder="./files", # files to be uploaded to OpenAI
            schemas_folder="./schemas", # OpenAPI schemas to be converted into tools
            tools=[MyCustomTool, LangchainTool])

from agency_swarm.agents.browsing import BrowsingAgent

browsing_agent = BrowsingAgent()

browsing_agent.instructions += "\n\nYou can add additional instructions here."
from agency_swarm import Agency

agency = Agency([
    ceo,  # CEO will be the entry point for communication with the user
    [ceo, dev],  # CEO can initiate communication with Developer
    [ceo, va],   # CEO can initiate communication with Virtual Assistant
    [dev, va]    # Developer can initiate communication with Virtual Assistant
], shared_instructions='agency_manifesto.md') # shared instructions for all agents
completion_output = agency.get_completion("Please create a new website for our client.", yield_messages=False)
