"""Ponto de entrada da aplicação RAG.

Uso:
    python main.py serve            # sobe a API em http://localhost:8000/docs
    python main.py ingest           # indexa os arquivos da pasta data/
    python main.py ask "sua pergunta"
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

from src.api.routes import create_router
from src.chunking.chunker import chunk_documents
from src.embeddings.embedder import Embedder
from src.ingestion.loader import load_directory
from src.llm.llm_client import LLMClient
from src.prompts.prompt_templates import SYSTEM_PROMPT, build_user_prompt
from src.retrieval.retriever import Retriever
from src.utils.helpers import load_config, setup_logging
from src.vectordb.vector_store import VectorStore


def build_components():
    config = load_config()
    logger = setup_logging(config)
    embedder = Embedder(config["embeddings"]["model"])
    store = VectorStore(
        config["vectordb"]["persist_directory"], config["vectordb"]["collection_name"]
    )
    retriever = Retriever(embedder, store, config["retrieval"]["top_k"])
    llm_cfg = config["llm"]
    llm = LLMClient(llm_cfg["model"], llm_cfg["max_tokens"], llm_cfg["effort"])
    return config, logger, embedder, store, retriever, llm


def create_app():
    from fastapi import FastAPI

    config, _, embedder, store, retriever, llm = build_components()
    app = FastAPI(title="RAG Project")
    app.include_router(create_router(config, embedder, store, retriever, llm))
    return app


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"

    if cmd == "serve":
        import uvicorn

        uvicorn.run(create_app(), host="0.0.0.0", port=8000)

    elif cmd == "ingest":
        config, logger, embedder, store, *_ = build_components()
        docs = load_directory(config["ingestion"]["data_dir"])
        chunks = chunk_documents(
            docs, config["chunking"]["chunk_size"], config["chunking"]["chunk_overlap"]
        )
        store.add(chunks, embedder.embed_documents([c["text"] for c in chunks]))
        logger.info("Ingeridos %d documentos / %d chunks", len(docs), len(chunks))

    elif cmd == "ask":
        question = " ".join(sys.argv[2:])
        *_, retriever, llm = build_components()
        chunks = retriever.retrieve(question)
        print(llm.generate(SYSTEM_PROMPT, build_user_prompt(question, chunks)))
        print("\nFontes:", ", ".join(sorted({c["source"] for c in chunks})))

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
