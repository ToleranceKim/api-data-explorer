# 12. 지역별 통계 목록 조회 (prfstsAreaService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_area(
    stdate,
    eddate,
    service_key=SERVICE_KEY
):
    """
    12. 지역별 통계 목록 조회(prfstsAreaService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsArea"
    params = {
        "service": service_key,
        "stdate": stdate,
        "eddate": eddate
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("Prfsts", {}).get("prfst", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "area": item.get("area"),
            "fcltycnt": item.get("fcltycnt"),
            "prfplccnt": item.get("prfplccnt"),
            "seatcnt": item.get("seatcnt"),
            "prfcnt": item.get("prfcnt"),
            "prfprcnt": item.get("prfprcnt"),
            "prfdtcnt": item.get("prfdtcnt"),
            "nmrs": item.get("nmrs"),
            "nmrcancl": item.get("nmrcancl"),
            "totnmrs": item.get("totnmrs"),
            "amount": item.get("amount")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "area": "지역",
        "fcltycnt": "공연시설수",
        "prfplccnt": "공연장수",
        "seatcnt": "총좌석수",
        "prfcnt": "공연건수",
        "prfprcnt": "개막편수",
        "prfdtcnt": "상연횟수",
        "nmrs": "판매수",
        "nmrcancl": "취소수",
        "totnmrs": "총티켓판매수",
        "amount": "총티켓판매액"
    }
    df = df.rename(columns=rename_dict)

    return df
