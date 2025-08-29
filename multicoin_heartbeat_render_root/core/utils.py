import os, logging
from dotenv import load_dotenv
from .config import Settings

def load_settings() -> Settings:
    load_dotenv()
    s = Settings(**{k: v for k, v in os.environ.items() if k in Settings.model_fields})
    s.TOTAL_EQUITY = float(os.getenv("TOTAL_EQUITY", s.TOTAL_EQUITY))
    s.FAST_MA = int(os.getenv("FAST_MA", s.FAST_MA))
    s.SLOW_MA = int(os.getenv("SLOW_MA", s.SLOW_MA))
    s.RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", s.RISK_PER_TRADE))
    s.MAX_DRAWDOWN = float(os.getenv("MAX_DRAWDOWN", s.MAX_DRAWDOWN))
    s.POSITION_LIMIT = int(os.getenv("POSITION_LIMIT", s.POSITION_LIMIT))
    return s

def parse_symbols(symbols_csv: str):
    return [tok.strip() for tok in symbols_csv.split(",") if tok.strip()]

def setup_logger(level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger("bot")
