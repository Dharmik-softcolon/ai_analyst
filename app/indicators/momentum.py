import pandas_ta as ta

def add_momentum(df):
    df["rsi"] = ta.rsi(df["close"], 14)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], 14)
    return df
