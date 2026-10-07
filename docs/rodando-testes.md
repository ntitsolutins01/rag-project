# Rodando os testes

Os testes do projeto são **unitários** — não dependem de API key, de modelos de embeddings nem de banco vetorial. Rodam rápido e de forma totalmente offline.

---

## Como rodar

Com o ambiente virtual ativado:

```bash
pytest tests/
```

Para saída detalhada (nome de cada teste):

```bash
pytest tests/ -v
```

---

## O que é testado

| Teste | O que verifica |
|---|---|
| `test_split_text_respeita_tamanho` | Chunks gerados respeitam o `chunk_size` configurado |
| `test_overlap_invalido` | Um `chunk_overlap` maior ou igual ao `chunk_size` levanta `ValueError` |
| `test_chunk_documents_gera_ids_unicos` | Cada chunk recebe um ID único (sem colisões) |
| `test_load_directory` | Leitura de arquivos `.txt` da pasta de dados retorna o conteúdo correto |
| `test_prompt_contem_pergunta_e_fonte` | O prompt montado contém a pergunta do usuário e a fonte do documento |

---

## Saída esperada

```
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1
collected 5 items

tests/test_app.py::test_split_text_respeita_tamanho PASSED           [ 20%]
tests/test_app.py::test_overlap_invalido PASSED                       [ 40%]
tests/test_app.py::test_chunk_documents_gera_ids_unicos PASSED        [ 60%]
tests/test_app.py::test_load_directory PASSED                         [ 80%]
tests/test_app.py::test_prompt_contem_pergunta_e_fonte PASSED         [100%]

============================== 5 passed in 0.41s ==============================
```

---

## O que esses testes NÃO cobrem

Os testes unitários validam a lógica interna dos módulos de forma isolada. Eles não testam:

- Chamadas à API Anthropic (`llm_client.py`)
- Geração e busca de embeddings (`embedder.py`)
- Persistência no ChromaDB (`vector_store.py`)
- Endpoints HTTP (`routes.py`)

Para validar o fluxo completo, consulte o guia [Executando localmente](executando-localmente.md) e o guia [Testando a API pelo Swagger](testando-api-swagger.md).