from agency_swarm.agents import Agent
from agency_swarm.tools import CodeInterpreter

class CodeAnalyzer(Agent):
    def __init__(self):
        super().__init__(
            name="CodeAnalyzer",
            description="Specializes in retrieving changes from pull requests using the GitHub API, analyzing them against predefined quality standards for TypeScript codebases. Communicates findings to the Report Generator Agent for report compilation.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CodeInterpreter],
            tools_folder="./tools"
        )
