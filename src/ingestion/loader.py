"""Carrega dados de PDFs, CSVs, TXT/MD e websites."""
import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_csv(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        rows = csv.DictReader(f)
        return "\n".join(
            "; ".join(f"{k}: {v}" for k, v in row.items()) for row in rows
        )


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_url(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


LOADERS = {
    ".pdf": load_pdf,
    ".csv": load_csv,
    ".txt": load_text,
    ".md": load_text,
}


def load_directory(data_dir: str | Path) -> list[dict]:
    """Lê todos os arquivos suportados e retorna [{'source', 'text'}]."""
    docs = []
    for path in sorted(Path(data_dir).rglob("*")):
        loader = LOADERS.get(path.suffix.lower())
        if path.is_file() and loader:
            text = loader(path).strip()
            if text:
                docs.append({"source": path.name, "text": text})
    return docs


def load_source(source: str) -> dict:
    """Carrega um arquivo ou URL individual."""
    if source.startswith(("http://", "https://")):
        return {"source": source, "text": load_url(source)}
    path = Path(source)
    return {"source": path.name, "text": LOADERS[path.suffix.lower()](path)}
