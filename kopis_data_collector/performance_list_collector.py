# 1. 공연목록 조회 (pblprfrService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_pblprfr_list(
    stdate,
    eddate,
    cpage=1,
    rows=10,
    shcate=None,
    shprfnm=None,
    shprfnmfct=None,
    prfplccd=None,
    signgucode=None,
    signgucodesub=None,
    kidstate=None,
    prfstate=None,
    openrun=None,
    afterdate=None,
    service_key=SERVICE_KEY
):
    """
    1. 공연목록 조회(pblprfrService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - cpage, rows: 페이징
    - shcate: 장르코드 (AAAA=연극, BBBC=무용 등)
    - shprfnm: 공연명
    - shprfnmfct: 공연시설명
    - prfplccd: 공연장코드
    - signgucode: 시도코드
    - signgucodesub: 구군코드
    - kidstate: 아동공연여부 (Y/N)
    - prfstate: 공연상태코드 (01=예정, 02=공연중, 03=완료)
    - openrun: 오픈런여부 (Y/N)
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/pblprfr"

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
    if shprfnmfct:
        params["shprfnmfct"] = shprfnmfct
    if prfplccd:
        params["prfplccd"] = prfplccd
    if signgucode:
        params["signgucode"] = signgucode
    if signgucodesub:
        params["signgucodesub"] = signgucodesub
    if kidstate:
        params["kidstate"] = kidstate
    if prfstate:
        params["prfstate"] = prfstate
    if openrun:
        params["openrun"] = openrun
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
            "mt20id": item.get("mt20id"),
            "prfnm": item.get("prfnm"),
            "genrenm": item.get("genrenm"),
            "prfstate": item.get("prfstate"),
            "prfpdfrom": item.get("prfpdfrom"),
            "prfpdto": item.get("prfpdto"),
            "poster": item.get("poster"),
            "fcltynm": item.get("fcltynm"),
            "openrun": item.get("openrun"),
            "area": item.get("area")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "genrenm": "공연장르",
        "prfstate": "공연상태",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "poster": "포스터경로",
        "fcltynm": "공연시설명",
        "openrun": "오픈런여부",
        "area": "공연지역"
    }
    df = df.rename(columns=rename_dict)

    return df
