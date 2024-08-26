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
from chatbot.exceptions import ChatBotException, LoaderNotSupported
from chatbot.functions import add_document, ask_question
from chatbot.logging import logger

router = APIRouter()
log = logger(__name__)


def process_file(file: UploadFile):
    if not os.path.isdir(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    new_path = os.path.join(TEMP_DIR, file.filename or "Document.txt")
    with open(new_path, "wb") as f:
        while data := file.file.read(30):
            f.write(data)

    return new_path


def process_files(files: list[UploadFile]):
    paths, mimes = [], []
    errs_with_exts = set()
    for file in files:
        try:
            DocumentLoader.by_type(file.content_type)
            paths.append(process_file(file))
            mimes.append(file.content_type)
        except Exception as e:
            log.exception(e)

            if isinstance(e, LoaderNotSupported):
                errs_with_exts.add(os.path.basename(file.filename or ".unknown"))

    return paths, mimes, errs_with_exts


def post_process_files(paths: list[str], mimes: list[Optional[str]]):
    for path, mime in zip(paths, mimes):
        try:
            add_document(path, mime)
        except Exception:
            log.exception("Error while post processing files..")
        finally:
            os.remove(path)


@router.post("/addDocument")
def add_doc_route(files: list[UploadFile], tasks: BackgroundTasks):
    paths, mimes, errs = process_files(files)
    tasks.add_task(post_process_files, paths, mimes)
    res = {"msg": "Documents are being processed..."}
    if errs:
        res["error"] = "Following extensions are not supported: " + ", ".join(errs)
    return res


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
async def chatbot_exception_handler(request: Request, exc: ChatBotException):
    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(exc))


@app.exception_handler(Exception)
async def base_exception_handler(request: Request, exc: Exception):
    log.exception("FastAPI base exception handler..")
    raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Server Faced some issue, kindly check logs..."
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
