"""Recupera os chunks mais relevantes por similaridade."""


class Retriever:
    def __init__(self, embedder, vector_store, top_k: int = 4):
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, question: str) -> list[dict]:
        query_embedding = self.embedder.embed_query(question)
        return self.vector_store.search(query_embedding, self.top_k)
