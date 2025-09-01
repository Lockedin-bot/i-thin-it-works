import os, logging
from dotenv import load_dotenv
from .config import Settings

def load_settings() -> Settings:
    load_dotenv()
    return Settings(**{k: v for k, v in os.environ.items() if k in Settings.model_fields})

def parse_symbols(csvv: str):
    return [t.strip() for t in csvv.split(",") if t.strip()]

def setup_logger(level="INFO"):
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO),
                        format="%(asctime)s [%(levelname)s] %(message)s")
    return logging.getLogger("bot")
