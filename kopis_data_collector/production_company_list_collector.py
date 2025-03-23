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

    - cpage: 현재페이지 (기본=1)
    - rows: 페이지당 목록 수 (기본=10, 최대=100)
    - entrpsnm: 기획/제작사명 (예: 국악단 등)
    - shcate: 장르코드 (AAAA=연극, BBBC=무용 등)
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: API 서비스 키 (.env 파일에서 로드)
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
    # 응답 루트가 <dbs>, 목록은 <db> 태그
    items = data_dict.get("dbs", {}).get("db", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "mt30id": item.get("mt30id"),      # 기획/제작사 ID
            "entrpsnm": item.get("entrpsnm"),  # 기획/제작사명
            "genrenm": item.get("genrenm"),    # 장르
            "telno": item.get("telno"),        # 전화번호
            "prfnm": item.get("prfnm"),        # 최신작품
            "relateurl": item.get("relateurl"),# 홈페이지
            "sidonm": item.get("sidonm")       # 시도명
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
