#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests

def GetPietroskiScore(Company : str = "MMM"):
    try:
        url = "https://www.gurufocus.com/term/fscore/NAS:" + Company + "/Piotroski-F-Score/"
        response = requests.Session().get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"})
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.find_all("font")
        for element in text:
            if ("(As of Today)" in element.text):
                PietroskiFScore = element.text.replace("(As of Today)", "")
                PietroskiFScore = PietroskiFScore.replace(" ", "")
                PietroskiFScore = PietroskiFScore.replace(":", "")
                #print(Company, ":", PietroskiFScore)
                return (PietroskiFScore)
    except:
        return("None")

def main():
    GetPietroskiScore("MMM")

if __name__ == "__main__":
    main()