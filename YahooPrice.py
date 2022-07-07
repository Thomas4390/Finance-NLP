#!/usr/bin/python3

import yfinance as yf
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt

def PriceChart(IndexEnterprise):
    yahoo_financials = YahooFinancials(IndexEnterprise)
    ticker = yf.Ticker(IndexEnterprise)
    CurrentPrice = yahoo_financials.get_current_price()
    aapl_df = ticker.history(period="5y")
    plt.ylabel('Price')
    aapl_df['Close'].plot(title=IndexEnterprise + "'s stock price\nActual Price (USD) : " + str(CurrentPrice))
    plt.show()

PriceChart("AAPL")