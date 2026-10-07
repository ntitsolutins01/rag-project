"""Operações no banco vetorial (ChromaDB). Troque aqui por Pinecone/FAISS se quiser."""
from pathlib import Path

import chromadb

from src.utils.helpers import ROOT_DIR


class VectorStore:
    def __init__(self, persist_directory: str, collection_name: str):
        path = Path(persist_directory)
        if not path.is_absolute():
            path = ROOT_DIR / path
        self.client = chromadb.PersistentClient(path=str(path))
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    def add(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        self.collection.upsert(
            ids=[c["id"] for c in chunks],
            documents=[c["text"] for c in chunks],
            metadatas=[{"source": c["source"]} for c in chunks],
            embeddings=embeddings,
        )

    def search(self, query_embedding: list[float], top_k: int = 4) -> list[dict]:
        res = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return [
            {"text": doc, "source": meta["source"], "distance": dist}
            for doc, meta, dist in zip(
                res["documents"][0], res["metadatas"][0], res["distances"][0]
            )
        ]

    def count(self) -> int:
        return self.collection.count()

    def reset(self, collection_name: str) -> None:
        self.client.delete_collection(collection_name)
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )
