import re
import os
import time
import base64

from agency_swarm.agents import Agent
from typing_extensions import override
from playwright.sync_api import sync_playwright

from agency_swarm.agents.BrowsingAgent.tools.util.selenium import selenium_config

selenium_config["full_page_screenshot"] = False

class Designer(Agent):
    def __init__(self):
        self.SCREENSHOT_FILE_NAME = "screenshot.jpg"
        super().__init__(
            name="Designer",
            description="An agent that analyzes the current browser window for WebDevCrafters.",
            instructions="./instructions.md",
            # files_folder="./files",
            # schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )
        self.prev_message = ""

    @override
    def response_validator(self, message):
        from agency_swarm.agents.BrowsingAgent.tools.util import get_web_driver, get_b64_screenshot

        # Filter out everything in square brackets
        filtered_message = re.sub(r'\[.*?\]', '', message).strip()
        
        if filtered_message and self.prev_message == filtered_message:
            raise ValueError("Do not repeat yourself. If you are stuck, try a different approach or search in google for the page you are looking for directly.")
        
        self.prev_message = filtered_message

        if "[send screenshot]" in message.lower():
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)  # Use Chromium in headless mode
                page = browser.new_page()
                page.goto("http://localhost:3000")
                
                # Wait for all images and resources to be fully loaded
                page.wait_for_load_state('networkidle')

                # Take a full-page screenshot
                screenshot = page.screenshot(full_page=True, type='png')
                
                # Save the screenshot to a file
                with open(self.SCREENSHOT_FILE_NAME, "wb") as screenshot_file:
                    screenshot_file.write(screenshot)
                
                print("Screenshot taken")
                browser.close()
                response_text = "Here is the screenshot of the current web page:"
        else:
            return message

        content = self.create_response_content(response_text)
        raise ValueError(content)        

    def create_response_content(self, response_text):
        with open(self.SCREENSHOT_FILE_NAME, "rb") as file:
            file_id = self.client.files.create(
                file=file,
                purpose="vision",
            ).id

        content = [
            {"type": "text", "text": response_text},
            {
                "type": "image_file",
                "image_file": {"file_id": file_id}
            }
        ]
        return content
    
    def wait_for_images_to_load(self, wd):
        # Wait until all images are loaded
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wd.execute_script("window.scrollTo(0, 0);")
        wd.execute_script("""
            return Array.from(document.images).every((img) => img.complete);
        """)
        time.sleep(2)  # Add a short delay to ensure images are rendered
