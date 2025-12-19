from scipy.signal import argrelextrema
import numpy as np

def market_structure(df):
    df["swing_high"] = df.iloc[
        argrelextrema(df["high"].values, np.greater, order=5)[0]
    ]["high"]

    df["swing_low"] = df.iloc[
        argrelextrema(df["low"].values, np.less, order=5)[0]
    ]["low"]

    return df
