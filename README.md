# Analyse.AI - Stock Trading Signal Generator

## 📋 Project Overview

**Analyse.AI** is an automated stock trading signal generator that analyzes market data to identify potential swing trading opportunities. The system uses technical analysis, supply/demand zone detection, and multiple indicators to generate BUY signals for stocks.

### What It Does
- Fetches 5-minute candlestick data from MongoDB
- Analyzes price action to identify demand zones (support areas)
- Uses multiple technical indicators (RSI, EMA, Volume, ATR)
- Generates trading signals with entry, stop-loss, and target prices
- Scores each setup based on multiple criteria

---

## 🏗️ Architecture & Components

The project is organized into modular components:

```
app/
├── main.py                 # Entry point - orchestrates the analysis
├── config/
│   └── settings.py         # Configuration (MongoDB, thresholds)
├── database/
│   └── mongodb.py          # MongoDB connection
├── data/
│   ├── fetcher.py          # Fetches data from MongoDB
│   └── resampler.py        # Converts 5m data to daily/weekly
├── indicators/
│   ├── trend.py            # Weekly trend analysis (EMA)
│   ├── momentum.py         # RSI and ATR indicators
│   └── volume.py           # Volume expansion detection
├── zones/
│   ├── supply_demand.py    # Detects demand zones
│   └── structure.py        # Market structure analysis
├── strategy/
│   ├── swing_strategy.py   # Signal generation logic
│   └── scoring.py          # Setup scoring system
├── risk/
│   └── risk_manager.py     # Calculates stop-loss & targets
├── models/
│   └── signal.py           # TradeSignal data model
└── utils/
    └── time.py             # Time utilities
```

---

## 🔄 How It Works - Step by Step

### 1. **Data Fetching** (`app/data/fetcher.py`)
```python
fetch_5m_data("ABB")  # Fetches 5-minute candlestick data from MongoDB
```
- Connects to MongoDB database
- Retrieves historical OHLCV (Open, High, Low, Close, Volume) data for a stock symbol
- Returns a pandas DataFrame with timestamp as index

### 2. **Data Resampling** (`app/data/resampler.py`)
```python
daily = resample_ohlc(df_5m, "1D")   # Convert to daily timeframe
weekly = resample_ohlc(df_5m, "1W")  # Convert to weekly timeframe
```
- Converts 5-minute data to daily and weekly timeframes
- Aggregates: Open (first), High (max), Low (min), Close (last), Volume (sum)

### 3. **Trend Analysis** (`app/indicators/trend.py`)
```python
weekly = weekly_trend(weekly)
```
- Calculates 20-period and 50-period Exponential Moving Averages (EMA)
- Determines trend: **BULL** if EMA20 > EMA50, otherwise **BEAR**
- Only BUY signals are generated in BULL trends

### 4. **Momentum Indicators** (`app/indicators/momentum.py`)
```python
daily = add_momentum(daily)
```
- **RSI (Relative Strength Index)**: Measures momentum (0-100)
  - RSI 35-45 = Sweet spot for swing trades (oversold but not too oversold)
- **ATR (Average True Range)**: Measures volatility for risk calculation

### 5. **Volume Analysis** (`app/indicators/volume.py`)
```python
daily = volume_expansion(daily)
```
- Calculates 20-period volume moving average
- Detects volume expansion: Volume > 1.8x average volume
- Confirms strong buying interest

### 6. **Demand Zone Detection** (`app/zones/supply_demand.py`)
```python
zones = detect_demand_zones(daily)
```
**How it works:**
- Scans through price history looking for patterns
- Identifies a "base" (2-3 candles of consolidation)
- Looks for an "impulse" move (4 candles) that rises >6% from base
- Creates a demand zone from the base's low to high
- These zones act as support levels where price might bounce

**Example:**
```
Base: 3 candles consolidating at ₹100-102
Impulse: Price jumps to ₹108 (6%+ move)
Demand Zone: ₹100-102 (where buyers stepped in)
```

### 7. **Signal Generation** (`app/strategy/swing_strategy.py`)
```python
signal = generate_signal(latest, zone, trend)
```
**Conditions for BUY signal:**
1. ✅ Weekly trend must be **BULL**
2. ✅ Current price must be **within the demand zone** (low ≤ price ≤ high)
3. ✅ RSI must be between **35-45** (good entry point)
4. ✅ Volume expansion detected (strong interest)

