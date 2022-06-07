#!/usr/local/bin/python3
# Importations des librairies

import requests
from bs4 import BeautifulSoup
import pandas as pd


def GetTable():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        headers = []

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        table = soup.find(
            "table", {"class": "wikitable sortable"}, id="constituents")

        for i in table.find_all("th"):
            title = i.text
            headers.append(title)

        headers_clean = [header.replace("\n", "") for header in headers]
        return (headers_clean, table)
    except:
        print("Error getting table")
        exit(84)


def SaveTab(headers_clean, tab):
    try:
        df = pd.DataFrame(columns=headers_clean)

        for j in tab.find_all("tr")[1:]:
            row_data = j.find_all("td")
            row = [i.text for i in row_data]
            length = len(df)
            df.loc[length] = row

        for col in df.columns:
            df[col] = df[col].str.replace("\n", "")

        df["Founded"] = df["Founded"].str[:4]
        #print(df.head(10))
        df.to_csv("sp500.csv", index=False)
    except:
        print("Error saving table")
        exit(84)


def main():
    headers_clean, tab = GetTable()
    SaveTab(headers_clean, tab)
    return (0)


if __name__ == "__main__":
    main()