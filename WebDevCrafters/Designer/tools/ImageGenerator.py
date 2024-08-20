from typing import Literal
from agency_swarm.tools import BaseTool
from agency_swarm.util import get_openai_client
from pydantic import Field
import openai
import os
import base64

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ImageGenerator(BaseTool):
    """
    Generates images based on ad copy and specific themes or requests, utilizing DALL-E 3.
    """
    description: str = Field(
        ..., description="The description of the image to be generated."
    )
    section: str = Field(
        ..., description="The section of the website that the image is for.", example="Homepage"
    )
    image_name: str = Field(
        ..., description="Name for the image, without extension."
    )
    dimensions: Literal["1024x1024", "1792x1024", "1024x1792"] = Field(
        "1024x1024", description="The dimensions of the image to be generated.", example="1024x1024"
    )

    def run(self):
        client = get_openai_client()
        client.timeout = 120
        prompt = f"Create an image for a website section: {self.section}. Description: {self.description}"
        response = client.images.generate(
                  model="dall-e-3",
                  prompt=prompt,
                  n=1,
                  size="1024x1024",
                response_format="b64_json",
                )

        self.save_image(response.data[0].b64_json)

        client.timeout = 4

        return "Image created successfully and saved to the assets directory: " + self._shared_state.get("assets_dir", "./assets")

    def save_image(self, image_data):
        if not os.path.exists(self._shared_state.get("assets_dir", "./assets")):
            os.makedirs(self._shared_state.get("assets_dir", "./assets"))
            self._shared_state.set("assets_dir", os.path.abspath("./assets"))
    
        with open(os.path.join(self._shared_state.get("assets_dir", "./assets"), f"{self.image_name}.png"), "wb") as f:
            f.write(base64.b64decode(image_data))
            f.close()

if __name__ == "__main__":
    tool = ImageGenerator(description="A beautiful sunset", section="Homepage", dimensions="1024x1024")
    tool.run()



