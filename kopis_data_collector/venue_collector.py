import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_venue_list(cpage=1, rows=5, shprfnmfct=None, signgucode=None, signgucodesub=None):
    """
    공연시설 목록 조회(prfplcService) API에서 DataFrame을 반환하는 함수.
    CSV 저장은 하지 않고, DataFrame만 return.
    """
    url = "http://www.kopis.or.kr/openApi/restful/prfplc"
    params = {
        "service": SERVICE_KEY,
        "cpage": cpage,
        "rows": rows
    }

    if shprfnmfct:
        params["shprfnmfct"] = shprfnmfct
    if signgucode:
        params["signgucode"] = signgucode
    if signgucodesub:
        params["signgucodesub"] = signgucodesub

    response = requests.get(url, params=params)

    # 디버깅: 응답 상태 코드와 일부 내용 확인 (필요하다면 주석 해제)
    # print("응답 상태 코드:", response.status_code)
    # print("응답 내용:", response.text)

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("dbs", {}).get("db", [])

    # items가 단일 dict인 경우 리스트로 감싸기
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "mt10id": item.get("mt10id"),
            "fcltynm": item.get("fcltynm"),
            "mt13cnt": item.get("mt13cnt"),
            "fcltychartr": item.get("fcltychartr"),
            "sidonm": item.get("sidonm"),
            "gugunnm": item.get("gugunnm"),
            "opende": item.get("opende")
        }
        records.append(record)

    df = pd.DataFrame(records)

    # 컬럼명 매핑
    rename_dict = {
        "mt10id": "시설ID",
        "fcltynm": "시설명",
        "mt13cnt": "공연장수",
        "fcltychartr": "시설특성코드",
        "sidonm": "시도명",
        "gugunnm": "구군명",
        "opende": "개관연도"
    }
    df = df.rename(columns=rename_dict)

    # CSV 저장 로직 제거 → DataFrame 반환
    return df
