from agency_swarm.agents import Agent
from agency_swarm.tools import CodeInterpreter


class ReportGenerator(Agent):
    def __init__(self):
        super().__init__(
            name="ReportGenerator",
            description="Generates comprehensive reports based on analysis results provided by the Code Analyzer. These reports detail adherence to quality standards and any deviations found.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CodeInterpreter],
            tools_folder="./tools"
        )
