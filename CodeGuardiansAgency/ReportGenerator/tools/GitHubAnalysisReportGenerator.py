import os

from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import json

from dotenv import load_dotenv
load_dotenv()

class GitHubAnalysisReportGenerator(BaseTool):
    """
    Generates a comprehensive report based on code analysis results and posts it using GitHub API.
    """
    report_content: str = Field(
        ..., description="Analysis results as a string."
    )
    # For markdown file
    file_path: str = Field(
        None, description="The path where the markdown report file should be created or updated."
    )

    def run(self):
        headers = {"Authorization": "Bearer " + os.environ.get('GITHUB_TOKEN')}

        github_event_path = os.environ['GITHUB_EVENT_PATH']

        # Read and parse the JSON file
        with open(github_event_path, 'r') as file:
            github_event = json.load(file)

        pull_request = github_event['pull_request']['number']

        url = f"https://api.github.com/repos/vrsen-ai-solutions/openai-widget/issues/{pull_request}/comments"
        response = requests.post(url, headers=headers, data=json.dumps({"body": self.report_content}))
        
        return response.json()

if __name__ == "__main__":
    tool = GitHubAnalysisReportGenerator(
        report_content="this is a test via api",
    )
    print(tool.run())