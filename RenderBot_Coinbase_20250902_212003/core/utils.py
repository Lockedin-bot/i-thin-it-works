import os, logging
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return {
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
        "SYMBOLS": os.environ.get("SYMBOLS", "BTC-USD,ETH-USD,SOL-USD"),
        "TA_TIMEFRAME": os.environ.get("TA_TIMEFRAME", "5m"),
        "FAST_MA": int(os.environ.get("FAST_MA", "12")),
        "SLOW_MA": int(os.environ.get("SLOW_MA", "26")),
        "LOOP_SEC": int(os.environ.get("LOOP_SEC", "30")),
    }

def setup_logger(level="INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    return logging.getLogger("bot")

def parse_symbols(csvv: str):
    return [t.strip() for t in csvv.split(",") if t.strip()]
