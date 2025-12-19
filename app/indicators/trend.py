import pandas_ta as ta

def weekly_trend(df):
    df["ema20"] = ta.ema(df["close"], 20)
    df["ema50"] = ta.ema(df["close"], 50)

    df["trend"] = df.apply(
        lambda x: "BULL" if x["ema20"] > x["ema50"] else "BEAR",
        axis=1
    )
    return df
