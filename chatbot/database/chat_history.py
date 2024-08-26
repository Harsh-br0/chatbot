import os

from langchain_mongodb import MongoDBChatMessageHistory

from ..defaults import (
    CHAT_HISTORY_COLLECTION_NAME,
    CHAT_HISTORY_HISTORY_KEY,
    CHAT_HISTORY_SESSION_KEY,
    DB_NAME,
)


def get_session_history(session_id: str):
    history = MongoDBChatMessageHistory(
        os.environ["MONGO_URL"],
        session_id,
        DB_NAME,
        CHAT_HISTORY_COLLECTION_NAME,
        session_id_key=CHAT_HISTORY_SESSION_KEY,
        history_key=CHAT_HISTORY_HISTORY_KEY,
    )
    return history
