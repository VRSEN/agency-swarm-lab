from pathlib import Path
from agency_swarm import Agency
from .AIProjectManager import AIProjectManager
from firebase_admin import initialize_app, credentials, firestore

from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[1] / ".env")

# Authenticate on firebase
service_account_key = "ai-project-manager-3ee92-firebase-adminsdk-7n7x9-638f0af4e4.json"

client_credentials = credentials.Certificate(service_account_key)
initialize_app(client_credentials)
db = firestore.client()


ai_project_manager = AIProjectManager()


def get_threads_from_db(conversation_id):
    doc = db.collection(u'slack-chats').document(conversation_id).get()

    if doc.exists:
        return doc.to_dict()['threads']
    else:
        return {}


def save_threads_to_db(conversation_id, threads):
    db.collection(u'slack-chats').document(conversation_id).set({
        u'threads': threads
    })


def generate_response(message, conversation_id):
    agency = Agency(
        [ai_project_manager],
        shared_instructions="./agency_manifesto.md",
        threads_callbacks={
            "load": lambda: get_threads_from_db(conversation_id),
            "save": lambda threads: save_threads_to_db(conversation_id, threads),
        },
        settings_path=str(Path(__file__).parent / "settings.json")
    )

    completion = agency.get_completion(message, yield_messages=False)
    return completion

if __name__ == "__main__":
    print(generate_response("Hello", "test_channel_id:test_thread_id"))