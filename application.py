#!/usr/local/bin/python3
import numpy as np
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import json
import datetime as dt
import sys
from GoogleNews import get_google_news
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import plotly.graph_objs as go
import matplotlib.pyplot as plt

df = pd.read_csv("sp500.csv")  # Loading Data in a DataFrame

# Making sure that all tickers are unique
tickers = df["Symbol"].unique()
ticker = st.sidebar.selectbox("Choose a ticker", tickers)  # Letting the users to choose a ticker directly in the Streamlit application
st.write("You selected: ", ticker)

def get_news_table_finviz(ticker: str = "MMM") -> BeautifulSoup:
    """This function allows you to obtain the news table from the symbol (ticker) of an action selected directly in the Streamlit application.
    We are getting the data from Finviz.
        Parameters:
        -----------
        Returns:
        --------
        An html object containing the news table.
    """
    try:



        # Finviz url without the ticker specified
        finviz_url = "https://finviz.com/quote.ashx?t="
        session_obj = requests.Session()  # Creating a session object
        ticker_url = finviz_url + ticker  # Finviz url with the ticker specified

        response = session_obj.get(
            ticker_url, headers={"User-Agent": "Mozilla/5.0"}
        )  # Response object from the session object. return 200 if ok. return 404 if not.

        # Parsing the html code
        html = BeautifulSoup(response.text, "html.parser")
        news_table = html.find(id="news-table")  # Finding the news table

        return news_table  # Returning the news table

    except:
        st.write("Error getting the news table")
        exit(84)


def extracting_date_and_title(news_table) -> list:
    """This function extracts the date and title of the news from the news table.
    Parameters
    ----------
    news_table : html object
        The news table from the Finviz website.
    Returns
    -------
    list
        A list of the date and title for each article.
    """

    try:

        news_table_tr = news_table.find_all(
            "tr"
        )  # Getting <tr> tags from the news table

        # The goal here is to create a list that will contain the different information of the table in the following format:
        # [0: "Article date", 1: "Article title"]
        news_table_td_text_list = []

        for index, row in enumerate(news_table_tr):
            news_table_td = row.find_all("td")
            news_table_td_text = [td.text for td in news_table_td]
            news_table_td_text_list.append(news_table_td_text)

        return news_table_td_text_list

    except:
        st.write("Error extracting date and title")
        exit(84)


def dates_to_clean_datetime_dates(news_table_td_text_list) -> list:
    """This function clean the date and convert them into a datetime format.
    Parameters
    ----------
    news_table_td_text_list :
        A list of the date and title for each article.
    Returns
    -------
    list(datetime.datetime)
        A list of the cleaned date in datetime format.
    """
    try:
        # After having obtained this list, we would like to keep only the dates: [0: "Date of the article"]
        news_table_td_text_list_date_cleaned = []

        for index in range(len(news_table_td_text_list)):

            date = news_table_td_text_list[index][0]

            # Corresponds to a complete date of the type: mmm-DD-YY HH:MM(AM/PM)
            # We realize that there is a little cleaning to do to remove the spaces at the end of the date
            # If the date exceeds 15 characters it is of type: mmm-DD-YY HH:MM(AM/PM)
            # Otherwise, it is of type: HH:MM(AM/PM)
            # There are 100% better ways to clean, but to be improved later.
            if len(date) > 15:
                news_table_td_text_list_date_cleaned.append(date[0:17])

            else:
                news_table_td_text_list_date_cleaned.append(date[0:7])

        # We convert the list of dates into a dataframe (Series)
        # This will be more convenient to do manipulations with, such as changing the dates to datetime format or adding
        # two series together.
        dates_series = pd.Series(news_table_td_text_list_date_cleaned)
        dates_series_split = dates_series.str.split(" ")

        # Here, we realize that we cannot split the Series in two because within the Series we will have lists of size 1 and size 2.
        # To overcome this, we add an empty column in the Series when the date is of type: HH:MM(AM/PM)
        for i in range(len(dates_series_split)):
            if len(dates_series_split[i]) == 1:
                dates_series_split[i] = [None] + dates_series_split[i]

        # We can now separate the two lists into two distinct columns.
        # We take the opportunity to replace the None values by the previous ones thanks to the ffill() function
        date_series = dates_series_split.str[0].ffill()
        time_series = dates_series_split.str[1]

        # We combine the two series into a dataframe
        dates_series_combined = date_series + " " + time_series

        # Convert the Series to dateTime format (easier to do manipulations)
        dates_series_dt = pd.to_datetime(dates_series_combined)

        # We can now convert the Series to a list
        dates_list = dates_series_dt.tolist()

        # dates_list = [dt.datetime.strftime(date, '%m-%d-%y %I:%M%p') for date in dates_list]

        return dates_list

    except:
        st.write("Error extracting date and title")
        exit(84)


