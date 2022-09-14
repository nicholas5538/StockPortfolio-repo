import csv, requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from .randomKey import iex_token, iex_sandbox_token, marketstack_token

# Extracting symbols from downloaded CSV
def us_equities():
    # market_data = 'C:/Users/nicho/Desktop/Python/StocksTracker/StockPortfolio-repo/mainpage/API/allTickerSymbols.csv'
    market_data = 'mainpage/API/allTickerSymbols.csv'
    df = pd.read_csv(market_data)
    # Make a new dataframe containing ticker symbols only
    symbols_df = df[['Symbol']].copy()

    # Check if new dataframe contains null
    if symbols_df['Symbol'].isnull().sum() > 0:
        symbols_df.dropna(axis=1, how='any')
        print('Null data present')
    else:
        symbols_df.columns = symbols_df.iloc[0]
        symbols_df = symbols_df[1:]
    # file_path = 'C:/Users/nicho/Desktop/Python/StocksTracker/StockPortfolio-repo/mainpage/API/ticker_symbols.csv'
    file_path = 'mainpage/API/ticker_symbols.csv'
    symbols_df.to_csv(file_path, encoding='utf-8', index=False)

    # Open symbols.csv
    with open(file_path, newline='') as f:
        reader = csv.reader(f, delimiter=' ')
        # Storing all symbols into a list
        ticker_symbols = [', '.join(row) for row in reader]
    return ticker_symbols

def company_quote(symbol):
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={iex_sandbox_token}' 
    response = requests.get(url).json()
    return response

def get_latest_price(symbol):
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/price?token={iex_sandbox_token}'
    return Decimal(requests.get(url).json())

def get_one_year_price(symbol):
    # one_yr_date = (datetime.now() - relativedelta(years=1)).strftime('%Y-%m-%d')
    # url = f'http://api.marketstack.com/v1/eod/{one_yr_date}?access_key={token}&symbols={symbol}'
    # requests.get(url).json()['data']['close']
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/1y?token={iex_sandbox_token}'
    return Decimal(requests.get(url).json()[-1]['close'])

def get_ytd_price(symbol):
    # for 2022
    url = f'http://api.marketstack.com/v1/eod/2022-01-03?access_key={marketstack_token}&symbols={symbol}'
    data = requests.get(url).json()["data"]
    return Decimal(dict(data[-1])['close'])

def indices_performance():
    indices = ['SPY', 'QQQ', 'DIA']
    spy_performances, nasdaq_performances, djia_performances = [], [], []
    for indice in indices:
        latest_price = get_latest_price(indice)
        ytd_price = get_ytd_price(indice)
        one_year_price = get_one_year_price(indice)
        if indice == 'SPY':
            spy_performances.append((latest_price - ytd_price)/ytd_price * 100)
            spy_performances.append(((latest_price - one_year_price)/one_year_price * 100))
        elif indice == 'QQQ':
            nasdaq_performances.append((latest_price - ytd_price)/ytd_price * 100)
            nasdaq_performances.append(((latest_price - one_year_price)/one_year_price * 100))
        else:
            djia_performances.append((latest_price - ytd_price)/ytd_price * 100)
            djia_performances.append(((latest_price - one_year_price)/one_year_price * 100))

    return spy_performances, nasdaq_performances, djia_performances