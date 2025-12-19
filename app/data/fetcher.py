import pandas as pd
from app.database.mongodb import db
from app.config.settings import COLLECTION_NAME

def fetch_5m_data(symbol: str) -> pd.DataFrame:
    cursor = db[COLLECTION_NAME].find(
        {"symbol": symbol},
        {"_id": 0}
    ).sort("timestamp", 1)

    df = pd.DataFrame(list(cursor))
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    return df
