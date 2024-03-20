import os

from agency_swarm.tools import BaseTool
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError
from pydantic import Field, model_validator

from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
app_id = os.getenv('FACEBOOK_APP_ID')
app_secret = os.getenv('FACEBOOK_APP_SECRET')
ad_account_id = os.getenv('FACEBOOK_AD_ACCOUNT_ID')

FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

class AdCreator(BaseTool):
    """
    Enables scheduling and posting of ads on Facebook with optimal timing and audience targeting.
    """
    name: str = Field(..., description='Headline of the ad.')
    link: str = Field(
        ..., description="The URL to which the ad will direct the user."
    )

    def run(self):
        image = AdImage(parent_id=ad_account_id)
        image[AdImage.Field.filename] = self.shared_state.get('image_path')
        image.remote_create()

        creative = AdCreative(parent_id=ad_account_id)
        creative[AdCreative.Field.title] = self.shared_state.get('ad_headline')
        creative[AdCreative.Field.body] = self.shared_state.get('ad_copy')
        creative[AdCreative.Field.object_story_spec] = {
            'page_id': os.getenv('FACEBOOK_PAGE_ID'),
            'link_data': {
                'image_hash': image.get_hash(),
                "call_to_action": {'type': 'LEARN_MORE'},
                'link': self.link,
                "name": self.shared_state.get('ad_headline'),
                "message": self.shared_state.get('ad_copy'),
            }
        }
        creative[AdCreative.Field.degrees_of_freedom_spec] = {
            'creative_features_spec': {
                'standard_enhancements': {
                    'enroll_status': 'OPT_OUT'
                }
            }
        }
        creative.remote_create()

        ad = Ad(parent_id=ad_account_id)
        ad[Ad.Field.name] = self.name
        ad[Ad.Field.adset_id] = self.shared_state.get('ad_set_id')
        ad[Ad.Field.creative] = creative
        ad.remote_create(params={
            'status': Ad.Status.paused,
        })

        return f"Ad created successfully with ID: {ad['id']}"

    @model_validator(mode="after")
    def validate(self):
        if not self.shared_state.get('image_path'):
            raise ValueError('Please tell Image Creator agent to generate an image first.')

        if not self.shared_state.get('ad_set_id'):
            raise ValueError('Ad set ID not found. Please use AdSetCreator tool first.')

        if not self.shared_state.get('campaign_id'):
            raise ValueError('Campaign ID not found. Please use AdCampaignStarter tool first.')

        if not self.shared_state.get('ad_copy'):
            raise ValueError('Please use AdCopyGenerator tool to generate ad copy first.')

if __name__ == "__main__":
    tool = AdCreator(name="Test Creative 2", ad_text="Check out our new product!",
                    link="https://www.example.com", )
    tool.shared_state.set('image_path', 'image2.png')
    tool.shared_state.set('ad_set_id', '120207414681720118')
    tool.shared_state.set('ad_copy', '123')
    print(tool.run())
