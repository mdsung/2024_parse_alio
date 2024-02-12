import collections
import time
from typing import Dict, Optional

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

collections.Callable = (
    collections.abc.Callable
)  # BeutifulSoup의 기능을 사용하기 위해서 필요한 코드

URL = "https://alio.go.kr/item/itemOrganList.do?reportFormRootNo=20305"


def make_content_metadata(apbaNa: str, input_string: Optional[str]) -> dict[str, str]:
    """
    Extracts metadata from an input string and returns it along with the given name.

    Parameters:
    - apbaNa: The name of the institution.
    - input_string: A multiline string containing metadata entries.

    Returns:
    A dictionary with keys for the institution name, registration date, and cause date.
    """
    # Default metadata dictionary
    metadata = {
        "기관명": apbaNa,
        "등록일": "",
        "사유발생일": "",
    }

    # Return default metadata if input_string is None
    if not input_string:
        return metadata

    # Process each line in the input string to extract dates
    for line in input_string.strip().split("\n"):
        key, _, value = line.partition(" ")
        if key in ["등록일", "사유발생일"]:
            metadata[key] = value

    return metadata


def click_nolink_for_scrollDown(driver, scrollDown_num=100):
    body = driver.find_element(By.TAG_NAME, "body")
    body.click()
    time.sleep(0.1)
    for _ in range(scrollDown_num):
        time.sleep(0.1)
        body.send_keys(Keys.PAGE_DOWN)


def switch_window(driver, main_window, target="new"):
    """
    Switches the webdriver context to a specified window.

    Parameters:
    - driver: The webdriver instance.
    - target: Specifies the target window to switch to.
              "main" to switch to the main window,
              "new" to switch to a new window that is not the main window.
              Can be extended to accept a specific window handle as well.

    If the target window is not found, does not switch the window context.
    """
    windows = driver.window_handles

    if target == "main":
        for handle in windows:
            if handle == main_window:
                driver.switch_to.window(handle)
                break

    elif target == "new":
        # Switch to the first window that is not the current window
        for handle in windows:
            if handle != main_window:
                driver.switch_to.window(handle)
                break
    else:
        # Extend functionality here to switch to a specific window by handle if needed
        pass


def save_to_html(soup, company_name, enroll_date):
    with open(
        f"data/raw/임원현황/{company_name}_{enroll_date}.html",
        "w",
    ) as file:
        file.write(soup.prettify())


def main():
    # Set up the Selenium driver
    driver = webdriver.Edge()
    options = webdriver.EdgeOptions()

    options.add_argument("headless")
    options.add_argument("test-type")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--guest")
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.use_chromium = True
    options.add_experimental_option("detach", True)

    main_window = driver.current_window_handle
    # Connect to the URL
    driver.get(URL)
    time.sleep(1)

    # 회사별로 돌아다니기
    t_content = driver.find_element(By.CLASS_NAME, "t-content")
    buttons = t_content.find_elements(By.TAG_NAME, "button")

    for i, button in tqdm(enumerate(buttons)):
        company_name = button.text.split("\n")[0]
        button.click()
        time.sleep(1)

        # 임원현황 확인
        try:
            total_status = driver.find_element(By.CLASS_NAME, "list-inner2")
            status_elements = total_status.find_elements(By.TAG_NAME, "li")
            content_metadata = make_content_metadata(
                company_name, status_elements[0].text
            )
            status_elements[0].click()
        except:
            print(f"{company_name} 임원현황이 없습니다.")
            content_metadata = make_content_metadata(company_name, None)
            continue
        time.sleep(1)

        # 새로 열린 창으로 전환
        switch_window(driver, main_window, target="new")

        # 스크롤 다운
        click_nolink_for_scrollDown(driver, 10)

        # Use BeautifulSoup to parse the HTML code
        soup = BeautifulSoup(driver.page_source, "html.parser")
        save_to_html(soup, content_metadata["기관명"], content_metadata["등록일"])

        # 기존창으로 이동
        driver.close()
        switch_window(driver, main_window, target="main")

    driver.quit()


if __name__ == "__main__":
    main()
