import csv, requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from .randomKey import test_token, marketstack_token

# Extracting symbols from downloaded CSV
def us_equities():
    market_data = 'C:/Users/nicho/Desktop/Python/python_work/Portfolio/stockstracker/mainpage/API/allTickerSymbols.csv'
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
    file_path = 'C:/Users/nicho/Desktop/Python/python_work/Portfolio/stockstracker/mainpage/API/ticker_symbols.csv'
    symbols_df.to_csv(file_path, encoding='utf-8', index=False)

    # Open symbols.csv
    with open(file_path, newline='') as f:
        reader = csv.reader(f, delimiter=' ')
        # Storing all symbols into a list
        ticker_symbols = [', '.join(row) for row in reader]
    return ticker_symbols

def company_quote(symbol):
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={test_token}' 
    response = requests.get(url).json()
    return response

def get_latest_price(symbol):
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/price?token={test_token}'
    return Decimal(requests.get(url).json())

def get_one_year_price(symbol):
    # one_yr_date = (datetime.now() - relativedelta(years=1)).strftime('%Y-%m-%d')
    # url = f'http://api.marketstack.com/v1/eod/{one_yr_date}?access_key={token}&symbols={symbol}'
    # requests.get(url).json()['data']['close']
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/1y?token={test_token}'
    return Decimal(requests.get(url).json()[-1]['close'])

def get_ytd_price(symbol):
    # for 2022
    url = f'http://api.marketstack.com/v1/eod/2022-01-03?access_key={marketstack_token}&symbols={symbol}'
    data = requests.get(url).json()["data"]
    return Decimal(dict(data[-1])['close'])

def indices_performance():
    # url = f'http://sandbox.iexapis.com/stable/stock/{one_yrs_ago}?access_key={token}&symbols={spy},{nasdaq}'
    # one_year = requests.get(url).json()['data']
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


if __name__ == '__main__':
    with open('C:/Users/nicho/Desktop/Python/python_work/Portfolio/stockstracker/mainpage/API/output.txt', 'w') as f:
        print(us_equities(), file=f)

# print(get_latest_price('SPY', 'Tpk_b92512064b5c4f27b2dd86b8bcd66b81'))
# print(stock_performance('VOO', 'QQQM', '6f0a6ec2e07afe990d5675957ee51947'))
# print(indices_performance(test_token))
# print(get_ytd_price('SPY'))