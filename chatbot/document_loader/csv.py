import os

from langchain_community.document_loaders import CSVLoader as RawCSVLoader

from .utils import get_splitter


class CSVLoader:
    def __init__(self) -> None:
        self.splitter = get_splitter()

    def load(self, path: str):
        csv = RawCSVLoader(path)
        for row in csv.lazy_load():
            for idx, chunk in enumerate(self.splitter.transform_documents([row])):
                chunk.metadata = {
                    "source": (
                        f"{os.path.basename(chunk.metadata['source'])}"
                        f":{chunk.metadata['row']}"
                        f":{idx}"
                    )
                }
                yield chunk
