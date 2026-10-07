"""Funções auxiliares: configuração, logging e variáveis de ambiente."""
import logging
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]


def load_config(path: str | Path | None = None) -> dict:
    """Carrega o config.yaml e as variáveis do .env."""
    load_dotenv(ROOT_DIR / ".env")
    path = Path(path) if path else ROOT_DIR / "config.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_logging(config: dict) -> logging.Logger:
    """Configura logging em arquivo (logs/app.log) e console."""
    log_cfg = config.get("logging", {})
    log_file = ROOT_DIR / log_cfg.get("file", "logs/app.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_cfg.get("level", "INFO")),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    return logging.getLogger("rag")
