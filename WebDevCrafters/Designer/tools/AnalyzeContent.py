import base64
import os
import signal
import subprocess

import agency_swarm.agents.BrowsingAgent.tools.util.selenium
from agency_swarm.tools import BaseTool
from pydantic import Field

agency_swarm.agents.BrowsingAgent.tools.util.selenium.selenium_config = {
    "chrome_profile_path": None,
    "headless": True,
    "full_page_screenshot": True,
}

from agency_swarm.agents.BrowsingAgent.tools.util import get_web_driver, get_b64_screenshot
from agency_swarm.util import get_openai_client


class AnalyzeContent(BaseTool):
    """
    This tool analyzes the current website content developed by the Web Developer agent.
    By asking questions you can ensure that the current website matches your requirements.
    You can only use this tool after the web developer agent has developed the website.
    """
    question: str = Field(
        ..., description="Question to ask about the contents of the current webpage."
    )

    def run(self):
        wd = get_web_driver()

        # make sure to run the web dev server first
        wd.get("http://localhost:3000")

        wd = get_web_driver()

        client = get_openai_client()

        screenshot = get_b64_screenshot(wd)

        # save screenshot locally
        # with open("screenshot.png", "wb") as fh:
        #     fh.write(base64.b64decode(screenshot))

        messages = [
            {
                "role": "system",
                "content": "Your primary task is to accurately extract and provide information in response to user queries based on webpage screenshots. ",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{screenshot}",
                    },
                    {
                        "type": "text",
                        "text": f"{self.question}",
                    }
                ]
            }

        ]

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=1024,
        )

        message = response.choices[0].message
        message_text = message.content

        return message_text
