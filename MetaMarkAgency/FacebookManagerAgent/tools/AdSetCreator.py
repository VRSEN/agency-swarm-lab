from datetime import datetime, timedelta

from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import facebook_business.exceptions
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet

from dotenv import load_dotenv
load_dotenv()

access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
app_id = os.getenv('FACEBOOK_APP_ID')
app_secret = os.getenv('FACEBOOK_APP_SECRET')
ad_account_id = os.getenv('FACEBOOK_AD_ACCOUNT_ID')

FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

class AdSetCreator(BaseTool):
    """
    Tool for creating ad sets within a Facebook campaign.
    """
    name: str = Field(..., description='Name of the ad set.')
    budget: int = Field(..., description='Daily budget for the ad set in cents.')

    def run(self):
        try:
            if not self.shared_state.get('campaign_id'):
                raise ValueError('Campaign ID not found. Please use AdCampaignStarter tool first.')

            ad_account = AdAccount(ad_account_id)
            params = {
                'campaign_id': self.shared_state.get('campaign_id'),
                'name': self.name,
                'targeting': {"geo_locations": {"countries": ["US"]}},
                'start_time': datetime.today().isoformat(),
                'end_time': (datetime.today() + timedelta(days=7)).isoformat(),
                'status': AdSet.Status.active,
                "billing_event": "IMPRESSIONS",
                'optimization_goal': "LINK_CLICKS",
                "bid_amount": "100",
            }
            ad_set = ad_account.create_ad_set(params=params)
            self.shared_state.set('ad_set_id', ad_set["id"])
            return f'Ad set {self.name} has been successfully created with ID {ad_set["id"]}.'
        except facebook_business.exceptions.FacebookRequestError as e:
            return f'Error creating ad set: {e}'

if __name__ == "__main__":
    tool = AdSetCreator(name="Test Ad Set", budget=1000)
    tool.shared_state.set('campaign_id', '120207371826520118')
    print(tool.run())
