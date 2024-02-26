import json
import os

from agency_swarm.tools import BaseTool
from pydantic import Field
import requests

from dotenv import load_dotenv

load_dotenv()


class GitHubPullRequestFetcher(BaseTool):
    """
    Fetches changes from pull requests in a GitHub repository, focusing on TypeScript files.
    """

    def run(self):
        # Path to the JSON file with GitHub event data
        github_event_path = os.environ['GITHUB_EVENT_PATH']

        # Read and parse the JSON file
        with open(github_event_path, 'r') as file:
            github_event = json.load(file)

        pull_request = github_event['pull_request']['number']

        print("Pull request:", pull_request)

        headers = {"Authorization": "Bearer " + os.environ.get('GITHUB_TOKEN')}
        url = f"https://api.github.com/repos/vrsen-ai-solutions/openai-widget/pulls/{pull_request}/files"

        response = requests.get(url, headers=headers).json()

        ts_files = [file for file in response if file['filename'].endswith('.ts')]

        changes = []
        for file in ts_files:
            changes.append(f"File: {file['filename']}\nChanges:\n{file.get('patch', 'No changes available')}\n\n---\n")

        return changes


if __name__ == "__main__":
    tool = GitHubPullRequestFetcher()
    print(tool.run())