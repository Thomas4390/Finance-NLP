#!/usr/local/bin/python3
import numpy as np
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st


# On charge les données depuis le fichier sp500 csv qui nous servira à récupérer le nom dst.es tickers
df = pd.read_csv("sp500.csv")


# On s'assure que pour chaque ticker le nom est unique
tickers = df["Symbol"].unique()

# On créer une side bar qui nous permettra de choisir le ticker dans l'application
ticker = st.sidebar.selectbox("Choose a ticker", tickers)

# On affiche ce qu'on à sélectionné dans la side bar
st.write("You selected: ", ticker)

# url du site web qui nous permettra de récupérer les données en web scrapping
finviz_url = "https://finviz.com/quote.ashx?t="

# Session de requête (sans cela on obtient une erreur)
session_obj = requests.Session()

# url complète de la requête grâce au ticker
ticker_url = finviz_url + ticker

# Réponse du site. Si tout est ok renvoie 200. 
response = session_obj.get(ticker_url, headers={"User-Agent": "Mozilla/5.0"})

st.write(f"Status code: {response.status_code}")

# On accède au code HTML de la page
html = BeautifulSoup(response.text, "html.parser")

# On filtre la page HTML pour se retrouver seulement avec la table qui contient le nom des différents articles.
news_table = html.find(id='news-table')

# On filtre encore pour ne garder que les tags <tr>
news_table_tr = news_table.find_all('tr')


# Le but ici est de créer une liste qui contiendra les différentes informations de la table au format suivant :
# [0: "Date de l'article", 1: "Titre de l'article"]
news_table_td_text_list = []

for index, row in enumerate(news_table_tr):
    news_table_td = row.find_all('td')
    news_table_td_text = [td.text for td in news_table_td]
    news_table_td_text_list.append(news_table_td_text)


# Après avoir obtenue cette liste, on aimerait ne conserver que les dates : [0: "Date de l'article"]
news_table_td_text_list_cleaned = []

for index in range(len(news_table_td_text_list)):

    date = news_table_td_text_list[index][0]

# Correspond à une date complète du type : mmm-JJ-AA HH:MM(AM/PM)
# On se rend compte qu'il y a un peu de nettoyage à faire pour enlever les espaces à la fin de la date
# Si la date dépasse 15 caractères c'est qu'elle est du type : mmm-JJ-AA HH:MM(AM/PM)
# Sinon, elle est du type : HH:MM(AM/PM)
# Il existe à 100% de meilleures manières de nettoyer, mais à améliorer plus tard. 
    if (len(date) > 15):

        news_table_td_text_list_cleaned.append(date[0:17])

    else:

        news_table_td_text_list_cleaned.append(date[0:7])


# Nouveau nom de variable plus concis

dates = news_table_td_text_list_cleaned

# On convertit la liste de dates en dataframe (Series)
# Cela sera plus pratique pour faire des manipulations avec, comme par exemple changer les date ern format datetime ou encore ajouter
# deux series ensembles. 

dates_series = pd.Series(dates)

dates_series_split = dates_series.str.split(" ")


# Ici, on se rend compte qu'on ne pourra pas split la Series en deux car au sein de la Series on aura des listes de taille 1 et de taille 2. 
# Pour pallier à cela, on ajoute une colonne vide dans la Series lorsque la date est du type : HH:MM(AM/PM)
for i in range(len(dates_series_split)):
    if (len(dates_series_split[i]) == 1):
        dates_series_split[i] = [None] + dates_series_split[i]


# On peut maintenant séparer les deux listes en deux colonnes distinctes. 
# on en profite pour remplacer les valeurs None par les valeurs précédentes grâce à la fonction ffill()
date_series = dates_series_split.str[0].ffill()
time_series = dates_series_split.str[1]

# on combine les deux series
dates_series_combined = date_series + " " + time_series

# On convertit la Series au format dateTime (plus facile pour faire des manipulations)
dates_series_dt = pd.to_datetime(dates_series_combined)

dates_list = dates_series_dt.tolist()

news_table_cleaned = []

for i in range(len(news_table_td_text_list)):
    news_table_td_text_list[i][0] = dates_list[i]
    news_table_cleaned.append(news_table_td_text_list[i])

st.write(news_table_cleaned[0:10])