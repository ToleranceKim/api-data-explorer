# 14. 공연별 통계 목록 조회 (prfstsPrfByService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_prfby(
    stdate,
    eddate,
    cpage=1,
    rows=10,
    shcate=None,
    shprfnm=None,
    service_key=SERVICE_KEY
):
    """
    14. 공연별 통계 목록 조회(prfstsPrfByService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - cpage, rows: 페이징
    - shcate: 장르코드
    - shprfnm: 공연명
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsPrfBy"
    params = {
        "service": service_key,
        "stdate": stdate,
        "eddate": eddate,
        "cpage": cpage,
        "rows": rows
    }
    if shcate:
        params["shcate"] = shcate
    if shprfnm:
        params["shprfnm"] = shprfnm

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("prfsts", {}).get("prfst", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "prfnm": item.get("prfnm"),
            "cate": item.get("cate"),
            "mt20id": item.get("mt20id"),
            "fcltynm": item.get("fcltynm"),
            "entrpsnm": item.get("entrpsnm"),
            "prfpdfrom": item.get("prfpdfrom"),
            "prfpdto": item.get("prfpdto"),
            "prfdtcnt": item.get("prfdtcnt")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "prfnm": "공연명",
        "cate": "장르",
        "mt20id": "공연ID",
        "fcltynm": "공연시설명",
        "entrpsnm": "기획/제작사",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "prfdtcnt": "상연횟수"
    }
    df = df.rename(columns=rename_dict)

    return df
