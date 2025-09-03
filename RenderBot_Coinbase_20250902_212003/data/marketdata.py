import time
import requests
import pandas as pd

# Coinbase Exchange (formerly Pro) public candles endpoint
# Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles
# Example: https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=300
CB_BASE = "https://api.exchange.coinbase.com"

GRAN_MAP = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
}

def fetch_ohlcv(symbol:str="BTC-USD", timeframe:str="5m", limit:int=300) -> pd.DataFrame | None:
    gran = GRAN_MAP.get(timeframe, 300)
    url = f"{CB_BASE}/products/{symbol}/candles?granularity={gran}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Coinbase returns newest-first arrays: [ time, low, high, open, close, volume ]
        df = pd.DataFrame(data, columns=["time","low","high","open","close","volume"])
        df = df.sort_values("time")  # make ascending
        if len(df) > limit:
            df = df.iloc[-limit:]
        df["timestamp"] = pd.to_datetime(df["time"], unit="s", utc=True)
        numeric_cols = ["open","high","low","close","volume"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        return df[["timestamp","open","high","low","close","volume"]].reset_index(drop=True)
    except Exception:
        return None

def latest_close(symbol:str="BTC-USD", timeframe:str="5m") -> float | None:
    df = fetch_ohlcv(symbol, timeframe, limit=2)
    if df is None or df.empty: return None
    return float(df.iloc[-1]["close"])
