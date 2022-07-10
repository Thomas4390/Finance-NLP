#!/usr/bin/python3

import yfinance as yf
from yahoofinancials import YahooFinancials
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader.data as web
import plotly.graph_objects as go


def PriceChartPlotly(ticker, start_year):
    start = dt.datetime(start_year, 1, 1)
    end = dt.datetime.now()

    stocks = web.DataReader([ticker], "yahoo", start, end)

    c_candlestick = go.Figure(
        data=[
            go.Candlestick(
                x=stocks.index,
                open=stocks[("Open", ticker)],
                high=stocks[("High", ticker)],
                low=stocks[("Low", ticker)],
                close=stocks[("Close", ticker)],
            )
        ]
    )

    c_candlestick.update_xaxes(
        title_text="Date",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )
    yahoo_financials = YahooFinancials(ticker)
    CurrentPrice = yahoo_financials.get_current_price()

    c_candlestick.update_layout(
        title={
            "text": ticker
            + " SHARE PRICE ("
            + str(start_year)
            + "-"
            + str(dt.datetime.now().year)
            + ") "
            + "| | Actual Price (USD) : "
            + str(CurrentPrice),
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        }
    )

    c_candlestick.update_yaxes(title_text=ticker + " Close Price", tickprefix="$")

    return c_candlestick
