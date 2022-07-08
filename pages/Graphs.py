from YahooPrice import PriceChartPlotly
import streamlit as st
import pandas as pd

st.title("Stock Price Chart")

df = pd.read_csv("sp500.csv")

tickers = df["Symbol"].unique()
ticker = st.sidebar.selectbox("Choose a ticker", tickers)

price_chart = PriceChartPlotly(ticker)

st.write(price_chart)
