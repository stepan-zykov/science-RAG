# Science-RAG 


RAG is a powerful tool that allows users to ask questions to an LLM and receive precise answers derived from their custom datasets. The project leverages advanced natural language processing and retrieval-augmented generation techniques to enhance the accuracy and relevance of responses.

# Core Components
## LLM
### Model: Yandex GPT model.
### Provides the language generation capabilities required for answering questions effectively.
## Embeddings Model
### Model: Yandex GPT text-search-query embeddings.
### Specializes in document retrieval for Russian-language datasets, ensuring efficient and accurate lookups.
## Vector Database
### Provider: Upstash (Free Tier).
### Used to store and search vectorized representations of documents, enabling fast and scalable similarity matching.
## Redis for Rate Limiting
### Provider: Upstash (Free Tier).
### Ensures API stability by limiting the number of requests per user in a given time window.
## API Framework
### Framework: FastAPI.
### Provides a robust and high-performance API layer for serving user queries.
