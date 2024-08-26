import os
from typing import Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    FastAPI,
    HTTPException,
    Request,
    UploadFile,
    status,
)

from chatbot.defaults import TEMP_DIR
from chatbot.document_loader import DocumentLoader
from chatbot.exceptions import ChatBotException
from chatbot.functions import add_document, ask_question

router = APIRouter()


def process_file(file: UploadFile):
    if not os.path.isdir(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    new_path = os.path.join(TEMP_DIR, file.filename or "Document.txt")
    with open(new_path, "wb") as f:
        while data := file.file.read(30):
            f.write(data)

    return new_path


def post_process_file(path: str, mime: Optional[str]):
    add_document(path, mime)
    os.remove(path)


@router.post("/addDocument")
def add_doc_route(file: UploadFile, tasks: BackgroundTasks):
    # document check
    DocumentLoader.by_type(file.content_type)  # type: ignore
    path = process_file(file)
    tasks.add_task(post_process_file, path, file.content_type)
    return {"msg": "Document is being processed..."}


@router.get("/ask")
def ask_question_route(session_id: str, question: str):
    session_id, question = map(str.strip, [session_id, question])
    if session_id == "" or question == "":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Query params are empty.")
    answer = ask_question(session_id, question)
    return {"output": answer}


app = FastAPI(
    title="Simple RAG Server",
)
app.include_router(router, prefix="/api")


@app.exception_handler(ChatBotException)
async def unicorn_exception_handler(request: Request, exc: ChatBotException):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(exc))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
