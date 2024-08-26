## Implemented Suggestions

| Change  | File and Line Numbers | Description |
| ------- | :-------------------: | ----------- |
| Setting CHUNK_SIZE to 400 with k = 4 | `chatbot/defaults.py`:`L13`  |  Added a constant for k = 4. |
|  | `chatbot/defaults.py`:`L19` | Updated the constant from 1000 to 400 |
|  | `chatbot/database/vector_store.py`:`L29` | Imported and used the `K` param constant introduced previously. |
| Adding support for multiple files | `main.py`:`L35-69` | Replaced logic to handle multiple files instead of single one. |
