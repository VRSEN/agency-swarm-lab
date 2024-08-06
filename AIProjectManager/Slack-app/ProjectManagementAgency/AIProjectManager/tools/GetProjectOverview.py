from agency_swarm.tools import BaseTool
import requests
import os

from dotenv import load_dotenv
load_dotenv()

# Define your Notion API key and the base URL for the Notion API
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
PAGE_ID = os.getenv("PAGE_ID")
NOTION_API_URL = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children?page_size=200"

class GetProjectOverview(BaseTool):
    """
    Retrieves the 'overview' section of a given Notion page.
    This tool fetches the content of the 'overview' section from a specified Notion page using the Notion API.
    """

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method fetches the 'overview' section from the specified Notion page.
        """
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Notion-Version": "2022-06-28"
        }

        response = requests.get(NOTION_API_URL, headers=headers)

        if response.status_code != 200:
            return f"Failed to retrieve page: {response.status_code} - {response.text}"

        blocks = response.json().get("results", [])

        # Find the callout block with Overview text
        overview_id = None
        for block in blocks:
            if (
                block.get("type") == "callout"
                and block["callout"]["rich_text"][0]["plain_text"] == "Overview"
            ):
                overview_id = block["id"]
                break

        if not overview_id:
            return "Overview section not found."

        # Get overview block content
        url = f"https://api.notion.com/v1/blocks/{overview_id}/children?page_size=200"
        response = requests.get(url, headers=headers)
        blocks = response.json().get("results", [])
        out_text = self.parse_blocks(blocks, headers)

        return out_text
    
    def parse_blocks(self, blocks, headers, line_start=""):
        page_text = ""
        numbered_list_index = 0

        for block in blocks:
            # Notion API does not return index for list items
            if block.get("type") == "numbered_list_item":
                numbered_list_index += 1
            else:
                numbered_list_index = 0

            parsed_text = self.extract_text(block)

            if numbered_list_index > 0:
                parsed_text = f"{numbered_list_index}. {line_start}{parsed_text}"
            else:
                parsed_text = line_start + parsed_text

            page_text += parsed_text + "\n"

            # Recursively extract text for block children
            if block.get("has_children"):
                children = self.get_children(block["id"], headers)
                children_text = self.parse_blocks(children, headers, line_start + "\t")
                page_text += f"{children_text}\n"

        return page_text

    @staticmethod
    def get_children(block_id, headers):
        url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=200"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            return []

    @staticmethod
    def extract_text(block):
        block_type = block.get("type")

        if block_type == "divider":
            return "---"

        block_text = ""
        for text in block[block_type]["rich_text"]:
            field_text = text["plain_text"]

            # Convert styling to markdown
            if text["annotations"]["code"]:
                field_text = f"`{field_text}`"
            if text["annotations"]["italic"]:
                field_text = f"*{field_text}*"
            if text["annotations"]["bold"]:
                field_text = f"**{field_text}**"
            if text["annotations"]["underline"]:
                field_text = f"<u>{field_text}</u>"
            if text["annotations"]["strikethrough"]:
                field_text = f"~~{field_text}~~"

            # Apply type formatting
            if "heading" in block_type:
                heading_level = "#" * int(block_type.split("_")[-1])
                field_text = heading_level + " " + field_text
            if "bulleted_list_item" in block_type:
                field_text = "- " + field_text
            if "to_do" in block_type:
                if block[block_type]["checked"]:
                    field_text = "- [x] " + field_text
                else:
                    field_text = "- [ ] " + field_text

            block_text += field_text

        return block_text
    
if __name__ == "__main__":
    tool = GetProjectOverview()
    print(tool.run())