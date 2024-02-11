import collections
import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

collections.Callable = (
    collections.abc.Callable
)  # BeutifulSoup의 기능을 사용하기 위해서 필요한 코드
driver = webdriver.Edge()


def read_json():
    with open("data/raw/apba.json") as f:
        data = json.load(f)
    return data


def create_url(apbaId):
    return f"https://alio.go.kr/item/itemReportTerm.do?apbaId={apbaId}&reportFormRootNo=10101"


def click_nolink_for_scrollDown(driver, scrollDown_num=100):
    body = driver.find_element(By.TAG_NAME, "body")
    body.click()
    time.sleep(0.1)
    for _ in range(scrollDown_num):
        time.sleep(0.1)
        body.send_keys(Keys.PAGE_DOWN)


def get_html(url):
    driver.get(url)
    time.sleep(0.5)
    click_nolink_for_scrollDown(
        driver, 10
    )  # 아랫까지 모두 로딩하기 위해서 scroll down을 최대한 한 상태에서 parsing을 한다.
    return BeautifulSoup(driver.page_source, "html.parser")


def main():
    jsons = read_json()
    target_raw_folder = "data/raw/일반현황"
    for d in tqdm(jsons):
        apbaId = d["apbaId"]
        apbaNa = d["apbaNa"]
        print(apbaNa)
        url = create_url(apbaId)
        soup = get_html(url)
        time.sleep(1)
        with open(f"{target_raw_folder}/{apbaNa}.html", "w") as file:
            file.write(soup.prettify())
    driver.quit()


if __name__ == "__main__":
    main()
