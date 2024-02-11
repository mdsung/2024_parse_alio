import collections
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

collections.Callable = collections.abc.Callable


# HTML 파일 로드
# 주요 정보를 찾기 위한 함수 정의
def find_text(soup, title):
    elements = soup.find_all(["td", "th"], string=lambda text: text and title in text)
    for el in elements:
        # 다음 형제 노드나 자식 노드에서 텍스트 추출
        next_sibling = el.find_next_sibling("td")
        if next_sibling and next_sibling.text.strip():
            return next_sibling.text.strip().replace("<br>", "\n")
        elif el.parent.find_next_sibling():
            sibling_cells = el.parent.find_next_sibling().find_all("td")
            if sibling_cells:
                return "\n".join(
                    cell.text.strip() for cell in sibling_cells if cell.text.strip()
                ).replace("<br>", "\n")
    return ""


def main():
    outputs = []
    titles = [
        "기관설립일",
        "설립근거",
        "설립목적",
        "주무기관",
        "소재지",
        "주요 기능 및 역할",
    ]
    for f in Path("data/raw/일반현황").glob("*.html"):
        with open(f, "r") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # 찾고자 하는 항목 리스트

        # 각 항목에 대한 정보 추출
        extracted_info = {}
        extracted_info = {title: find_text(soup, title) for title in titles}
        extracted_info["기관명"] = f.stem
        outputs.append(extracted_info)
    print(outputs)
    pd.DataFrame(outputs)[
        [
            "기관명",
        ]
        + titles
    ].to_excel("data/processed/일반현황/일반현황.xlsx", index=False)


if __name__ == "__main__":
    main()
