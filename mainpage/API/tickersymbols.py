import requests, os
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

iex_token = os.environ.get('IEX_TOKEN')
iex_sandbox_token = os.environ.get('IEX_SANDBOX_TOKEN')
marketstack_token = os.environ.get('MARKETSTACK_TOKEN')
sandbox_url = "https://sandbox.iexapis.com/stable/stock/"

# Request

def request_url(url):
    return requests.get(url).json()

# Extracting ticker symbols

def us_equities():
    url = 'https://dumbstockapi.com/stock?format=tickers-only&countries=US'
    response = request_url(url)
    return sorted(response)

class Ticker:

    def __init__(self, ticker):
        self.ticker = ticker

    def __str__(self):
        return f'Ticker symbol: {self.ticker}'

    def company_quote(self):
        url = f'{sandbox_url}{self.ticker}/quote?token={iex_sandbox_token}' 
        response = request_url(url)
        return response
    
    def get_latest_price(self):
        url = f'{sandbox_url}{self.ticker}/price?token={iex_sandbox_token}'
        response = request_url(url)
        return Decimal(response)

    def get_one_year_price(self):
        url = f'{sandbox_url}{self.ticker}/chart/1y?token={iex_sandbox_token}'
        response = request_url(url)
        return Decimal(response[-1]['close'])

    def get_ytd_price(self):
        # for 2022
        url = f'http://api.marketstack.com/v1/eod/2022-01-03?access_key={marketstack_token}&symbols={self.ticker}'
        data = request_url(url)["data"]
        return Decimal(dict(data[-1])['close'])

def indices_performance():
    performances = {
    'SPY': {'ytd': 0, 'oneYear': 0},
    'QQQ': {'ytd': 0, 'oneYear': 0},
    'DIA': {'ytd': 0, 'oneYear': 0},
    }
    indices = [Ticker('SPY'), Ticker('QQQ'), Ticker('DIA')]

    def addValues(index):
        if index == 0:
            indice = 'SPY'
        elif index == 1:
            indice = 'QQQ'
        else:
            indice = 'DIA'

        performances[indice]['ytd'] = ytd_math
        performances[indice]['oneYear'] = one_year_math

        return performances

    for index, indice in enumerate(indices):
        latest_price = indice.get_latest_price()
        ytd_price = indice.get_ytd_price()
        one_year_price = indice.get_one_year_price()
        ytd_math = (latest_price - ytd_price)/ytd_price * 100
        one_year_math = (latest_price - one_year_price)/one_year_price * 100
        indices = addValues(index)

    return indices