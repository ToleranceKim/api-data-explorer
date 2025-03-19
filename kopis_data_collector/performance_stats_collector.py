import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_performance_stats(start_date, end_date, shcate, shprfnm, cpage=1, rows=10, filename=None):
    if filename is None:
        filename = f"data/prfsts_prf_by_{shcate}_{shprfnm}_{start_date}_{end_date}.csv"
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
    items = data_dict.get("prfsts", {}).get("prfst", [])
    if isinstance(items, dict):
        items = [items]
    records = []
    for item in items:
        record = {
            "mt20id": item.get("mt20id"),
            "prfnm": item.get("prfnm"),
            "prfpdfrom": item.get("prfpdfrom"),
            "prfpdto": item.get("prfpdto"),
            "prfdtcnt": item.get("prfdtcnt")
            # 실제 응답에 매출액(amount), 관객수(nmrs) 등의 필드가 있다면 여기에 추가
        }
        records.append(record)
    df = pd.DataFrame(records)
    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "prfdtcnt": "상연횟수"
    }
    df = df.rename(columns=rename_dict)
    df.to_csv(filename, index=False, encoding="utf-8")
