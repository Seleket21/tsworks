import csv
import requests

def download_csv(ticker):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=1644314526&period2=1675850526&interval=1d&events=history&includeAdjustedClose=true"
    response = requests.get(url, headers = user_agent)
    with open(f"{ticker}.csv", 'w') as f:
        f.write(response.text)

with open('tickers.txt') as f:
    tickers = f.read().splitlines()

for ticker in tickers:
    download_csv(ticker)
