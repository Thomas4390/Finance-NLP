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

#Trouver le nom
df2 = df.set_index("Symbol")
Security_name = df2.loc[ticker].iat[0]



# On affiche ce qu'on à sélectionné dans la side bar
ticker_col, Sec_col = st.columns(2)

with ticker_col : st.write("You selected: ", ticker)

with Sec_col :
    st.write("Security name : ", Security_name )


#Company Information

url_finance = 'https://ca.finance.yahoo.com/quote/{}/financials?p={}'



response = requests.Session().get(url_finance.format(ticker, ticker),headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"})

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())

table = soup.find_all("span")


def has_numbers(x):
    return any(char.isdigit() for char in x)

Headers = []
for i in table:
    title=i.text
    Headers.append(title)

index_start = Headers.index("ttm")
index_end = Headers.index("Net Income")

data = Headers[ index_start : index_end+6 ]

#remove text
data2 = [s for s in data[5:] if has_numbers(s)]
rows= [s for s in data if has_numbers(s) == False]

rows.remove("Operating Expenses")
rows.remove("ttm")


#Find the date
date = data[0:5]
df = pd.DataFrame(columns=date)

start = 0
end = 5
for x in range(int((len(data2))/5)):
    to_append = data2[start:end]
    df.loc[x] = to_append
    start = start + 5
    end = end + 5

df_new = df.set_axis(rows)

#On le met sur l'app
st.dataframe(df_new)
