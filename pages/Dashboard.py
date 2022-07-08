#!/usr/bin/python3
import pandas as pd
import streamlit as st
from pietroski import GetPietroskiScore

# Le nom de la page
st.title("Dashboard")

df = pd.read_csv("sp500.csv")

# On s'assure que pour chaque ticker le nom est unique
tickers = df["Symbol"].unique()

# On créer une side bar qui nous permettra de choisir le ticker dans l'application
ticker = st.sidebar.selectbox("Choose a ticker", tickers)

pietroski_score = GetPietroskiScore(ticker)

st.write("**Pietroski F score:** ", pietroski_score)

security_name = df.loc[df["Symbol"] == ticker]["Security"].values[0]
sector_name = df.loc[df["Symbol"] == ticker]["GICS Sector"].values[0]
industry_name = df.loc[df["Symbol"] == ticker]["GICS Sub-Industry"].values[0]

# On affiche ce qu'on à sélectionné dans la side bar
st.write(
    "**Ticker**: ",
    ticker,
    " || **Security:** ",
    security_name,
    " || **Sector:** ",
    sector_name,
    " || **Industry:** ",
    industry_name,
)

df_stat_tab = pd.read_csv("StatTab.csv")
st.write(df_stat_tab)
