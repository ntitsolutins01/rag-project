# Executando o projeto localmente

---

## A ordem certa é: `ingest` → `ask` (ou `serve`)

Você não pode fazer perguntas antes de indexar os documentos. É como tentar consultar um fichário que ainda está vazio.

---

## Passo 1 — Indexar os documentos (`ingest`)

```bash
python main.py ingest
```

O projeto vai ler os arquivos da pasta `data/`, dividir em chunks, converter cada chunk em um vetor numérico usando um **modelo de embeddings que roda localmente na sua máquina** (sem chamar API nenhuma), e salvar tudo no ChromaDB em disco.

```
Antes de rodar:
  .venv/            ← Python isolado com todas as libs
  .env              ← sua chave da API (só usada no passo 2)
  data/exemplo.txt  ← o documento que vai ser indexado

O que será criado:
  chroma_db/        ← banco vetorial com os chunks + vetores
```

> **Atenção na primeira execução:** o modelo de embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) será **baixado da internet** (~120MB). Isso acontece uma única vez — depois fica em cache local.

O que você verá no terminal:

```
INFO  Ingeridos 1 documentos / X chunks
```

---

## Passo 2 — Fazer uma pergunta (`ask`)

```bash
python main.py ask "sua pergunta aqui"
```

Agora sim a chave da Anthropic é usada. O projeto vai:

1. Converter sua pergunta em vetor (modelo local, sem custo)
2. Buscar os chunks mais parecidos no ChromaDB
3. Montar um prompt com esses chunks como contexto
4. Enviar para o Claude via API Anthropic
5. Imprimir a resposta + as fontes utilizadas

**Você paga apenas essa chamada de API** — embeddings e busca são 100% locais.

O que você verá no terminal:

```
[resposta do Claude baseada nos seus documentos]

Fontes: exemplo.txt
```

---

## Alternativa — Subir a API REST (`serve`)

```bash
python main.py serve
```

Em vez de perguntas via terminal, sobe um servidor web em `http://localhost:8000`. Acesse `http://localhost:8000/docs` para usar a interface interativa (Swagger) e testar os endpoints `/ingest` e `/ask` pelo navegador.

---

## Resumo do fluxo completo

```
data/exemplo.txt
      │
      ▼
python main.py ingest      ← lê, chunka, vetoriza e salva no ChromaDB
      │
      ▼
chroma_db/                 ← banco vetorial persistido em disco
      │
      ▼
python main.py ask "..."   ← busca semântica + chamada ao Claude
      │
      ▼
Resposta + Fontes
```

---

## Dúvidas?

- Quer entender **por que o projeto funciona assim**? Leia o [guia de funcionamento do RAG](como-funciona.md).
- Quer ajustar chunk size, top_k ou modelo? Edite o [config.yaml](../config.yaml).