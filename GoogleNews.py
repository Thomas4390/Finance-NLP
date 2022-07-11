#!/usr/bin/python3
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
import re
import pandas as pd


def Connection():
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # for headless mode
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--nogpu")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,1280")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    )
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def GoogleNews(driver, Enterprise):
    url = "https://www.google.com/search?q=" + Enterprise.upper()
    driver.get(url)
    driver.set_page_load_timeout(30)
    try:
        driver.find_element(By.XPATH, "//*[@class='QS5gu sy4vM']").click()
    except:
        pass
    try:
        NewsButton = driver.find_elements(By.XPATH, "//*[@class='hdtb-mitem']")
        NewsButton[0].click()
        Title = driver.find_elements(
            By.XPATH, "//*[@class='mCBkyc y355M ynAwRc MBeuO nDgy9d']"
        )
        SousText = driver.find_elements(By.XPATH, "//*[@class='GI74Re nDgy9d']")
        Time = driver.find_elements(By.XPATH, "//*[@class='OSrXXb ZE0LJd']")


        def convert_str_to_date(date_str):
            substring = date_str.split()[:2]
            current_date = datetime.datetime.now()
            # I could have used the dictionnary method to map the differents if cases. 
            # But I wanted to keep the code as simple as possible.
            try:
                if (substring[1] == "year" or substring[1] == "years"):
                    date = current_date - datetime.timedelta(years=int(substring[0]))

                elif (substring[1] == "month" or substring[1] == "months"):
                    date = current_date - datetime.timedelta(months=int(substring[0]))

                elif (substring[1] == "week" or substring[1] == "weeks"):
                    date = current_date - datetime.timedelta(weeks=int(substring[0]))

                elif (substring[1] == "day" or substring[1] == "days"):
                    date = current_date - datetime.timedelta(days=int(substring[0]))

                elif (substring[1] == "hour" or substring[1] == "hours"):
                    date = current_date - datetime.timedelta(hours=int(substring[0]))
                else:
                    date = current_date - datetime.timedelta(minutes=int(substring[0]))

            except:
                date = current_date - datetime.timedelta(days=30)

            return date
            
        def sort_list_datetime(list_datetime):
            list_datetime.sort(reverse=True)
            return list_datetime    

        MAX_RANGE = 10

        Times = [(i, elem.text) for i, elem in enumerate(Time)][:MAX_RANGE]
        DateTimes = sort_list_datetime([convert_str_to_date(elem[1]) for elem in Times][:MAX_RANGE])
        Titles = [elem.text.replace("...", "") for elem in Title][:MAX_RANGE]
        SousTexts = [elem.text.replace("...", "")
                     for elem in SousText][:MAX_RANGE]

        df = pd.DataFrame(
            data={'Time': DateTimes, 'Titles': Titles, 'Subtitle': SousTexts})

        return df

    except:
        print("No News")
        


def get_google_news(ticker:str = "GOOGL"):
    driver = Connection()
    GoogleNews(driver, ticker)


if __name__ == "__main__":
    get_google_news()
