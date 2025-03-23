# 13. 장르별 통계 목록 조회 (prfstsCateService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_cate(
    stdate,
    eddate,
    service_key=SERVICE_KEY
):
    """
    13. 장르별 통계 목록 조회(prfstsCateService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsCate"
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
            "cate": item.get("cate"),
            "prfprocnt": item.get("prfprocnt"),
            "prfdtcnt": item.get("prfdtcnt"),
            "amount": item.get("amount"),
            "amountshr": item.get("amountshr"),
            "nmrs": item.get("nmrs"),
            "nmrsshr": item.get("nmrsshr")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "cate": "장르",
        "prfprocnt": "개막편수",
        "prfdtcnt": "상연횟수",
        "amount": "매출액",
        "amountshr": "매출액점유율",
        "nmrs": "관객수",
        "nmrsshr": "관객점유율"
    }
    df = df.rename(columns=rename_dict)

    return df
