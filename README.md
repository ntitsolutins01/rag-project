## 🤖 RAG Project

> Sistema **RAG (Retrieval-Augmented Generation)** modular em Python: ingestão de documentos → chunking → embeddings → banco vetorial → recuperação semântica → prompt → LLM → resposta com fontes.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-Anthropic-D97757?style=for-the-badge&logo=anthropic&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-FF6B35?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📑 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#️-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Quick Start](#️-quick-start)
- [API REST](#-api-rest)
- [Testes](#-testes)
- [Personalização](#️-personalização)
- [Roadmap](#️-roadmap)
- [Contribuições](#-contribuições)
- [Autor](#-autor)

---

## 📌 Sobre o Projeto

POC de um sistema RAG completo e modular, construído para demonstrar como conectar documentos privados a um LLM sem fine-tuning ou retreinamento.

Os módulos são independentes e trocáveis — banco vetorial, modelo de embeddings e LLM podem ser substituídos alterando apenas um arquivo.

> 📖 Quer entender **como o RAG funciona internamente**? Leia o [guia explicativo completo](docs/como-funciona.md).

---

## 🏗️ Arquitetura

```text
rag-project/
├── 📄 main.py                  # Ponto de entrada (CLI + servidor)
├── 📄 config.yaml              # Configurações centralizadas
├── 📄 requirements.txt
├── 📄 .env                     # Sua chave de API (não versionar)
├── 📁 data/                    # Seus documentos (PDF, CSV, TXT, MD)
├── 📁 chroma_db/               # Banco vetorial persistido (gerado após ingest)
├── 📁 docs/                    # Documentação adicional
│   └── 📄 como-funciona.md    # Explicação didática do fluxo RAG
├── 📁 logs/
├── 📁 tests/
└── 📁 src/
    ├── ingestion/              # Carrega PDFs, CSVs, TXT, MD e URLs
    ├── chunking/               # Divide textos em chunks com overlap
    ├── embeddings/             # Texto → vetor (sentence-transformers, local)
    ├── vectordb/               # ChromaDB (trocável por Pinecone/FAISS)
    ├── retrieval/              # Busca por similaridade semântica
    ├── prompts/                # Templates de prompt
    ├── llm/                    # Cliente do LLM (Claude / Anthropic)
    ├── api/                    # Endpoints FastAPI
    └── utils/                  # Config, logging
```

---

## 🔧 Pré-requisitos

| Ferramenta | Versão mínima |
|------------|---------------|
| **Python** | 3.11+ |
| **pip** | mais recente |
| **ANTHROPIC_API_KEY** | [console.anthropic.com](https://console.anthropic.com) |

---

## ▶️ Quick Start

### 1️⃣ Instalar dependências

```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2️⃣ Configurar a chave de API

```bash
cp .env.example .env
# edite o .env e coloque sua chave:
# ANTHROPIC_API_KEY=sua-chave-aqui
```

### 3️⃣ Adicionar documentos

Coloque seus arquivos (PDF, CSV, TXT ou MD) na pasta `data/`.

### 4️⃣ Indexar e perguntar

```bash
# Indexa os documentos da pasta data/
python main.py ingest

# Faz uma pergunta
python main.py ask "O que é RAG?"

# Sobe a API REST
python main.py serve       # http://localhost:8000/docs
```

---

## 🌐 API REST

Após rodar `python main.py serve`:

| Método | Endpoint | Body | Descrição |
|--------|----------|------|-----------|
| `GET` | `/health` | — | Status e total de chunks indexados |
| `POST` | `/ingest` | `{"source": "arquivo.pdf"}` ou `{}` | Indexa um arquivo, URL ou toda a pasta `data/` |
| `POST` | `/ask` | `{"question": "sua pergunta"}` | Retorna resposta e fontes utilizadas |

> 📖 Documentação interativa (Swagger) em `http://localhost:8000/docs`.

---

## 🧪 Testes

```bash
pytest tests/
```

Os testes são unitários e não dependem de API key nem de modelos: cobrem chunking, ingestão de arquivos e montagem de prompts.

---

## ⚙️ Personalização

Tudo configurável em `config.yaml`:

| Parâmetro | Efeito |
|-----------|--------|
| `llm.model` | Modelo do Claude a usar |
| `llm.temperature` | `0` = determinístico · `1` = mais criativo |
| `embeddings.model` | Modelo de embeddings (local, via sentence-transformers) |
| `chunking.chunk_size` | Tamanho de cada chunk em caracteres |
| `chunking.chunk_overlap` | Sobreposição entre chunks |
| `retrieval.top_k` | Quantos chunks são enviados ao LLM por pergunta |

> Para trocar o banco vetorial (Pinecone, FAISS) edite apenas `src/vectordb/vector_store.py`.  
> Para trocar o LLM (OpenAI, Gemini) edite apenas `src/llm/llm_client.py`.

---

## 🗺️ Roadmap

```text
✅ Fase 1 — MVP
   ├── Ingestão de PDF, CSV, TXT, MD e URLs
   ├── Chunking com overlap configurável
   ├── Embeddings locais (sem custo de API)
   ├── Busca semântica com ChromaDB
   ├── Geração de respostas com Claude
   └── API REST com FastAPI

🚧 Fase 2 — Qualidade
   ├── Testes de integração com banco vetorial real
   ├── Suporte a múltiplas coleções (multi-tenant)
   └── Avaliação de qualidade das respostas (RAG eval)

🔮 Fase 3 — Evoluções
   ├── Troca de banco vetorial via config (sem alterar código)
   ├── Memória de conversa (histórico de perguntas)
   └── Deploy em cloud (Docker + API Gateway)
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um **fork** do repositório
2. Criar uma branch: `git checkout -b feature/minha-feature`
3. Fazer o commit: `git commit -m "feat: adiciona suporte a Pinecone"`
4. Fazer o push: `git push origin feature/minha-feature`
5. Abrir um **Pull Request** 🚀

---

## 📚 Documentação adicional

| Documento | Descrição |
|-----------|-----------|
| 📖 [Como o RAG funciona](docs/como-funciona.md) | Explicação didática do fluxo completo, diagramas e analogias |

---

## 👤 Autor

Feito com 💙 por **Fábio Muniz**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fabiomunizdeveloper/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/ntitsolutins01?tab=repositories)

---

**Versão:** 1.0.0 · **Status:** ✅ POC completa