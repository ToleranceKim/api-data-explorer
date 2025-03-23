# 5. 기획/제작사 목록 조회 (mnfctService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_mnfct_list(
    cpage=1,
    rows=10,
    entrpsnm=None,
    shcate=None,
    afterdate=None,
    service_key=SERVICE_KEY
):
    """
    5. 기획/제작사 목록 조회(mnfctService)

    - cpage, rows: 페이징
    - entrpsnm: 기획/제작사명
    - shcate: 장르코드
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/mnfct"
    params = {
        "service": service_key,
        "cpage": cpage,
        "rows": rows
    }
    if entrpsnm:
        params["entrpsnm"] = entrpsnm
    if shcate:
        params["shcate"] = shcate
    if afterdate:
        params["afterdate"] = afterdate

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("dbs", {}).get("db", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "mt30id": item.get("mt30id"),
            "entrpsnm": item.get("entrpsnm"),
            "genrenm": item.get("genrenm"),
            "telno": item.get("telno"),
            "prfnm": item.get("prfnm"),
            "relateurl": item.get("relateurl"),
            "sidonm": item.get("sidonm")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "mt30id": "기획사ID",
        "entrpsnm": "기획사명",
        "genrenm": "장르",
        "telno": "전화번호",
        "prfnm": "최신작품",
        "relateurl": "홈페이지",
        "sidonm": "시도명"
    }
    df = df.rename(columns=rename_dict)

    return df
