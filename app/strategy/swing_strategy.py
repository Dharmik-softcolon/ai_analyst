def generate_signal(latest_row, zone, weekly_trend):
    if weekly_trend != "BULL":
        return None

    if zone["low"] <= latest_row["low"] <= zone["high"]:
        if 35 <= latest_row["rsi"] <= 45 and latest_row["vol_exp"]:
            return "BUY"

    return None
