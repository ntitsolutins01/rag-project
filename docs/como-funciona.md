# Como o RAG Project funciona

---

## O problema que o RAG resolve

Um LLM como o Claude foi treinado com dados até uma certa data e não conhece **seus documentos privados**. O RAG resolve isso: em vez de retreinar o modelo, você dá a ele os trechos relevantes dos seus documentos no momento da pergunta.

---

## O fluxo em duas fases

### Fase 1 — Ingestão (`python main.py ingest`)

Esta fase acontece uma vez (ou quando você adiciona novos documentos):

```
data/documento.pdf
       │
       ▼
  [loader.py]          Lê o arquivo e extrai o texto puro
       │
       ▼
  [chunker.py]         Divide o texto em pedaços menores (chunks)
                       Ex: chunk de 800 caracteres, com 120 de sobreposição
       │
       ▼
  [embedder.py]        Converte cada chunk em um vetor de números
                       (modelo local: paraphrase-multilingual-MiniLM-L12-v2)
                       "RAG é uma técnica..." → [0.12, -0.45, 0.88, ...]
       │
       ▼
  [vector_store.py]    Salva os vetores + textos no ChromaDB (banco vetorial)
                       Persiste em disco na pasta chroma_db/
```

> **Por que dividir em chunks?** O LLM tem limite de tokens. Mandar o documento inteiro seria caro e impreciso. Chunks menores permitem selecionar só o que é relevante.
>
> **Por que vetores?** Vetores representam o *significado* do texto matematicamente. Textos com significados parecidos ficam próximos no espaço vetorial — isso permite busca por similaridade semântica, não apenas por palavras-chave.

---

### Fase 2 — Pergunta (`python main.py ask "O que é RAG?"`)

Esta fase acontece toda vez que o usuário pergunta:

```
"O que é RAG?"
       │
       ▼
  [embedder.py]        Converte a pergunta em vetor
                       "O que é RAG?" → [0.10, -0.41, 0.90, ...]
       │
       ▼
  [retriever.py]       Busca os 4 chunks mais próximos (top_k=4)
                       no ChromaDB por distância de cosseno
       │
       ▼
  [prompt_templates.py] Monta o prompt combinando:
                        - pergunta do usuário
                        - os 4 chunks encontrados como contexto
       │
       ▼
  [llm_client.py]      Envia para o Claude via API Anthropic
       │
       ▼
  Resposta + fontes    O Claude responde baseado APENAS no contexto fornecido
```

---

## Analogia prática

Imagine um funcionário novo numa empresa:

1. **Ingestão** = ele lê todos os manuais da empresa e grifa os trechos importantes num fichário indexado.
2. **Pergunta** = quando você pergunta algo, ele consulta o fichário, pega os trechos mais relevantes, lê e te responde citando as fontes.

O Claude é o "funcionário" — ele não memorizou os manuais, mas sabe raciocinar sobre o que você coloca na frente dele.

---

## Os componentes e suas responsabilidades

```
┌─────────────────────┬────────────────────────────────────────────────┐
│       Arquivo       │                Responsabilidade                │
├─────────────────────┼────────────────────────────────────────────────┤
│ loader.py           │ Lê PDF, CSV, TXT, MD, URLs                     │
├─────────────────────┼────────────────────────────────────────────────┤
│ chunker.py          │ Divide texto em pedaços com sobreposição       │
├─────────────────────┼────────────────────────────────────────────────┤
│ embedder.py         │ Texto → vetor numérico (modelo local, sem API) │
├─────────────────────┼────────────────────────────────────────────────┤
│ vector_store.py     │ Salva/busca vetores no ChromaDB                │
├─────────────────────┼────────────────────────────────────────────────┤
│ retriever.py        │ Orquestra embedding da query + busca           │
├─────────────────────┼────────────────────────────────────────────────┤
│ prompt_templates.py │ Monta o prompt com contexto                    │
├─────────────────────┼────────────────────────────────────────────────┤
│ llm_client.py       │ Chama a API do Claude                          │
├─────────────────────┼────────────────────────────────────────────────┤
│ routes.py           │ Expõe tudo via HTTP (FastAPI)                  │
├─────────────────────┼────────────────────────────────────────────────┤
│ main.py             │ Ponto de entrada: CLI ou servidor              │
├─────────────────────┼────────────────────────────────────────────────┤
│ config.yaml         │ Controla modelo, tamanho de chunk, top_k etc.  │
└─────────────────────┴────────────────────────────────────────────────┘
```

---

## O que você pode ajustar no `config.yaml`

- **`chunk_size`** — chunks maiores = mais contexto por pedaço, mas menos precisão na busca
- **`chunk_overlap`** — sobreposição evita que uma ideia seja cortada no meio entre dois chunks
- **`top_k`** — quantos chunks o retriever envia para o Claude (mais chunks = mais contexto, mais tokens gastos)
- **`temperature`** — `0` = respostas mais determinísticas; `1` = mais criativas