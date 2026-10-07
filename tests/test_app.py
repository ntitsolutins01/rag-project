"""Testes unitários que não dependem de modelos nem de API key."""
from src.chunking.chunker import chunk_documents, split_text
from src.ingestion.loader import load_directory
from src.prompts.prompt_templates import build_user_prompt


def test_split_text_respeita_tamanho():
    text = "Frase de teste. " * 200
    chunks = split_text(text, chunk_size=300, chunk_overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 300 for c in chunks)


def test_overlap_invalido():
    try:
        split_text("abc", chunk_size=10, chunk_overlap=10)
        assert False
    except ValueError:
        pass


def test_chunk_documents_gera_ids_unicos():
    docs = [{"source": "a.txt", "text": "Olá mundo. " * 100}]
    chunks = chunk_documents(docs, 200, 20)
    ids = [c["id"] for c in chunks]
    assert len(ids) == len(set(ids))


def test_load_directory(tmp_path):
    (tmp_path / "nota.txt").write_text("conteúdo", encoding="utf-8")
    docs = load_directory(tmp_path)
    assert docs == [{"source": "nota.txt", "text": "conteúdo"}]


def test_prompt_contem_pergunta_e_fonte():
    prompt = build_user_prompt("O que é RAG?", [{"source": "doc.pdf", "text": "RAG é..."}])
    assert "O que é RAG?" in prompt and "[doc.pdf]" in prompt
