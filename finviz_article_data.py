from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pandas as pd

finviz_url = "https://finviz.com/quote.ashx?t="

session_obj = requests.Session()

df = pd.read_csv("sp500.csv")

tickers = df["Symbol"].tolist()

tickers_url = [finviz_url + ticker for ticker in tickers]
#responses = [session_obj.get(ticker_url, headers={'User-Agent': 'Mozilla/5.0'}) for ticker_url in tickers_url]

ticker_url = tickers_url[0]

response = session_obj.get(ticker_url, headers={"User-Agent": "Mozilla/5.0"})

responses = [session_obj.get(ticker_url, headers={"User-Agent": "Mozilla/5.0"}) for ticker_url in tickers_url]

print(response.status_code)
print(responses[0].status_code)
