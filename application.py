from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st


df = pd.read_csv("sp500.csv")

tickers = df["Symbol"].unique()

ticker = st.sidebar.selectbox("Choose a ticker", tickers)

st.write("You selected: ", ticker)

finviz_url = "https://finviz.com/quote.ashx?t="

session_obj = requests.Session()

ticker_url = finviz_url + ticker

response = session_obj.get(ticker_url, headers={"User-Agent": "Mozilla/5.0"})

st.write(f"Status code: {response.status_code}")

html = BeautifulSoup(response.text, "html.parser")

news_table = html.find(id='news-table')

news_table_tr = news_table.find_all('tr')

for index, row in enumerate(news_table_tr):
    if index == 0:
        continue
    news_table_td = row.find_all('td')
    news_table_td_text = [td.text for td in news_table_td]
    st.write(news_table_td_text[1])
