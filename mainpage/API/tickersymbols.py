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


def company_quote(ticker):
    url = f'{sandbox_url}{ticker}/quote?token={iex_sandbox_token}' 
    response = request_url(url)
    return response

def get_ytd_price(tickers):
    # for 2022
    url = f'http://api.marketstack.com/v1/eod/2022-01-03?access_key={marketstack_token}&symbols={",".join(tickers)}'
    response = list(dict(request_url(url))['data'])
    return [Decimal(response[2]['close']), Decimal(response[1]['close']), Decimal(response[0]['close'])]

def get_latest_price(tickers):
        if len(tickers) > 1:
            tickers = ",".join(tickers)
        else:
            tickers = tickers[0]
        url = f"{sandbox_url}market/batch?token={iex_sandbox_token}&types=price&symbols={tickers}"
        response = list(dict(request_url(url)).values())
        response = [Decimal(ticker['price']) for ticker in response]
        return response

def indices_performance():
    indices = ['SPY', 'QQQ', 'DIA']
    performances = {
    indices[0]: {'ytdPerf': 0, 'oneYearPerf': 0},
    indices[1]: {'ytdPerf': 0, 'oneYearPerf': 0},
    indices[2]: {'ytdPerf': 0, 'oneYearPerf': 0},
    }

    url = f"{sandbox_url}market/batch?token={iex_sandbox_token}&types=price,chart&range=1y&symbols={','.join(indices)}"
    current_one_year_price = dict(request_url(url))
    ytd_price = get_ytd_price(indices)
    for index, indice in enumerate(indices):
        current_price = Decimal(current_one_year_price[indice]['price'])
        one_year_price = Decimal(current_one_year_price[indice]['chart'][0]['close'])
        performances[indice]['oneYearPerf'] = (current_price - one_year_price)/one_year_price * 100
        performances[indice]['ytdPerf'] = (current_price - ytd_price[index])/ytd_price[index] * 100

    return performances