#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def Connection():
    chrome_options = Options()
    chrome_options.add_argument('--headless') #for headless mode
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--nogpu")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,1280")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    return (driver)

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
        Title = driver.find_elements(By.XPATH, "//*[@class='mCBkyc y355M ynAwRc MBeuO nDgy9d']")
        SousText = driver.find_elements(By.XPATH, "//*[@class='GI74Re nDgy9d']")
        Time = driver.find_elements(By.XPATH, "//*[@class='OSrXXb ZE0LJd']")
        with open("GoogleNews.txt", "w") as f:
            f.write("")
        for i, elem in enumerate(Title):
            with open("GoogleNews.txt", "a") as f:
                Titles = elem.text.replace("...", "")
                SousTexts = SousText[i].text.replace("...", "")
                Times = Time[i].text.replace("There is ", "")
                f.write(Titles + "\n" + SousTexts + "\n" + Times + "\n")
                f.write("\n")
    except:
        pass
    return(0)

def main():
    driver = Connection()
    GoogleNews(driver, "aapl")

if __name__ == "__main__":
    main()