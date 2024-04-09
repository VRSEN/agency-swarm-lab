from instructor import llm_validator

from agency_swarm.agents import Agent


class PlannerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            description="CEO of CodeSolutionAgency responsible for overseeing and planning the execution of specific coding tasks.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools"
        )

    def response_validator(self, message):
        try:
            llm_validator(statement="Assess whether the message confirms the successful completion of the specified task. "
                                    "The message should explicitly state that the task has been fully "
                                    "completed, without implying that the process has merely started or that the agent "
                                    "awaits additional directives. In the event of any complications, include in the "
                                    "'reason' argument detailed advice on how to proceed.",
                          openai_client=self.client)(message)
        except Exception as e:
            raise ValueError(f"Error: '{e}'.\n"
                             f"Remember, you must continue sending messages to agents until the task is fully completed.")

        return message
