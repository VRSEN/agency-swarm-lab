from agency_swarm.tools import BaseTool
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from pydantic import Field
import os
import facebook_business
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.exceptions import FacebookRequestError

from dotenv import load_dotenv
load_dotenv()

access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
app_id = os.getenv('FACEBOOK_APP_ID')
app_secret = os.getenv('FACEBOOK_APP_SECRET')
ad_account_id = os.getenv('FACEBOOK_AD_ACCOUNT_ID')

FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

class AdPerformanceMonitor(BaseTool):
    """
    Enables monitoring of ad performance on Facebook, including metrics like clicks, impressions, and conversion rates.
    """
    ad_id: str = Field(
        ..., description="The ID of the ad to monitor."
    )
    fields: list = Field(
        ["impressions", "clicks", "spend"], description="The fields to retrieve from the ad insights."
    )

    def run(self):
        try:
            ad = Ad(self.ad_id)
            params = {
                "date_preset": "maximum",
            }
            return ad.get_insights(fields=self.fields,params=params)
        except FacebookRequestError as e:
            return f"Error accessing ad performance metrics: {e.api_error_message()}"

if __name__ == "__main__":
    tool = AdPerformanceMonitor(ad_id="23853583733130117")
    print(tool.run())