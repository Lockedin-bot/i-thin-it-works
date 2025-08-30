import pandas as pd
def momentum_signals(df: pd.DataFrame, fast:int=20, slow:int=60):
    df = df.copy()
    df['fast'] = df['close'].rolling(fast).mean()
    df['slow'] = df['close'].rolling(slow).mean()
    df['signal'] = 0
    df.loc[(df['fast'] > df['slow']) & (df['fast'].shift(1) <= df['slow'].shift(1)), 'signal'] = 1
    df.loc[(df['fast'] < df['slow']) & (df['fast'].shift(1) >= df['slow'].shift(1)), 'signal'] = -1
    return df
