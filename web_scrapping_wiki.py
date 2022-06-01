# Importations des librairies

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lien URL
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

page = requests.get(url)

# On change le parseur pour qu'il soit plus compatible avec le format Python
# On obtient l'information de la page

soup = BeautifulSoup(page.text, 'lxml')





