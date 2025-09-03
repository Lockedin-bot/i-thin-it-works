import pandas as pd

def momentum_signals(df: pd.DataFrame, fast:int=12, slow:int=26):
    df = df.copy()
    df["fast"] = df["close"].rolling(fast).mean()
    df["slow"] = df["close"].rolling(slow).mean()
    df["signal"] = 0
    # cross up
    df.loc[(df["fast"] > df["slow"]) & (df["fast"].shift(1) <= df["slow"].shift(1)), "signal"] = 1
    # cross down
    df.loc[(df["fast"] < df["slow"]) & (df["fast"].shift(1) >= df["slow"].shift(1)), "signal"] = -1
    return df