def append_dates_and_title(dates_list, news_table_td_text_list) -> list:
    """This function append the date and title of the news to the list of dates.
    Parameters
    ----------
    dates_list : list(datetime.datetime)
        A list of the cleaned date in datetime format.
    news_table_td_text_list : list
        A list of the date and title for each article.
    Returns
    -------
    list(datetime.datetime, string)
        A list of the cleaned date and title for each article.
    """
    try:
        news_table_cleaned = []
        # Replacing old dates with new dates and appending the title to the list
        for i in range(len(news_table_td_text_list)):
            news_table_td_text_list[i][0] = dates_list[i]
            news_table_cleaned.append(news_table_td_text_list[i])

        return news_table_cleaned

    except:
        st.write("Error appending date and title")
        exit(84)


def get_finviz_news(ticker) -> pd.DataFrame:
    """This function is the main function of the application."""
    news_table = get_news_table_finviz(ticker)
    news_table_td_text_list = extracting_date_and_title(news_table)
    dates_list = dates_to_clean_datetime_dates(news_table_td_text_list)
    news_table_cleaned = append_dates_and_title(dates_list, news_table_td_text_list)
    df_news_data = pd.DataFrame(news_table_cleaned, columns=["Date", "Title"])
    return df_news_data

def from_df_to_text_list(df: pd.DataFrame, column_name: str = 'Title') -> list:
    """This function convert the dataframe into a list of strings.
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the news.
    column_name : str
        The name of the column to convert.
    Returns
    -------
    list
        A list of strings.
    """
    try:
        text_list = []
        for index, row in df.iterrows():
            text_list.append(row[column_name])
        return text_list

    except:
        st.write("Error converting dataframe into list")
        exit(84)

def from_text_list_to_sentiment_df(text_list: list) -> pd.DataFrame:
    """This function convert the list of strings into a list of sentiment scores.
    Parameters
    ----------
    text_list : list
        A list of strings.
    Returns
    -------
    DataFrame
        A Dataframe of sentiment scores.
    """
    try:
        finbert = BertForSequenceClassification.from_pretrained(
            'yiyanghkust/finbert-tone', num_labels=3)
        tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)
        results = nlp(text_list)
        df_results = pd.DataFrame(results)

        return df_results

    except:
        st.write("Error converting list of strings into list of sentiment scores")
        exit(84)
    

def concat_results(df1: pd.DataFrame, df2: pd.DataFrame):

    df_results = pd.concat([df1, df2], axis=1)
    return df_results

def count_sentiment_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """This function count the number of positive, negative and neutral sentiment over time.
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the news.
    Returns
    -------
    pd.DataFrame
        A Dataframe of the number of positive, negative and neutral sentiment over time.
    """

    negative_count_list = []
    positive_count_list = []
    neutral_count_list = []

    try:
        label_list = list(df['label'])

        for i in range(len(label_list)):
            neutral_count_list.insert(0, label_list[-i-1:].count("Neutral"))
            positive_count_list.insert(0, label_list[-i-1:].count("Positive"))
            negative_count_list.insert(0, label_list[-i-1:].count("Negative"))

        df["negative_count"] = negative_count_list
        df["positive_count"] = positive_count_list
        df["neutral_count"] = neutral_count_list
    except:
        pass

    return df

    

def plot_sentiment(df: pd.DataFrame):
    """This function plot the sentiment scores.
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the sentiment scores.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Line(x=df["Date"], y=df["negative_count"], name="Negative", marker_color="red"))
    fig.add_trace(
        go.Line(x=df["Date"], y=df["positive_count"], name="Positive", marker_color="green"))
    fig.add_trace(
        go.Line(x=df["Date"], y=df["neutral_count"], name="Neutral", marker_color="blue"))
        
    return fig.show()
    

if __name__ == "__main__":
    df_finviz_news = get_finviz_news(ticker)
    #df_google_news = get_google_news(ticker)

    text_list_finviz = from_df_to_text_list(df_finviz_news, column_name='Title')
    #text_list_google = from_df_to_text_list(df_google_news, column_name='Subtitle')

    df_results_finviz = from_text_list_to_sentiment_df(text_list_finviz)
    #df_results_google = from_text_list_to_sentiment_df(text_list_google)

    df_concat_finviz = concat_results(df_finviz_news, df_results_finviz)
    #df_concat_google = concat_results(df_google_news, df_results_google)

    df_finviz_final = count_sentiment_over_time(df_concat_finviz)
    #df_google_final = count_sentiment_over_time(df_concat_google)

    st.write(df_finviz_final)
    #st.write(df_google_final)

    st.write(plot_sentiment(df_finviz_final))
    #st.write(plot_sentiment(df_google_final))
    
