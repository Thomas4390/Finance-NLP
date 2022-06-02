# Importations des librairies

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lien URL
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

page = requests.get(url)

# On change le parseur pour qu'il soit plus compatible avec le format Python
# On obtient l'information de la page
# Ne pas oublier de pip install le parseur avant de lancer le script

soup = BeautifulSoup(page.text, "lxml")

# On obtient l'information depuis le tag HTML <table>

table1 = soup.find("table", {"class": "wikitable sortable"}, id="constituents")

# Le but est maintenant d'obtenir tous les titres de chaque colonne grâce au tag <th>

headers = []
for i in table1.find_all("th"):
    title = i.text
    headers.append(title)

# On nettoie les headers pour enlever les espaces

headers_clean = [header.replace("\n", "") for header in headers]

print(headers_clean)

# on creer une Dataframe

df = pd.DataFrame(columns=headers_clean)


# Create a for loop to fill mydata
for j in table1.find_all("tr")[1:]:

    row_data = j.find_all("td")
    row = [i.text for i in row_data]
    length = len(df)
    df.loc[length] = row



for col in df.columns:
    df[col] = df[col].str.replace("\n", "")

df["Founded"] = df["Founded"].str[:4]



