from YahooPrice import PriceChartPlotly
import streamlit as st
import pandas as pd

st.title("Stock Price Chart")

df = pd.read_csv("sp500.csv")

tickers = df["Symbol"].unique()
ticker = st.sidebar.selectbox("Choose a ticker", tickers)

start_year = st.sidebar.slider("Start year", 2000, 2020, 2000)

price_chart = PriceChartPlotly(ticker, start_year)

st.write(price_chart)
