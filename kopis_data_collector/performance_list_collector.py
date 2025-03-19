import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_performance_list(start_date, end_date, cpage=1, rows=10, filename=None):
    if filename is None:
        filename = f"data/pblprfr_list_{start_date}_{end_date}.csv"
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
            "genrenm": item.get("genrenm"),
            "area": item.get("area")
        }
        records.append(record)
    df = pd.DataFrame(records)
    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "genrenm": "공연장르",
        "area": "공연지역"
    }
    df = df.rename(columns=rename_dict)
    df.to_csv(filename, index=False, encoding="utf-8")
