import os

from pymongo import MongoClient
from pymongo.collection import Collection

from ..defaults import DB_NAME

client = MongoClient(os.environ["MONGO_URL"])
db = client[DB_NAME]


def get_collection(name: str) -> Collection:
    return db[name]


# useless now since mongodb have issues with index management service
# https://www.mongodb.com/community/forums/t/error-connecting-to-search-index-management-service/270272
def ensure_index(col: Collection, model: dict):
    if col.count_documents({}) == 0:
        return False

    index_name = model.get("name")
    if index_name is not None:
        if len(tuple(col.list_search_indexes(index_name))) == 0:
            col.create_search_index(model)

        return True

    return False
