from pydantic import BaseModel
class Settings(BaseModel):
    MODE: str = "paper"
    LOG_LEVEL: str = "INFO"
    TOTAL_EQUITY: float = 10000.0
    SYMBOLS: str = "BTC-USD,ETH-USD,SOL-USD"
    FAST_MA: int = 20
    SLOW_MA: int = 60
    TA_TIMEFRAME: str = "5m"
    RISK_PER_TRADE: float = 0.01
    MAX_DRAWDOWN: float = 0.20
    POSITION_LIMIT: int = 5
