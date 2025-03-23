# 15. 공연시설별 통계 목록 조회 (prfstsPrfByFctService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_prfbyfct(
    stdate,
    eddate,
    sharea=None,
    shprfnmfct=None,
    service_key=SERVICE_KEY
):
    """
    15. 공연시설별 통계 목록 조회(prfstsPrfByFctService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - sharea: 지역(시도)코드
    - shprfnmfct: 공연시설명
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsPrfByFct"
    params = {
        "service": service_key,
        "stdate": stdate,
        "eddate": eddate
    }
    if sharea:
        params["sharea"] = sharea
    if shprfnmfct:
        params["shprfnmfct"] = shprfnmfct

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("prfsts", {}).get("prfst", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "prfnmfct": item.get("prfnmfct"),
            "prfnmplc": item.get("prfnmplc"),
            "seatcnt": item.get("seatcnt"),
            "prfcnt": item.get("prfcnt"),
            "prfprocnt": item.get("prfprocnt"),
            "prfdtcnt": item.get("prfdtcnt"),
            "totnmrs": item.get("totnmrs")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "prfnmfct": "공연시설명",
        "prfnmplc": "공연장명",
        "seatcnt": "좌석수",
        "prfcnt": "공연건수",
        "prfprocnt": "개막편수",
        "prfdtcnt": "상연횟수",
        "totnmrs": "총티켓판매수"
    }
    df = df.rename(columns=rename_dict)

    return df
