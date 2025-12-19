def risk_levels(zone, atr):
    stop_loss = zone["low"] - atr
    target = zone["high"] + (zone["high"] - zone["low"]) * 2
    return stop_loss, target
