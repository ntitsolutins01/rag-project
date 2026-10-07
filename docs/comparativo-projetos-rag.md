# Comparativo: rag-project vs PostGraduate HBR RAG

Este documento compara duas implementações RAG construídas pelo mesmo autor:

- **rag-project** — este repositório: POC modular voltada para produção
- **PostGraduateProgramAIAgentsBusinessApplications** — exercício acadêmico de pós-graduação que responde perguntas sobre o artigo da Harvard Business Review *"How Apple Is Organized for Innovation"*

---

## Visão geral

| | PostGraduate (HBR RAG) | rag-project |
|---|---|---|
| **Propósito** | Exercício acadêmico de pós-graduação | POC de sistema RAG para produção |
| **Formato** | Jupyter Notebook (Google Colab) | Aplicação Python modular |
| **Documento de entrada** | PDF do artigo HBR da Apple (11 pgs) | Qualquer PDF, CSV, TXT, MD ou URL |

---

## 1. Arquitetura

| | PostGraduate | rag-project |
|---|---|---|
| **Estrutura** | Notebook linear, tudo em células sequenciais | Módulos independentes em `src/` com responsabilidade única |
| **Orquestração** | LangChain + LCEL chains | Do zero — sem framework de orquestração |
| **Interface** | Nenhuma (saída no notebook) | CLI (`ingest`, `ask`, `serve`) + API REST (FastAPI) + Swagger |
| **Configuração** | Hardcoded nas células | Centralizada em `config.yaml` |
| **Testes** | Nenhum | 5 testes unitários com pytest |

---

## 2. Stack tecnológica

| Componente | PostGraduate | rag-project |
|---|---|---|
| **LLM** | Mistral-7B-Instruct-v0.2 (open-source, 4-bit quantizado, GPU T4) | Claude Sonnet (Anthropic, via API) |
| **Embeddings** | `all-MiniLM-L6-v2` (inglês, 90MB) | `paraphrase-multilingual-MiniLM-L12-v2` (multilíngue, ~120MB) |
| **Banco vetorial** | ChromaDB via abstração LangChain | ChromaDB direto (sem abstração) |
| **Splitter** | `RecursiveCharacterTextSplitter` do LangChain | Implementação própria com detecção de fronteira de frase |
| **Framework** | LangChain (langchain, langchain-core, langchain-chroma…) | Sem framework — só as libs essenciais |
| **Ambiente** | Google Colab (GPU cloud, gratuito/pago) | Local (CPU Windows) |

---

## 3. Abordagem ao RAG

| | PostGraduate | rag-project |
|---|---|---|
| **Evolução didática** | Mostra 3 fases: sem RAG → prompt engineering → RAG completo | Direto ao RAG completo |
| **Chunking** | `chunk_size=1000`, `chunk_overlap=150`, separadores hierárquicos | `chunk_size=800`, `chunk_overlap=120`, corte em final de frase |
| **top_k** | 4 chunks | 4 chunks (configurável via `config.yaml`) |
| **Metadados** | Número de página do PDF nas fontes | Nome do arquivo nas fontes |
| **Prompt** | Template com instrução de usar APENAS o contexto + bullet points | `SYSTEM_PROMPT` separado + `build_user_prompt` com contexto inline |

---

## 4. Pontos fortes de cada projeto

### PostGraduate — o que ele tem e o rag-project não tem

- **Demonstração progressiva**: mostra as 3 fases do RAG (sem RAG → prompt engineering → RAG+recuperação), ideal para quem está aprendendo
- **LLM open-source**: Mistral-7B rodando localmente na GPU, sem custo de API por token
- **Splitter hierárquico**: `RecursiveCharacterTextSplitter` respeita separadores naturais (`\n\n` → `\n` → `. `)
- **Metadado de página**: o resultado indica de qual página do PDF veio cada trecho recuperado

### rag-project — o que ele tem e o PostGraduate não tem

- **Arquitetura modular e trocável**: troca de LLM ou banco vetorial em 1 arquivo
- **API REST**: endpoints prontos para consumo externo com documentação automática (Swagger)
- **Múltiplos formatos**: suporte nativo a PDF, CSV, TXT, MD e URLs (scraping)
- **Embeddings multilíngues**: funciona bem em português e outros idiomas
- **Testes unitários**: cobertura dos módulos de chunking, ingestion e prompts
- **Configuração externalizada**: todos os parâmetros em `config.yaml`, sem alterar código
- **Documentação estruturada**: README e guias em `docs/` para facilitar a navegação

---

## 5. Quando usar cada abordagem

| Cenário | Recomendação |
|---|---|
| Aprender RAG do zero, entender o porquê de cada etapa | PostGraduate |
| Prototipar um sistema RAG para um produto ou empresa | rag-project |
| Rodar sem custo de API (LLM local) | PostGraduate |
| Expor RAG via API para consumo externo | rag-project |
| Trabalhar com documentos em português ou multilíngues | rag-project |
| Demonstração rápida num ambiente de notebook | PostGraduate |

---

## Resumo

> O **PostGraduate** é uma demonstração didática que mostra o *porquê* e a evolução do RAG usando um LLM open-source. O **rag-project** é uma fundação de produção que mostra o *como* construir RAG modular, configurável e com API exposta.

---

## Referências

- [PostGraduateProgramAIAgentsBusinessApplications](https://github.com/ntitsolutins01/PostGraduateProgramAIAgentsBusinessApplications) — implementação em notebook com LangChain + Mistral
- [rag-project](https://github.com/ntitsolutins01/rag-project) — este repositório