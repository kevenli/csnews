import yfinance as yf
import os
import pandas as pd


def fetch_data(symbol):
    data_dir = 'marketdata'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    ticker = yf.Ticker(symbol)
    df_history = ticker.history()
    df_history.to_csv(f'{data_dir}/{symbol}.csv')


def load_data(symbol):
    data_dir = 'marketdata'
    data_file = f'{data_dir}/{symbol}.csv'
    if not os.path.exists(data_file):
        fetch_data(symbol)
    return pd.read_csv(data_file)


def main():
    symbols = ['BABA', 'BILI']
    for symbol in symbols:
        fetch_data(symbol)


if __name__ == '__main__':
    main()
