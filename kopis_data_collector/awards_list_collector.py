# 17. 수상작 목록 조회 (prfawadService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfawad_list(
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
    afterdate=None,
    service_key=SERVICE_KEY
):
    """
    17. 수상작 목록 조회(prfawadService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - cpage, rows: 페이징
    - shcate: 장르코드
    - shprfnm: 공연명
    - shprfnmfct: 공연시설명
    - prfplccd: 공연장코드
    - signgucode: 시도코드
    - signgucodesub: 구군코드
    - kidstate: 아동공연여부 (Y/N)
    - prfstate: 공연상태코드 (01,02,03)
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfawad"

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
            "prfpdfrom": item.get("prfpdfrom"),
            "prfpdto": item.get("prfpdto"),
            "fcltynm": item.get("fcltynm"),
            "poster": item.get("poster"),
            "genrenm": item.get("genrenm"),
            "prfstate": item.get("prfstate"),
            "awards": item.get("awards")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "fcltynm": "공연시설명",
        "poster": "포스터경로",
        "genrenm": "공연장르",
        "prfstate": "공연상태",
        "awards": "수상실적"
    }
    df = df.rename(columns=rename_dict)

    return df
