import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_performance_stats(start_date, end_date, shcate, shprfnm, cpage=1, rows=10):
    """
    공연별 통계(prfstsPrfBy) API에서 DataFrame을 반환만 하는 함수.
    CSV 저장은 하지 않고, 메인 스크립트에서 처리.
    """
    url = "http://www.kopis.or.kr/openApi/restful/prfstsPrfBy"
    params = {
        "service": SERVICE_KEY,
        "stdate": start_date,
        "eddate": end_date,
        "shcate": shcate,
        "shprfnm": shprfnm,
        "cpage": cpage,
        "rows": rows
    }
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.text)

    # XML 파싱
    items = data_dict.get("prfsts", {}).get("prfst", [])
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
            "prfdtcnt": item.get("prfdtcnt")
            # API에 따라 매출액(amount), 관객수(nmrs) 등이 있으면 여기에 추가
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
        "prfdtcnt": "상연횟수"
    }
    df = df.rename(columns=rename_dict)

    # CSV 저장 대신 DataFrame만 반환
    return df
