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


def GetTitle(driver):
    Title = driver.find_element(
        By.XPATH,
        '//*[@class="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Tt(u) Bgc($lv1BgColor)"]',
    )
    Title2 = driver.find_elements(
        By.XPATH,
        '//*[@class="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)"]',
    )
    Title3 = driver.find_elements(
        By.XPATH,
        '//*[@class="Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)"]',
    )
    MainTitle = (
        Title.text
        + ","
        + Title2[0].text
        + ","
        + Title3[0].text
        + ","
        + Title2[1].text
        + ","
        + Title3[1].text
    )
    with open("StatTab.csv", "w") as f:
        f.write("Breakdown" + "," + MainTitle + "\n")


def GetTab(ticker):
    temp = 0
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--nogpu")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,1280")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    website = (
        "https://ca.finance.yahoo.com/quote/"
        + ticker
        + "/financials?p="
        + ticker
    )
    try:
        driver.get(website)
        driver.set_page_load_timeout(30)
    except:
        print("Can't open the website")
        exit(84)

    try:
        cookies = driver.find_elements(
            By.XPATH, "//*[@class='btn secondary accept-all consent_reject_all_2']"
        )
        sleep(0.5)
        cookies[0].click()
    except:
        pass

    try:
        GetTitle(driver)
        MainTab = driver.find_elements(By.XPATH, "//*[@class='D(tbrg)']")
        ParseTab = MainTab[0].text
        ParseTab = ParseTab.replace(",", ".")
        ParseTab = ParseTab.split("\n")
        for element in ParseTab:
            with open("StatTab.csv", "a") as f:
                # MANAGE FIRST COLUMN
                if temp == 0:
                    element = element + ","
                    f.write(element)
                    # print(element, end="")
                    temp += 1
                # MANAGE NUMBER
                elif temp == 1 and element[0].isalpha() == False:
                    element = element.replace(" ", ",")
                    f.write(element + "\n")
                    # print(element)
                    temp = 0
                # MANAGE EMPTY LINE
                else:
                    element = element + ","
                    f.write(",,,,\n" + element)
                    # print("\n", element, end="")
                    temp = 1
    except:
        print("Error")
        exit(84)


def GetCSV(ticker : str = "MMM"):
    return GetTab(ticker)


if __name__ == "__main__":
    GetCSV()
    
