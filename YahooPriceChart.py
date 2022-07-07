#!/usr/bin/python3

import yfinance as yf
import matplotlib.pyplot as plt

def PriceChart(IndexEnterprise):
    ticker = yf.Ticker(IndexEnterprise)
    aapl_df = ticker.history(period="5y")
    aapl_df['Close'].plot(title="APPLE's stock price")
    plt.show()

PriceChart("AAPL")