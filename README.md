### Setup
- Install Dependencies with `pip install -r requirements.txt`.
- Rename `config.env.sample` to `config.env` and fill the vars.
- There's an unexpected issue with mongodb (check [this](https://www.mongodb.com/community/forums/t/error-connecting-to-search-index-management-service/270272)) that wouldn't let us create index programmatically, so we need to create a vector search index manually through atlas console. Follow [this guide](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type/) to create the index for `vector_store` collection with this config below.

    ```
    {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 768,
        "similarity": "cosine"
    }
    ```

### Usage
- Run `python ./main.py`
- Head over to `http://localhost:8080/docs`

### Models Used
- `sentence-transformers/all-mpnet-base-v2`

    It is used for embedding vectors and this will run locally. Initially it will download the model into `models` directory.

- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

    It is the main LLM that being used through the HuggingFace Hub Inference API.


> Note: Since it is using Inference API and a model locally, the setup would be too slow. On my side, it took more than 2 mins exactly to add a document of 45+ pages to vector store and almost 1 min to process the messages with LLM.
