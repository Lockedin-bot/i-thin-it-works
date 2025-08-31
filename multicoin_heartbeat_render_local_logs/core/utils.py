import os, logging
from dotenv import load_dotenv
from .config import Settings

def load_settings() -> Settings:
    load_dotenv()
    s = Settings(**{k: v for k, v in os.environ.items() if k in Settings.model_fields})
    def num(name, cast, default):
        try: return cast(os.getenv(name, default))
        except: return default
    s.TOTAL_EQUITY = num("TOTAL_EQUITY", float, s.TOTAL_EQUITY)
    s.FAST_MA = num("FAST_MA", int, s.FAST_MA)
    s.SLOW_MA = num("SLOW_MA", int, s.SLOW_MA)
    s.RISK_PER_TRADE = num("RISK_PER_TRADE", float, s.RISK_PER_TRADE)
    s.MAX_DRAWDOWN = num("MAX_DRAWDOWN", float, s.MAX_DRAWDOWN)
    s.POSITION_LIMIT = num("POSITION_LIMIT", int, s.POSITION_LIMIT)
    return s

def parse_symbols(symbols_csv: str):
    return [tok.strip() for tok in symbols_csv.split(",") if tok.strip()]

def setup_logger(level: str = "INFO"):
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO),
                        format="%(asctime)s [%(levelname)s] %(message)s")
    return logging.getLogger("bot")
