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
    return f"https://alio.go.kr/item/itemReportTerm.do?apbaId={apbaId}&reportFormRootNo=2020&disclosureNo="


def get_html(url):
    driver.get(url)
    time.sleep(1)
    return BeautifulSoup(driver.page_source, "html.parser")


def get_table(soup):
    tables = soup.find_all("table")
    print(len(tables))
    return tables[5]  # 6번째 테이블이 임직원 정보 테이블임


def transform_table(table):
    return pd.read_html(str(table))[0]


def get_a_dataframe(apbaId):
    url = create_url(apbaId)
    soup = get_html(url)
    print("=" * 100)
    print(soup)
    table = get_table(soup)
    print(table)
    return transform_table(table)


def save_a_dataframe(dataframe, apbaNa):
    dataframe.to_csv(
        f"data/raw/임직원수/{apbaNa}.csv", index=False, encoding="utf-8-sig"
    )


def main():
    jsons = read_json()
    for d in jsons:
        apbaId = d["apbaId"]
        apbaNa = d["apbaNa"]
        print(apbaNa)
        dataframe = get_a_dataframe(apbaId)
        save_a_dataframe(dataframe, apbaNa)
        # time.sleep(1)  # for preventing server block
    driver.quit()


if __name__ == "__main__":
    main()
