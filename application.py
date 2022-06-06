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

news_table_td_text_list = []

for index, row in enumerate(news_table_tr):
    news_table_td = row.find_all('td')
    print(news_table_td[0].text)
    news_table_td_text = [td.text for td in news_table_td]
    st.write(news_table_td_text)
    news_table_td_text_list.append(news_table_td_text)

news_table_td_text_list_cleaned = []

for index in range(len(news_table_td_text_list)):

    date = news_table_td_text_list[index][0]

# Correspond à une date complète du type : mmm-JJ-AA HH:MM(AM/PM)

    if (len(date) > 15):

        news_table_td_text_list_cleaned.append(date[0:17])

    else:

        news_table_td_text_list_cleaned.append(date[0:7])

print(news_table_td_text_list_cleaned)