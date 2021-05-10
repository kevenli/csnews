from fetchdata import load_data
import pandas as pd

def process_data(symbol):
    df_ohlcv = load_data(symbol)
    df_full = df_ohlcv
    df_full['Chg'] = df_ohlcv['Close'] / df_ohlcv.shift()['Close'] -1
    return df_full
