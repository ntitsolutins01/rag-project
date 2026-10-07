# Testando a API pelo Swagger

O Swagger é a interface visual da API — você pode testar todos os endpoints diretamente pelo navegador, sem precisar de ferramentas externas como Postman ou curl.

---

## Pré-requisito

Com o servidor rodando:

```bash
python main.py serve
```

Acesse **http://localhost:8000/docs** no navegador.

---

## POST /ingest — Indexar documentos

**1.** Clique em `POST /ingest` para expandir o endpoint

**2.** Clique no botão **"Try it out"** (canto direito)

**3.** No campo **Request body**, escolha uma das opções:

- **Indexar toda a pasta `data/`** — deixe o body assim:
```json
{}
```

- **Indexar um arquivo específico** — informe o caminho:
```json
{
  "source": "data/exemplo.txt"
}
```

- **Indexar uma URL** — informe o endereço:
```json
{
  "source": "https://exemplo.com/pagina"
}
```

**4.** Clique em **"Execute"**

**5.** A resposta aparece abaixo com o total de documentos e chunks processados:
```json
{
  "documentos": 1,
  "chunks": 1
}
```

---

## POST /ask — Fazer uma pergunta

**1.** Clique em `POST /ask` para expandir o endpoint

**2.** Clique em **"Try it out"**

**3.** No campo **Request body**, informe sua pergunta:
```json
{
  "question": "O que é RAG e quais são suas vantagens?"
}
```

**4.** Clique em **"Execute"**

**5.** A resposta inclui o texto gerado e as fontes utilizadas:
```json
{
  "answer": "RAG (Retrieval-Augmented Generation) é uma técnica...",
  "sources": [
    "exemplo.txt"
  ]
}
```

---

## GET /health — Verificar status

**1.** Clique em `GET /health`

**2.** Clique em **"Try it out"** → **"Execute"**

**3.** Retorna o status da aplicação e quantos chunks estão indexados:
```json
{
  "status": "ok",
  "chunks_indexados": 1
}
```

> Se `chunks_indexados` for `0`, rode o `/ingest` antes de fazer perguntas.

---

## Fluxo recomendado no Swagger

```
1. GET  /health   → confirma que o servidor está no ar
2. POST /ingest   → indexa os documentos da pasta data/
3. GET  /health   → verifica se os chunks foram criados
4. POST /ask      → faz sua pergunta e recebe a resposta com fontes
```