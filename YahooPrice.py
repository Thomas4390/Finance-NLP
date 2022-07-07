#!/usr/bin/python3

import yfinance as yf
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader.data as web
import plotly.graph_objects as go

def PriceChart(IndexEnterprise):
    yahoo_financials = YahooFinancials(IndexEnterprise)
    ticker = yf.Ticker(IndexEnterprise)
    CurrentPrice = yahoo_financials.get_current_price()
    aapl_df = ticker.history(period="5y")
    plt.ylabel('Price')
    aapl_df['Close'].plot(title=IndexEnterprise + "'s stock price\nActual Price (USD) : " + str(CurrentPrice))
    plt.show()

def PriceChart2(IndexEnterprise, BeginYears):
    # Customized OHLC
    start = dt.datetime(BeginYears,1,1)
    end = dt.datetime.now()

    stocks = web.DataReader([IndexEnterprise], 'yahoo', start, end)

    c_candlestick = go.Figure(data = [go.Candlestick(x = stocks.index, 
                                                   open = stocks[('Open',    IndexEnterprise)], 
                                                   high = stocks[('High',    IndexEnterprise)], 
                                                   low = stocks[('Low',    IndexEnterprise)], 
                                                   close = stocks[('Close',    IndexEnterprise)])])

    c_candlestick.update_xaxes(
        title_text = 'Date',
        rangeslider_visible = True,
        rangeselector = dict(
            buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))

    c_candlestick.update_layout(
        title = {
            'text': IndexEnterprise + ' SHARE PRICE (' + str(BeginYears) + '-' + str(dt.datetime.now().year) + ')',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    c_candlestick.update_yaxes(title_text = IndexEnterprise + ' Close Price', tickprefix = '$')
    c_candlestick.show()

#The best is the PriceChart2() function.
#PriceChart("AAPL")
#PriceChart2("AAPL", 2019)