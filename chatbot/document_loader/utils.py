from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..defaults import SPLITTER_CHUNK_OVERLAP, SPLITTER_CHUNK_SIZE


def get_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=SPLITTER_CHUNK_SIZE,
        chunk_overlap=SPLITTER_CHUNK_OVERLAP,
        length_function=len,
    )
