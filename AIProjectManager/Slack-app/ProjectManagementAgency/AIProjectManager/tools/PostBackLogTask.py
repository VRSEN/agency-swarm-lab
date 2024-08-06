from agency_swarm.tools import BaseTool
from pydantic import Field, field_validator
from .util.constants import TASK_TEMPLATE, BACKGROUND_PLACEHOLDER
import requests
import os
import re

from dotenv import load_dotenv
load_dotenv()

# Define your Notion API key and the base URL for the Notion API
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
PAGE_ID = os.getenv("PAGE_ID")
DATABASE_ID = os.getenv("DATABASE_ID")
NOTION_API_URL = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children?page_size=200"

class PostBackLogTask(BaseTool):
    """
    Posts a task with a given title, content, and background to a specified project page in Notion.
    This tool creates a new task in the specified Notion project page using the Notion API.
    """

    task_title: str = Field(
        ..., description="The title of the task to be posted."
    )
    task_content: str = Field(
        ..., description="The content/description of the task to be posted."
    )
    task_background: str = Field(
        ..., description="The background information of the task to be posted."
    )

    @field_validator("task_content")
    def check_content(cls, v):
        # Check that content contains to-do list
        if not ("- [ ]" in v or "- [x]" in v):
            raise ValueError("Input content should contain at least one to-do list.")

        # Check that content doesn't have headings of level 4 or more (not supported in Notion)
        pattern = re.compile(r"^\s*#{4,}", re.MULTILINE)
        match = pattern.search(v)
        if match:
            raise ValueError("Only headings up to level 3 are supported.")

        return v

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method posts a new task to the specified Notion project page.
        """
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        properties = TASK_TEMPLATE.copy()
        
        # Replace placeholders with a title and project
        properties["Task name"]["title"][0]["text"]["content"] = self.task_title
        properties["Task name"]["title"][0]["plain_text"] = self.task_title
        properties["Project"]["relation"][0]["id"] = PAGE_ID

        # Add a Background section to the top of the task
        page_content = BACKGROUND_PLACEHOLDER.copy()
        page_content.extend(self.markdown_to_list(self.task_background))
        page_content.extend(self.markdown_to_list(self.task_content))

        data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": properties,
            "children": page_content,
        }

        url = "https://api.notion.com/v1/pages"
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"Failed to post task: {response.status_code} - {response.text}"

        return "Task posted successfully"
    
    # Splits a given text into a list of formatted blocks
    def markdown_to_list(self, markdown_text):
        lines = markdown_text.split("\n")
        blocks = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line is a part of a numbered list
            numbered_list = False
            pattern = re.compile(r"^\s*(\d+)\.\s+(.*)")
            match = pattern.match(line)
            if match:
                numbered_list = True

            block = {
                "object": "block",
                "type": "",
            }

            if line.startswith("#"):
                heading_level = len(re.match(r"#+", line).group())
                block_type = f"heading_{heading_level}"
                text = line[heading_level:].strip()
                block[block_type] = {"rich_text": self.split_into_segments(text)}
            elif line.startswith("- [x] "):
                block_type = "to_do"
                text = line[6:].strip()
                block[block_type] = {
                    "rich_text": self.split_into_segments(text),
                    "checked": True,
                }
            elif line.startswith("- [ ] "):
                block_type = "to_do"
                text = line[6:].strip()
                block[block_type] = {
                    "rich_text": self.split_into_segments(text),
                    "checked": False,
                }
            elif line.startswith("- "):
                block_type = "bulleted_list_item"
                text = line[2:].strip()
                block[block_type] = {"rich_text": self.split_into_segments(text)}
            elif numbered_list:
                block_type = "numbered_list_item"
                text = match.group(2).strip()
                block[block_type] = {"rich_text": self.split_into_segments(text)}
            else:
                block_type = "paragraph"
                text = line.strip()
                block[block_type] = {"rich_text": self.split_into_segments(text)}

            block["type"] = block_type
            blocks.append(block)

        return blocks
    
    @staticmethod
    def parse_markdown_segment(segment):
        annotations = {
            "bold": False,
            "italic": False,
            "underline": False,
            "strikethrough": False,
            "code": False,
        }

        while True:
            if segment.startswith("**") and segment.endswith("**"):
                annotations["bold"] = True
                segment = segment[2:-2]
                continue
            if segment.startswith("*") and segment.endswith("*"):
                annotations["italic"] = True
                segment = segment[1:-1]
                continue
            if segment.startswith("<u>") and segment.endswith("</u>"):
                annotations["underline"] = True
                segment = segment[3:-4]
                continue
            if segment.startswith("~~") and segment.endswith("~~"):
                annotations["strikethrough"] = True
                segment = segment[2:-2]
                continue
            if segment.startswith("`") and segment.endswith("`"):
                annotations["code"] = True
                segment = segment[1:-1]
                continue
            break

        return {
            "type": "text",
            "text": {"content": segment, "link": None},
            "annotations": annotations,
        }

    def split_into_segments(self, text):
        pattern = re.compile(r"(\*\*.*?\*\*|<u>.*?</u>|~~.*?~~|`.*?`|\*.*?\*)")
        segments = pattern.split(text)
        rich_text_segments = []

        for segment in segments:
            if not segment:
                continue
            if pattern.match(segment):
                rich_text_segments.append(self.parse_markdown_segment(segment))
            else:
                rich_text_segments.append(
                    {
                        "type": "text",
                        "text": {"content": segment, "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "underline": False,
                            "strikethrough": False,
                            "code": False,
                        },
                    }
                )
        return rich_text_segments
    
if __name__ == "__main__":
    markdown_text = """
    # Heading 1
    ## Heading 2
    - [x] Completed task
    - [ ] Incomplete task
    **Bold text**: normal text *Italic text*
    <u>Underlined text</u>
    ~~Strikethrough text~~
    `Code text`
    1. Numbered
    2. List
    3. Example
    Simple text
    - Bullet point
    """
    background = """
    Recap of the client's feedback
    - Some key points
    - That they mentioned
    """
    tool = PostBackLogTask(
        task_title="Test title",
        task_content=markdown_text,
        task_background=background,
    )
    print(tool.run())