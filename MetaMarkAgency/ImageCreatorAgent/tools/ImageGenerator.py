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

    ad_copy: str = Field(
        ..., description="The ad copy to base the image on."
    )
    theme: str = Field(
        ..., description="The specific theme or visual goals for the image."
    )
    specific_requests: str = Field(
        None, description="Any specific requests related to the image creation."
    )

    def run(self):
        client = get_openai_client()
        client.timeout = 120
        prompt = f"Create an image that visually represents: {self.ad_copy}. Theme: {self.theme}. {('Specific requests: ' + self.specific_requests) if self.specific_requests else ''}"
        response = client.images.generate(
                  model="dall-e-3",
                  prompt=prompt,
                  n=1,
                  size="1024x1024",
                response_format="b64_json",
                )

        self.save_image(response.data[0].b64_json)

        client.timeout = 4

        return "Image created successfully. You can now proceed with creating ads"

    def save_image(self, image_data):
        with open("image.png", "wb") as f:
            f.write(base64.b64decode(image_data))
            f.close()

        self.shared_state.set("image_path", os.path.abspath("image.png"))

if __name__ == "__main__":
    tool = ImageGenerator(ad_copy="A beautiful sunset", theme="Nature",
                          specific_requests="Include a river in the image.")
    tool.run()

    print(tool.shared_state.get("image_path"))



