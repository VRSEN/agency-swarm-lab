from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import facebook_business.exceptions
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser

from dotenv import load_dotenv
load_dotenv()

access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
app_id = os.getenv('FACEBOOK_APP_ID')
app_secret = os.getenv('FACEBOOK_APP_SECRET')
ad_account_id = os.getenv('FACEBOOK_AD_ACCOUNT_ID')

FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

class AdCampaignStarter(BaseTool):
    """
    Tool for starting ad campaigns on Facebook.
    """

    campaign_name: str = Field(..., description='Name of the ad campaign.')
    budget: int = Field(..., description='Daily budget for the ad campaign in cents.')

    def run(self):
        try:
            ad_account = AdAccount(ad_account_id)
            params = {
                'name': self.campaign_name,
                'objective': "OUTCOME_LEADS",
                'status': Campaign.Status.active,
                'daily_budget': self.budget,
                'special_ad_categories': 'NONE',

            }
            campaign = ad_account.create_campaign(params=params)
            self.shared_state.set('campaign_id', campaign["id"])
            return f'Ad campaign {self.campaign_name} has been successfully started with ID {campaign["id"]}.'
        except facebook_business.exceptions.FacebookRequestError as e:
            return f'Error starting ad campaign: {e}'

if __name__ == "__main__":
    tool = AdCampaignStarter(campaign_name="Test Campaign", budget=1000)
    print(tool.run())

