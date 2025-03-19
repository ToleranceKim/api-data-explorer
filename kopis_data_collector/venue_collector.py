import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_venue_list(cpage=1, rows=5, shprfnmfct=None, signgucode=None, signgucodesub=None, filename=None):
    if filename is None:
        filename = f"data/prfplc_list.csv"
    url = "http://www.kopis.or.kr/openApi/restful/prfplc"
    params = {"service": SERVICE_KEY, "cpage": cpage, "rows": rows}
    if shprfnmfct:
        params["shprfnmfct"] = shprfnmfct
    if signgucode:
        params["signgucode"] = signgucode
    if signgucodesub:
        params["signgucodesub"] = signgucodesub
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("dbs", {}).get("db", [])
    if isinstance(items, dict):
        items = [items]
    records = []
    for item in items:
        record = {
            "mt10id": item.get("mt10id"),
            "fcltynm": item.get("fcltynm"),
            "mt13cnt": item.get("mt13cnt"),
            "fcltychartr": item.get("fcltychartr"),
            "sidonm": item.get("sidonm"),
            "gugunnm": item.get("gugunnm"),
            "opende": item.get("opende")
        }
        records.append(record)
    df = pd.DataFrame(records)
    rename_dict = {
        "mt10id": "시설ID",
        "fcltynm": "시설명",
        "mt13cnt": "공연장수",
        "fcltychartr": "시설특성코드",
        "sidonm": "시도명",
        "gugunnm": "구군명",
        "opende": "개관연도"
    }
    df = df.rename(columns=rename_dict)
    df.to_csv(filename, index=False, encoding="utf-8")
