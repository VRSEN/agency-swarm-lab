import re
from os import getenv
from pathlib import Path

from openai import OpenAI
from ProjectManagementAgency.agency import generate_response

from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

app = App(
    token=getenv("SLACK_TOKEN"),
    signing_secret=getenv("SLACK_SIGNING_SECRET"),
)
app_handler = SlackRequestHandler(app)
api = FastAPI()

aiclient = OpenAI()


@api.post("/slack/events")
async def endpoint(req: Request):
    body = await req.json()
    # Handle Slack URL verification challenge
    if "challenge" in body:
        print("Authorizing slack endpoint")
        return JSONResponse(content={"challenge": body["challenge"]})
    # Handle other requests via SlackRequestHandler
    return await app_handler.handle(req)


@app.event("app_mention")
@app.event("message")
def handle_message_events(event, say):
    # Filter out system messages
    if "user" not in event:
        return

    event_type = event["type"]
    user_id = event["user"]

    # Fetch the user's info
    user_info = app.client.users_info(user=user_id)
    workspace_id = app.client.auth_test()["team_id"]
    message_text = event.get("text", "")

    # Filter out messages that have mentions or coming from a manager.
    if event_type != "app_mention":
        user_mentions = re.findall(r"<@U[A-Z0-9]+>", message_text)
        if workspace_id == user_info["user"]["team_id"] or user_mentions:
            return

    # Get user's real name
    real_name = user_info["user"]["profile"]["real_name"]

    message = real_name + ": " + message_text
    # Check if the message is not in a thread (i.e., it's a top-level message)
    if event_type == "app_mention" or is_response_required(message):
        if "thread_ts" not in event:
            app.client.chat_postMessage(
                channel=event["channel"],
                text=generate_response(message, event["channel"] + ":" + event["ts"]),
                thread_ts=event["ts"],  # thread id is set to message timestamp
            )
        else:
            say(
                text=generate_response(
                    message, event["channel"] + ":" + event["thread_ts"]
                ),
                thread_ts=event["thread_ts"],
                channel=event["channel"],
            )

    return


def is_response_required(message_input) -> str:
    """
    Get the completion from the LLM model.
    """
    try:
        response = aiclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant responsible for analyzing slack chat messages. "
                        "You work as a part of AI agency that is helping clients automate their businesses."
                        "Your role within that agency is to help manager determine, if they should create "
                        "a new task for developers or not.\n"
                        "Your primary instructions are:\n"
                        "1. Take a chat message from Slack as an input.\n"
                        "2. Analyze the message and determine if user's message requires agency's "
                        "manager to schedule a new task. Specifically, look if contains any feedback, "
                        "has any issues regarding the product or new requirements\n"
                        "3. Clarifications or follow-up questions do not require task creation.\n"
                        "If a new task needs to be created, you need to respond with a single `True` word. "
                        "If it doesn't, respond with a single `False` word."
                    ),
                },
                {
                    "role": "user",
                    "content": message_input,
                },
            ],
            max_tokens=4000,
            temperature=0.0,
        )
        response_value = response.choices[0].message.content
        return "true" in response_value.lower()

    except Exception as e:
        raise ConnectionError(
            f"Error making request to OpenAI: {e}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="0.0.0.0", port=8000)
