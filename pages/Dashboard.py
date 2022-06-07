#!/usr/local/bin/python3
import numpy as np
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
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


