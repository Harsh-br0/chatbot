from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch

from ..defaults import (
    MODEL_DIR,
    VECTORSTORE_COLLECTION_NAME,
    VECTORSTORE_EMBEDDING_KEY,
    VECTORSTORE_INDEX_NAME,
    VECTORSTORE_SEARCH_FUNC,
)
from ..logging import logger
from .mongo import get_collection

log = logger(__name__)

embeddings = HuggingFaceEmbeddings(cache_folder=MODEL_DIR)

vector_store = MongoDBAtlasVectorSearch(
    collection=get_collection(VECTORSTORE_COLLECTION_NAME),
    embedding=embeddings,
    index_name=VECTORSTORE_INDEX_NAME,
    embedding_key=VECTORSTORE_EMBEDDING_KEY,
    relevance_score_fn=VECTORSTORE_SEARCH_FUNC,
)


def get_retriever():
    return vector_store.as_retriever(k=3)
