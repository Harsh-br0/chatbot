import mimetypes
from typing import Optional

from .chain import rag_chain_with_history
from .database import vector_store
from .document_loader import DocumentLoader
from .exceptions import MimeTypeInvalid
from .logging import logger

log = logger(__name__)


def add_document(path: str, mime: Optional[str] = None):
    if mime is None:
        mime = mimetypes.guess_type(path)[0]
        if mime is None:
            raise MimeTypeInvalid("Invalid Mimetype...")

    loader = DocumentLoader.by_type(mime)
    for docs in loader.load(path):
        vector_store.add_documents(docs)
        log.info(f"Added {len(docs)} docs from path {path}.")

    log.info(f"Added all docs for path {path}")


def ask_question(session_id: str, question: str):
    res = rag_chain_with_history.invoke(
        {"input": question}, config={"configurable": {"session_id": session_id}}
    )
    return res["answer"]
