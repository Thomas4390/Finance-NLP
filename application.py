#!/usr/local/bin/python3
import numpy as np
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import json
import datetime as dt


def get_news_table_finviz():
    """This function allows you to obtain the news table from the symbol (ticker) of an action selected directly in the Streamlit application.
    We are getting the data from Finviz.
        Parameters:
        -----------
        Returns:
        --------
        An html object containing the news table.
    """
    try:

        df = pd.read_csv("sp500.csv")  # Loading Data in a DataFrame

        # Making sure that all tickers are unique
        tickers = df["Symbol"].unique()
        ticker = st.sidebar.selectbox(
            "Choose a ticker", tickers
        )  # Letting the users to choose a ticker directly in the Streamlit application

        st.write("You selected: ", ticker)

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


def main():
    """This function is the main function of the application."""
    news_table = get_news_table_finviz()
    news_table_td_text_list = extracting_date_and_title(news_table)
    dates_list = dates_to_clean_datetime_dates(news_table_td_text_list)
    news_table_cleaned = append_dates_and_title(
        dates_list, news_table_td_text_list)
    df = pd.DataFrame(news_table_cleaned, columns=["Date", "Title"])
    st.write(df)


if __name__ == "__main__":
    main()
