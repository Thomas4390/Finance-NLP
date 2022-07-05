#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def GetTab(EnterpriseLetter):
    temp = 0
    driver = webdriver.Chrome()
    website = (
        "https://ca.finance.yahoo.com/quote/"
        + EnterpriseLetter
        + "/financials?p="
        + EnterpriseLetter
    )

    try:
        driver.get(website)
        driver.set_page_load_timeout(30)
        cookies = driver.find_elements(
            By.XPATH, "//*[@class='btn secondary accept-all consent_reject_all_2']"
        )
        sleep(0.5)
        cookies[0].click()
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
                    f.write("\n" + element)
                    # print("\n", element, end="")
                    temp = 1
    except:
        print("Error")
        exit(84)


def main():
    GetTab("AAPL")


if __name__ == "__main__":
    main()
