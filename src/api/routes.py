"""Endpoints FastAPI do sistema RAG."""
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.chunking.chunker import chunk_documents
from src.ingestion.loader import load_directory, load_source
from src.prompts.prompt_templates import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger("rag.api")


class AskRequest(BaseModel):
    question: str


class IngestRequest(BaseModel):
    source: str | None = None  # caminho de arquivo ou URL; vazio = pasta data/


def create_router(config, embedder, vector_store, retriever, llm) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health():
        return {"status": "ok", "chunks_indexados": vector_store.count()}

    @router.post("/ingest")
    def ingest(req: IngestRequest):
        docs = [load_source(req.source)] if req.source else load_directory(
            config["ingestion"]["data_dir"]
        )
        if not docs:
            raise HTTPException(404, "Nenhum documento encontrado para ingestão.")
        chunks = chunk_documents(
            docs,
            config["chunking"]["chunk_size"],
            config["chunking"]["chunk_overlap"],
        )
        vector_store.add(chunks, embedder.embed_documents([c["text"] for c in chunks]))
        logger.info("Ingeridos %d documentos / %d chunks", len(docs), len(chunks))
        return {"documentos": len(docs), "chunks": len(chunks)}

    @router.post("/ask")
    def ask(req: AskRequest):
        chunks = retriever.retrieve(req.question)
        if not chunks:
            return {"answer": "Nenhum documento indexado ainda.", "sources": []}
        answer = llm.generate(SYSTEM_PROMPT, build_user_prompt(req.question, chunks))
        logger.info("Pergunta respondida: %s", req.question)
        return {"answer": answer, "sources": sorted({c["source"] for c in chunks})}

    return router
