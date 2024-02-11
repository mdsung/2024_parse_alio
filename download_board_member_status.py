import collections
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

collections.Callable = (
    collections.abc.Callable
)  # BeutifulSoup의 기능을 사용하기 위해서 필요한 코드


def make_status_dict(apbaNa: str, input_string: str) -> dict[str, str]:
    # Processing the input string to extract data
    lines = input_string.strip().split("\n")
    registration_date = ""
    cause_date = ""
    for line in lines:
        if line.startswith("등록일"):
            _, registration_date = line.split(" ", 1)
        elif line.startswith("사유발생일"):
            _, cause_date = line.split(" ", 1)
    return {
        "기관명": apbaNa,
        "등록일": registration_date,
        "사유발생일": cause_date,
    }


# Set up the Selenium driver
driver = webdriver.Edge()
main_window = driver.current_window_handle
# Connect to the URL
url = "https://alio.go.kr/item/itemOrganList.do?reportFormRootNo=20305"
driver.get(url)
time.sleep(1)

t_content = driver.find_element(By.CLASS_NAME, "t-content")
buttons = t_content.find_elements(By.TAG_NAME, "button")
print(buttons[0].text)
buttons[0].click()

total_status = driver.find_element(By.CLASS_NAME, "list-inner2")
status_elements = total_status.find_elements(By.TAG_NAME, "li")
d = make_status_dict(buttons[0].text.split("\n")[0], status_elements[0].text)
print(d)
status_elements[0].click()
time.sleep(1)
from bs4 import BeautifulSoup


def click_nolink_for_scrollDown(driver, scrollDown_num=100):
    body = driver.find_element(By.TAG_NAME, "body")
    body.click()
    time.sleep(0.1)
    for _ in range(scrollDown_num):
        time.sleep(0.1)
        body.send_keys(Keys.PAGE_DOWN)


# 새로 열린 창으로 전환
for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break


# 새 창 닫기

click_nolink_for_scrollDown(driver, 10)
# Get the HTML code of the current page
html = driver.page_source

# Use BeautifulSoup to parse the HTML code
soup = BeautifulSoup(html, "html.parser")
# Save the HTML code as an HTML file
with open(f"data/raw/임원현황/{d['기관명']}_{d['등록일']}.html", "w") as file:
    file.write(soup.prettify())

driver.close()

# for button in buttons:
#     button.click()


#     time.sleep(1)

# Close the driver
driver.quit()
