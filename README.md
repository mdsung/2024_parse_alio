# Alio 기관정보 parsing
- Author: MinDong Sung
- Date:  2024-02-11
---
## Objective

## Process
1. Alio 기관정보 및 기관코드 확인
    - apgaid는 https://www.alio.go.kr/organ/organDisclosureList.do source를 보면 아랫쪽에 확인할 수 있다. 
    - json형태로 hard coding 되어 있다. 
    - 이를 `data/raw/abpa.json`으로 만들었음.
2. 임직원 수
    - 기관코드를 이용하여 임원현황을 확인한다. 
    - https://alio.go.kr/item/itemReportTerm.do?apbaId=C0226&reportFormRootNo=2020&disclosureNo=
    - ![임직원수](<임직원수.png>)

3. 일반현황
    - 예시 주소: https://alio.go.kr/item/itemReportTerm.do?apbaId=C0226&reportFormRootNo=10101
    - ![alt text](<일반현황.png>)

4. 임직원현황
    - 업데이트 필요
    - 매일 하루 한번씩 크롤링 하여 업데이트 필요