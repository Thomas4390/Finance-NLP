# ToDo: Afficher un menu déroulant pour choisir une compagnie

import streamlit as st
import pandas as pd 

df = pd.read_csv("sp500.csv")

tickers = df["Symbol"].unique()

option = st.sidebar.selectbox("Choose a ticker",tickers)

st.write("You selected: ", option)
