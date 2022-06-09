#!/usr/local/bin/python3

import re
import json
import csv
from io import StringIO
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

#Le nom de la page
st.markdown("Dashboard")

df = pd.read_csv("sp500.csv")

# On s'assure que pour chaque ticker le nom est unique
tickers = df["Symbol"].unique()

# On créer une side bar qui nous permettra de choisir le ticker dans l'application
ticker = st.sidebar.selectbox("Choose a ticker", tickers)

security_name = df.loc[df["Symbol"] == ticker]["Security"].values[0]
sector_name = df.loc[df["Symbol"] == ticker]["GICS Sector"].values[0]
industry_name = df.loc[df["Symbol"] == ticker]["GICS Sub-Industry"].values[0]

# On affiche ce qu'on à sélectionné dans la side bar
st.write("**Ticker**: ", ticker,
         " || **Security:** ", security_name,
         " || **Sector:** ", sector_name,
         " || **Industry:** ", industry_name)


def scrapping_income_statement_from_yahoo_finance(ticker):
    url_finance = 'https://ca.finance.yahoo.com/quote/{}/financials?p={}'
    response = requests.Session().get(url_finance.format(ticker, ticker), headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"})
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find_all("span")
    text = [x.text for x in text]

    return text


text = scrapping_income_statement_from_yahoo_finance("MMM")

index_start = text.index("ttm")
index_end = text.index("Net Income")

data = text[index_start: index_end+6]

regex_numbers = '-?\d+,?\d+,?\d+'
data_numbers = [re.findall(regex_numbers, string) for string in data]

data_numbers_cleaned = [match for match in data_numbers[5:] if len(match) > 0]
data_numbers_flat = sum(data_numbers_cleaned, [])

regex_text = '\D+'
data_texts = [re.findall(regex_text, string) for string in data]

data_text_flat = []

for text in data_texts:
    for word in text:
        if len(word) > 1:
            data_text_flat.append(word)

regex_dates = '\d+-\d+-\d+'
data_dates = [re.findall(regex_dates, string) for string in data]
data_dates_cleaned = [date for date in data_dates if len(date) > 0]
data_dates_flat = sum(data_dates_cleaned, [])

print(data_text_flat)


