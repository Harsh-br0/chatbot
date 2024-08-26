import os

from .utils import get_splitter


class TextLoader:
    def __init__(self) -> None:
        self.splitter = get_splitter()

    def load(self, path: str):
        with open(path) as f:
            src_file = os.path.basename(path)
            count = 0
            while data := f.read(self.splitter._chunk_size * 2):
                splitted_text = self.splitter.split_text(data)
                for idx, chunk in enumerate(self.splitter.create_documents(splitted_text)):
                    if len(chunk.page_content.strip()) > 0:
                        chunk.metadata = {"source": f"{src_file}:{2 * count + idx}"}
                        yield chunk
                count += 1
