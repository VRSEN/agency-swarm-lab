from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import json
import os

class BraveSearchTool(BaseTool):
    """
    A tool that queries the Brave Search API and returns a cleaned response.
    """
    query: str = Field(..., description="The query to be sent to the Brave Search API.")

    def run(self):
        """
        Executes the query against the Brave Search API and returns the cleaned response.
        """
        api_key = os.getenv("BRAVE_SEARCH_API_KEY")
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "X-Subscription-Token": api_key,
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
        }
        payload = {"q": self.query}
        response = requests.get(url=url, params=payload, headers=headers)
        response_json = response.json()
        cleaned_response = self._clean_brave_response(response_json)
        return json.dumps(cleaned_response)

    def _clean_brave_response(self, search_response, top_k=3):
        query = None
        clean_response = []
        if "query" in search_response:
            if "original" in search_response["query"]:
                query = search_response["query"]["original"]
        if "mixed" in search_response:
            mixed_results = search_response["mixed"]
            for m in mixed_results["main"][:top_k]:
                r_type = m["type"]
                results = search_response[r_type]["results"]
                if r_type == "web":
                    # For web data - add a single output from the search
                    idx = m["index"]
                    selected_keys = [
                        "type",
                        "title",
                        "url",
                        "description",
                        "date",
                        "extra_snippets",
                    ]
                    cleaned = {
                        k: v for k, v in results[idx].items() if k in selected_keys
                    }
                elif r_type == "faq":
                    # For faq data - take a list of all the questions & answers
                    selected_keys = ["type", "question", "answer", "title", "url"]
                    cleaned = []
                    for q in results:
                        cleaned.append(
                            {k: v for k, v in q.items() if k in selected_keys}
                        )
                elif r_type == "infobox":
                    idx = m["index"]
                    selected_keys = [
                        "type",
                        "title",
                        "url",
                        "description",
                        "long_desc",
                    ]
                    cleaned = {
                        k: v for k, v in results[idx].items() if k in selected_keys
                    }
                elif r_type == "videos":
                    selected_keys = [
                        "type",
                        "url",
                        "title",
                        "description",
                        "date",
                    ]
                    cleaned = []
                    for q in results:
                        cleaned.append(
                            {k: v for k, v in q.items() if k in selected_keys}
                        )
                elif r_type == "locations":
                    selected_keys = [
                        "type",
                        "title",
                        "url",
                        "description",
                        "coordinates",
                        "postal_address",
                        "contact",
                        "rating",
                        "distance",
                        "zoom_level",
                    ]
                    cleaned = []
                    for q in results:
                        cleaned.append(
                            {k: v for k, v in q.items() if k in selected_keys}
                        )
                elif r_type == "news":
                    selected_keys = [
                        "type",
                        "title",
                        "url",
                        "description",
                    ]
                    cleaned = []
                    for q in results:
                        cleaned.append(
                            {k: v for k, v in q.items() if k in selected_keys}
                        )
                else:
                    cleaned = []

                clean_response.append(cleaned)

        return {"query": query, "top_k": clean_response}
