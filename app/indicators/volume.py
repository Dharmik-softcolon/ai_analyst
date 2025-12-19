def volume_expansion(df):
    df["vol_ma"] = df["volume"].rolling(20).mean()
    df["vol_exp"] = df["volume"] > df["vol_ma"] * 1.8
    return df