### 8. **Risk Management** (`app/risk/risk_manager.py`)
```python
stop_loss, target = risk_levels(zone, atr)
```
- **Stop Loss**: Zone low - ATR (below the demand zone)
- **Target**: Zone high + (2x zone height) (profit target)
- Ensures risk-reward ratio of at least 2:1

### 9. **Scoring System** (`app/strategy/scoring.py`)
Each setup gets a score (0-9) based on:
- **Weekly Trend (BULL)**: +2 points
- **Fresh Zone**: +2 points
- **Volume Expansion**: +2 points
- **RSI in Sweet Spot (35-45)**: +1 point
- **Risk-Reward ≥ 2:1**: +1 point
- **Clean Market Structure**: +1 point

**Confidence Levels:**
- **HIGH**: Score ≥ 7
- **MEDIUM**: Score 5-6
- **LOW**: Score < 5

---

## 📊 Complete Workflow Example

```
1. Fetch Data
   └─> Get 5m candles for "ABB" from MongoDB

2. Resample
   ├─> Daily: Aggregate to daily candles
   └─> Weekly: Aggregate to weekly candles

3. Calculate Indicators
   ├─> Weekly: EMA20, EMA50 → Trend (BULL/BEAR)
   ├─> Daily: RSI, ATR
   └─> Daily: Volume expansion flag

4. Detect Demand Zones
   └─> Find zones where price had strong upward impulse

5. Check Each Zone
   ├─> Is weekly trend BULL? ✅
   ├─> Is price in zone? ✅
   ├─> Is RSI 35-45? ✅
   └─> Is volume expanding? ✅

6. Generate Signal
   └─> If all conditions met → BUY SIGNAL
       ├─> Entry: Current price
       ├─> Stop Loss: Zone low - ATR
       └─> Target: Zone high + (2x zone height)

7. Score & Confidence
   └─> Calculate score → Determine confidence level
```

---

## 🎯 Strategy Logic Explained

### **Why This Strategy Works**

1. **Demand Zones**: Areas where buyers previously stepped in strongly. Price often respects these levels.

2. **Weekly Trend Filter**: Only trades in the direction of the larger trend (bullish). "The trend is your friend."

3. **RSI Sweet Spot**: RSI 35-45 means the stock is oversold but not extremely oversold - good entry for swing trades.

4. **Volume Confirmation**: High volume confirms real buying interest, not just noise.

5. **Risk Management**: Stop-loss below the zone and target above ensures good risk-reward.

### **Trading Style**
- **Type**: Swing Trading
- **Holding Period**: 1-6 weeks (based on score)
- **Timeframe**: Daily charts
- **Market**: Indian Stock Market (NSE)

---

## ⚙️ Configuration

Edit `app/config/settings.py` to customize:

```python
MIN_IMPULSE_PCT = 0.06      # Minimum 6% price move to create zone
MAX_BASE_CANDLES = 3        # Max candles in base formation
MAX_HOLD_DAYS = 30          # Maximum holding period
TIMEZONE = "Asia/Kolkata"   # Market timezone
```

---

## 🚀 How to Use

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Analysis
```python
python app/main.py
```

### Current Output
The system prints BUY signals when found:
```
BUY SIGNAL: {'type': 'DEMAND', 'low': 100.5, 'high': 102.0, 'date': ...}
```

---

## 📦 Dependencies

- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **pandas-ta**: Technical indicators (RSI, EMA, ATR)
- **pymongo**: MongoDB database connection
- **scipy**: Signal processing (for market structure)
- **scikit-learn**: Machine learning utilities

---

## 🔮 Future Enhancements

The project structure suggests potential additions:
- Supply zone detection (for short signals)
- Signal persistence to database
- Backtesting framework
- Real-time signal alerts
- Portfolio management
- Performance tracking

---

## 📝 Notes

- The system currently analyzes one symbol at a time ("ABB" in main.py)
- Signals are printed to console (not saved to database yet)
- MongoDB must be running and contain 5-minute candlestick data
- All analysis is based on historical data - not real-time

---

## 🎓 Key Concepts

**Demand Zone**: A price range where buyers previously showed strong interest, causing a significant upward move. These zones often act as support.

**Swing Trading**: Holding positions for days to weeks, capturing medium-term price movements.

**RSI**: Relative Strength Index - momentum oscillator (0-100). Below 30 = oversold, above 70 = overbought.

**EMA**: Exponential Moving Average - gives more weight to recent prices.

**ATR**: Average True Range - measures market volatility.
