from agency_swarm.tools import BaseTool
from agency_swarm.util import get_openai_client
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class AdCopyGenerator(BaseTool):
    """
    Generates creative and engaging ad copy tailored to target audience demographics, product features, and desired ad tone.
    """

    target_audience: str = Field(
        ..., description="Description of the target audience demographics."
    )
    product_features: str = Field(
        ..., description="Features of the product or service."
    )
    ad_tone: str = Field(
        ..., description="Desired tone of the ad copy."
    )

    def run(self):
        client = get_openai_client()
        prompt = f"""Generate a creative ad copy targeting {self.target_audience}, 
        highlighting the following features: {self.product_features}. 
        The ad should have a {self.ad_tone} tone. Do not output more than 100 characters. 
        Include a headline in your ad in the following format:
        Headline: [Your headline here]
        Ad Copy: [Your ad copy here]"""
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.7,
            max_tokens=250,
        )
        text = response.choices[0].text.strip()
        headline = text.split("Ad Copy:")[0].split("Headline:")[1].strip()
        self.shared_state.set("ad_headline", headline)
        ad_copy = response.choices[0].text.strip().split("Ad Copy:")[1].strip()
        self.shared_state.set("ad_copy", ad_copy)
        return text

if __name__ == "__main__":
    tool = AdCopyGenerator(
        target_audience="young adults",
        product_features="sustainable, affordable, stylish",
        ad_tone="fun, energetic"
    )
    print(tool.run())
