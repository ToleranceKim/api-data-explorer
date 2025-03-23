# 11. 기간별 통계 목록 조회 (prfstsTotalService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_total(
    ststype,
    stdate,
    eddate,
    service_key=SERVICE_KEY
):
    """
    11. 공연통계 기간별 통계 목록 조회(prfstsTotalService)

    - ststype: 날짜코드(day, dayWeek)
    - stdate, eddate: YYYYMMDD (최대 31일)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsTotal"
    params = {
        "service": service_key,
        "ststype": ststype,
        "stdate": stdate,
        "eddate": eddate
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("prfSts", {}).get("prfSt", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "prfdt": item.get("prfdt"),
            "prfprocnt": item.get("prfprocnt"),
            "prfdtcnt": item.get("prfdtcnt"),
            "amount": item.get("amount"),
            "nmrs": item.get("nmrs"),
            "prfcnt": item.get("prfcnt"),
            "ntssnmrs": item.get("ntssnmrs"),
            "cancelnmrs": item.get("cancelnmrs")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "prfdt": "기준값(날짜_또는_요일)",
        "prfprocnt": "개막편수",
        "prfdtcnt": "상연횟수",
        "amount": "매출액",
        "nmrs": "총티켓판매수",
        "prfcnt": "공연건수",
        "ntssnmrs": "판매수",
        "cancelnmrs": "취소수"
    }
    df = df.rename(columns=rename_dict)

    return df
