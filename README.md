# Simple RAG Server Chatbot

A sophisticated chatbot implementation using Retrieval-Augmented Generation (RAG) with FastAPI, MongoDB, and Hugging Face models. This chatbot can process multiple document types, maintain conversation history, and provide context-aware responses.

## Features

- **Document Processing**
  - Support for multiple file uploads
  - Automatic document type detection
  - Chunked text processing with configurable size
  - Vector embeddings for efficient retrieval

- **Chat Capabilities**
  - Context-aware conversations
  - Session management
  - History-aware retrieval system
  - Concise, three-sentence maximum responses

- **Technical Stack**
  - FastAPI for the backend API
  - MongoDB with vector search capabilities
  - Hugging Face models for embeddings and chat
  - LangChain for chain management

## Models Used

- **Embedding Model**: `sentence-transformers/all-mpnet-base-v2`
  - Runs locally
  - Used for generating document embeddings
  - Downloads automatically to `models` directory

- **LLM**: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
  - Accessed through Hugging Face Hub Inference API
  - Used for generating responses

## Setup Instructions

1. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2. **Configuration**
    - Rename `config.env.sample` to `config.env`
    - Fill in the required environment variables

3. **MongoDB Setup**
    > There's an unexpected issue with mongodb (check [this](https://www.mongodb.com/community/forums/t/error-connecting-to-search-index-management-service/270272)) that wouldn't let us create index programmatically, so we need to create a vector search index manually through atlas console. Follow [this guide](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type/) to create the index.

    - Create a vector search index manually through the Atlas console
    - Use the following configuration for the `vector_store` collection: <br/> <br/>

   ```json
    {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 768,
        "similarity": "cosine"
    }
    ```

## Usage

- Start the Server

```bash
python ./main.py
```

- Access the API by navigating to [http://localhost:8080/docs](http://localhost:8080/docs) for Swagger documentation

## Configuration

Key configurations in `defaults.py`:

- `SPLITTER_CHUNK_SIZE`: 400
- `SPLITTER_CHUNK_OVERLAP`: 25
- `RETRIEVER_K_PARAM`: 4
- `MAX_READ_LINES_FOR_TEXT_FILE`: 40

## Performance Note

The system may experience some latency due to:

- Initial model download and loading
- Document processing time
- Inference API response time

> On my side, it took more than 2 mins exactly to add a document of 45+ pages to vector store and almost 1 min to process the messages with LLM.
