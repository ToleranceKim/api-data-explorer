# 3. 공연시설 목록 조회 (prfplcService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfplc_list(
    cpage=1,
    rows=10,
    shprfnmfct=None,
    fcltychartr=None,
    signgucode=None,
    signgucodesub=None,
    afterdate=None,
    service_key=SERVICE_KEY
):
    """
    3. 공연시설 목록 조회(prfplcService)

    - cpage: 현재페이지
    - rows: 페이지당 목록 수 (최대 100)
    - shprfnmfct: 공연시설명
    - fcltychartr: 공연시설특성코드
    - signgucode: 시도코드
    - signgucodesub: 구군코드
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfplc"
    params = {
        "service": service_key,
        "cpage": cpage,
        "rows": rows
    }
    if shprfnmfct:
        params["shprfnmfct"] = shprfnmfct
    if fcltychartr:
        params["fcltychartr"] = fcltychartr
    if signgucode:
        params["signgucode"] = signgucode
    if signgucodesub:
        params["signgucodesub"] = signgucodesub
    if afterdate:
        params["afterdate"] = afterdate

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    # XML -> dict 변환
    data_dict = xmltodict.parse(response.text)
    # 응답 루트가 <dbs> 이고, 목록은 <db> 태그로 반복
    items = data_dict.get("dbs", {}).get("db", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "mt10id": item.get("mt10id"),        # 공연시설 ID
            "fcltynm": item.get("fcltynm"),      # 공연시설명
            "mt13cnt": item.get("mt13cnt"),      # 공연장 수
            "fcltychartr": item.get("fcltychartr"),  # 시설특성코드
            "sidonm": item.get("sidonm"),        # 시도명
            "gugunnm": item.get("gugunnm"),      # 구군명
            "opende": item.get("opende")         # 개관연도
        }
        records.append(record)

    df = pd.DataFrame(records)
    # 원하는 컬럼명으로 변경
    rename_dict = {
        "mt10id": "공연시설ID",
        "fcltynm": "공연시설명",
        "mt13cnt": "공연장수",
        "fcltychartr": "시설특성코드",
        "sidonm": "시도명",
        "gugunnm": "구군명",
        "opende": "개관연도"
    }
    df = df.rename(columns=rename_dict)

    return df
