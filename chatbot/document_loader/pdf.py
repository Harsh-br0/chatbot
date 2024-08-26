import os

from langchain_community.document_loaders import PyPDFLoader

from .utils import get_splitter


class PDFLoader:

    def __init__(self) -> None:
        self.splitter = get_splitter()

    def load(self, path: str):
        pdf = PyPDFLoader(path)
        for page in pdf.lazy_load():
            for idx, chunk in enumerate(self.splitter.transform_documents([page])):
                chunk.metadata = {
                    "source": (
                        f"{os.path.basename(chunk.metadata['source'])}"
                        f":{chunk.metadata['page']}"
                        f":{idx}"
                    )
                }
                yield chunk
