def detect_demand_zones(df):
    zones = []

    for i in range(5, len(df) - 5):
        base = df.iloc[i-2:i+1]
        impulse = df.iloc[i+1:i+5]

        impulse_pct = (impulse["close"].iloc[-1] - base["close"].mean()) / base["close"].mean()

        if impulse_pct > 0.06:
            zones.append({
                "type": "DEMAND",
                "low": base["low"].min(),
                "high": base["high"].max(),
                "date": df.index[i]
            })
    return zones
