import collections
import json
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

collections.Callable = collections.abc.Callable
driver = webdriver.Edge()


def read_json():
    with open("data/raw/apba.json") as f:
        data = json.load(f)
    return data


def create_url(apbaId):
    return f"https://alio.go.kr/item/itemReportTerm.do?apbaId={apbaId}&reportFormRootNo=10101"


def get_html(url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, "html.parser")


def main():
    jsons = read_json()
    for d in jsons:
        apbaId = d["apbaId"]
        apbaNa = d["apbaNa"]
        url = create_url(apbaId)
        soup = get_html(url)
        with open("output.html", "w") as file:
            file.write(soup.prettify())
        # tables = soup.find_all("table")
        # for i, table in enumerate(tables):
        #     print(f"{i+1}" + "=" * 100)
        #     print(table)
        break
    driver.quit()


if __name__ == "__main__":
    main()
