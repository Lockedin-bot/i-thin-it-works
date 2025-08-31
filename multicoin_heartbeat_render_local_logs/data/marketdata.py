import requests, pandas as pd
def fetch_ohlcv(symbol:str="BTC-USD", granularity:int=300):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles?granularity={granularity}"
    try:
        r = requests.get(url, timeout=10); r.raise_for_status()
        arr = r.json()
        df = pd.DataFrame(arr, columns=["time","low","high","open","close","volume"]).sort_values("time")
        df["timestamp"] = pd.to_datetime(df["time"], unit="s", utc=True)
        return df[["timestamp","open","high","low","close","volume"]]
    except Exception:
        return None
