from typing import Optional

from ..exceptions import LoaderNotSupported
from ..utils import chunk_iter
from .csv import CSVLoader
from .pdf import PDFLoader
from .text import TextLoader

LOADERS = {
    "application/pdf": PDFLoader,
    "text/csv": CSVLoader,
    "text/plain": TextLoader,
}


class DocumentLoader:

    def __init__(self, loader) -> None:
        self._loader = loader

    @classmethod
    def by_type(cls, mime_type: Optional[str]):
        if mime_type is None or mime_type not in LOADERS:
            raise LoaderNotSupported(f"Files with mime type {mime_type} are not supported...")

        return cls(LOADERS[mime_type]())

    def load(self, path: str, num_docs=20):
        for docs in chunk_iter(self._loader.load(path), num_docs):
            yield list(filter(lambda doc: len(doc.page_content.strip()) > 0, docs))
