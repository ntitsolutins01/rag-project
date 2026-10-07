"""Divide textos em chunks menores com sobreposição."""


def split_text(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> list[str]:
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap deve ser menor que chunk_size")

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        # tenta cortar em final de frase/parágrafo para não quebrar ideias
        if end < len(text):
            cut = max(text.rfind("\n", start, end), text.rfind(". ", start, end))
            if cut > start + chunk_size // 2:
                end = cut + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - chunk_overlap, start + 1)
    return chunks


def chunk_documents(docs: list[dict], chunk_size: int, chunk_overlap: int) -> list[dict]:
    """Recebe [{'source','text'}] e devolve [{'id','source','text'}]."""
    result = []
    for doc in docs:
        for i, chunk in enumerate(split_text(doc["text"], chunk_size, chunk_overlap)):
            result.append(
                {"id": f"{doc['source']}::{i}", "source": doc["source"], "text": chunk}
            )
    return result
