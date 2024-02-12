import collections
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

collections.Callable = (
    collections.abc.Callable
)  # BeutifulSoup의 기능을 사용하기 위해서 필요한 코드
# Read the HTML file


def parse_from_table(company_name, table):
    data = {
        "기업": "",
        "직위": "",
        "성명": "",
        "직책": "",
        "성별": "",
        "임기_시작일": "",
        "임기_종료일": "",
        "주요경력": "",
        "선임절차": "",
        "선임절차규정": "",
    }

    # 직위와 성명
    data["기업"] = company_name
    data["직위"] = table.find_all("tr")[0].find_all("td")[1].get_text().strip()  # 직위
    data["성명"] = table.find_all("tr")[0].find_all("td")[3].get_text().strip()  # 성명

    # 직책과 성별
    data["직책"] = table.find_all("tr")[1].find_all("td")[1].get_text().strip()
    data["성별"] = table.find_all("tr")[1].find_all("td")[3].get_text().strip()

    # 임기 시작일과 종료일
    data["임기_시작일"] = table.find_all("tr")[2].find_all("td")[2].get_text().strip()
    data["임기_종료일"] = table.find_all("tr")[2].find_all("td")[4].get_text().strip()

    # 주요경력
    data["주요경력"] = (
        table.find_all("tr")[3].find_all("td")[1].get_text(separator="\n")
    )

    # 선임절차
    data["선임절차"] = table.find_all("tr")[4].find_all("td")[1].get_text().strip()

    # 선임절차규정
    data["선임절차규정"] = table.find_all("tr")[5].find_all("td")[1].get_text().strip()
    return data


def read_downloaded_file(html_file):
    with open(html_file, "r") as file:
        return file.read()


def main():
    outcomes = []
    for html_file in Path("data/raw/임원현황").glob("*.html"):
        html_content = read_downloaded_file(html_file)
        soup = BeautifulSoup(html_content, "html.parser")

        tables = soup.find_all("table")
        company_name = html_file.stem.split("_")[0]
        for table in tables:
            try:
                d = parse_from_table(company_name, table)
            except Exception as e:
                continue
            else:
                outcomes.append(d)

    pd.DataFrame(outcomes).to_excel(
        "data/processed/임원현황/임원현황.xlsx", index=False
    )


if __name__ == "__main__":
    main()
