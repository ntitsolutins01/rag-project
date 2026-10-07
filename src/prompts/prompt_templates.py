"""Templates de prompt do sistema RAG."""

SYSTEM_PROMPT = (
    "Você é um assistente que responde perguntas usando SOMENTE o contexto fornecido. "
    "Se a resposta não estiver no contexto, diga claramente que não encontrou a "
    "informação nos documentos. Responda no mesmo idioma da pergunta e cite as "
    "fontes entre colchetes, por exemplo [arquivo.pdf]."
)

USER_TEMPLATE = """Contexto:
{context}

Pergunta: {question}"""


def format_context(chunks: list[dict]) -> str:
    return "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in chunks)


def build_user_prompt(question: str, chunks: list[dict]) -> str:
    return USER_TEMPLATE.format(context=format_context(chunks), question=question)
