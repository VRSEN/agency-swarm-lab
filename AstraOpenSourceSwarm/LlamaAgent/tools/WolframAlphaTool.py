from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import json, os

class WolframAlphaTool(BaseTool):
    """
    Tool to query Wolfram Alpha API and process the response.
    """
    query: str = Field(..., description="Query string for the search")

    def run(self) -> str:
        api_key = os.getenv("WOLFRAM_ALPHA_API_KEY")
        url = "https://api.wolframalpha.com/v2/query"
        params = {
            "input": self.query,
            "appid": api_key,
            "format": "plaintext",
            "output": "json",
        }
        response = requests.get(url, params=params)
        return json.dumps(self._clean_wolfram_alpha_response(response.json()))

    def _clean_wolfram_alpha_response(self, wa_response):
        remove = {
            "queryresult": [
                "datatypes",
                "error",
                "timedout",
                "timedoutpods",
                "numpods",
                "timing",
                "parsetiming",
                "parsetimedout",
                "recalculate",
                "id",
                "host",
                "server",
                "related",
                "version",
                {
                    "pods": [
                        "scanner",
                        "id",
                        "error",
                        "expressiontypes",
                        "states",
                        "infos",
                        "position",
                        "numsubpods",
                    ]
                },
                "assumptions",
            ],
        }
        for main_key in remove:
            for key_to_remove in remove[main_key]:
                try:
                    if key_to_remove == "assumptions":
                        if "assumptions" in wa_response[main_key]:
                            del wa_response[main_key][key_to_remove]
                    if isinstance(key_to_remove, dict):
                        for sub_key in key_to_remove:
                            if sub_key == "pods":
                                for i in range(len(wa_response[main_key][sub_key])):
                                    if wa_response[main_key][sub_key][i]["title"] == "Result":
                                        del wa_response[main_key][sub_key][i + 1 :]
                                        break
                            sub_items = wa_response[main_key][sub_key]
                            for i in range(len(sub_items)):
                                for sub_key_to_remove in key_to_remove[sub_key]:
                                    if sub_key_to_remove in sub_items[i]:
                                        del sub_items[i][sub_key_to_remove]
                    elif key_to_remove in wa_response[main_key]:
                        del wa_response[main_key][key_to_remove]
                except KeyError:
                    pass
        return wa_response
