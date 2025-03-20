import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_performance_list(start_date, end_date, cpage=1, rows=10):
    """
    공연목록(pblprfrService) API에서 DataFrame을 반환만 하는 함수.
    """
    url = "http://www.kopis.or.kr/openApi/restful/pblprfr"
    params = {
        "service": SERVICE_KEY,
        "stdate": start_date,
        "eddate": end_date,
        "cpage": cpage,
        "rows": rows
    }
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.text)

    # XML 파싱
    items = data_dict.get("dbs", {}).get("db", [])
    if isinstance(items, dict):
        items = [items]

    # 레코드 구성
    records = []
    for item in items:
        record = {
            "mt20id": item.get("mt20id"),
            "prfnm": item.get("prfnm"),
            "prfpdfrom": item.get("prfpdfrom"),
            "prfpdto": item.get("prfpdto"),
            "genrenm": item.get("genrenm"),
            "area": item.get("area")
        }
        records.append(record)

    # DataFrame 생성
    df = pd.DataFrame(records)

    # 컬럼명 매핑
    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "genrenm": "공연장르",
        "area": "공연지역"
    }
    df = df.rename(columns=rename_dict)

    # DataFrame 반환
    return df
