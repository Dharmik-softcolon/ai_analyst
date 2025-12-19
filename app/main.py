from app.data.fetcher import fetch_5m_data
from app.data.resampler import resample_ohlc
from app.indicators.trend import weekly_trend
from app.indicators.momentum import add_momentum
from app.indicators.volume import volume_expansion
from app.zones.supply_demand import detect_demand_zones
from app.strategy.swing_strategy import generate_signal

df_5m = fetch_5m_data("ABB")
daily = resample_ohlc(df_5m, "1D")
weekly = weekly_trend(resample_ohlc(df_5m, "1W"))

daily = add_momentum(daily)
daily = volume_expansion(daily)

zones = detect_demand_zones(daily)
latest = daily.iloc[-1]
trend = weekly.iloc[-1]["trend"]

for zone in zones:
    signal = generate_signal(latest, zone, trend)
    if signal:
        print("BUY SIGNAL:", zone)
# main.py
