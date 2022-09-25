import requests, os
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

iex_token = os.environ.get('IEX_TOKEN')
iex_sandbox_token = os.environ.get('IEX_SANDBOX_TOKEN')
marketstack_token = os.environ.get('MARKETSTACK_TOKEN')

# Request
def request_url(url):
    return requests.get(url).json()

# Extracting ticker symbols
def us_equities():
    url = 'https://dumbstockapi.com/stock?format=tickers-only&countries=US'
    response = request_url(url)
    return sorted(response)

def company_quote(symbol):
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={iex_sandbox_token}' 
    response = request_url(url)
    return response

def get_latest_price(symbol):
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/price?token={iex_sandbox_token}'
    response = request_url(url)
    return Decimal(response)

def get_one_year_price(symbol):
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/1y?token={iex_sandbox_token}'
    response = request_url(url)
    return Decimal(response[-1]['close'])

def get_ytd_price(symbol):
    # for 2022
    url = f'http://api.marketstack.com/v1/eod/2022-01-03?access_key={marketstack_token}&symbols={symbol}'
    data = request_url(url)["data"]
    return Decimal(dict(data[-1])['close'])

def indices_performance():
    indices = ['SPY', 'QQQ', 'DIA']
    spy_performances, nasdaq_performances, djia_performances = [[] for _ in range(3)]
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