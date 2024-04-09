from typing import Literal, List

from instructor import OpenAISchema

from agency_swarm import get_openai_client
from agency_swarm.tools import BaseTool
from pydantic import Field, field_validator, model_validator
import os
import openai


class Step(OpenAISchema):
    name: str = Field(..., description="The name of the step. Do not include maintenance or placeholder steps.")
    agent: Literal['Devid', 'Browsing Agent'] = Field(..., description="The agent responsible for this step.")
    task: str = Field(...,
                      description="The task to be performed in this step. Focus on a high-level description, rather than detailed implementation.")

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v):
        if "maintenance" in v.lower() or "placeholder" in v.lower():
            raise ValueError("Do not include steps for maintenance, or placeholders.")
        return v


class ExecutionPlan(OpenAISchema):
    step: List[Step] = Field(..., description="A step in the execution plan.")

    def format(self):
        return "\n".join([f"{i + 1}. {step.name}\nAgent: {step.agent}\nTask: {step.task}" for i, step in enumerate(self.step)])


class CreatePlan(BaseTool):
    """
    This tool creates a structured execution plan for coding tasks.
    """
    coding_task_description: str = Field(
        ..., description="A clear description of the coding task for which an execution plan is required."
    )

    def run(self) -> str:
        client = get_openai_client()

        execution_plan = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        """As a seasoned software engineering manager, you are tasked with devising an execution strategy for a coding project requested by the user. Your resources include a Browsing Agent capable of conducting research, such as locating API documentation, and a Coding Agent (Devid) skilled in writing and executing code. Construct a concise, step-by-step plan for accomplishing the task with the following guidelines:

- Resort to the Browsing Agent exclusively for engaging with unfamiliar libraries or APIs.
- Refrain from delving into code or specifics of implementation.
- Focus on outlining a strategic plan at a high level, avoiding any code snippets.
- Exclude steps related to documentation or maintenance of the resulting code.
- Do not break down the task into too many granular steps. Agents can determine the specifics during execution.

The aim is to streamline the planning process, ensuring it's both efficient and directly focused on task completion."""
                    )
                },
                {"role": "user", "content": f"Task: '{self.coding_task_description}'"}
            ],
            response_model=ExecutionPlan,
            max_retries=5,
        )

        return execution_plan.format()


if __name__ == "__main__":
    tool = CreatePlan(coding_task_description="I would like you to benchmark Llama 2 on three different providers: Together, Replicate, and Perplexity. Instruct BrowsingAgent to determine their API formats and export their documentation pages as files. Then, pass these file IDs to Devid. Inform Devid that he must first read these files using the myfiles_browser tool and then write a script that sends the same prompt/parameters to all of them. API keys are stored in the following environment variables: REPLICATE_API_KEY, TOGETHER_API_KEY, PERPLEXITY_API_KEY. Please do not report back to me until the task is completed.")
    print(tool.run())
