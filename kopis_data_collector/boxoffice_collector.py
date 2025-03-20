import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_boxstats_day(start_date, end_date):
    """
    예매통계 기간별 조회(boxStats) API에서 DataFrame을 반환만 하는 함수.
    """
    url = "http://www.kopis.or.kr/openApi/restful/boxStats"
    params = {
        "service": SERVICE_KEY,
        "ststype": "day",
        "stdate": start_date,
        "eddate": end_date
    }
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.text)

    items = data_dict.get("box-statsofs", {}).get("boxStatsof", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "prfdt": item.get("prfdt"),
            "prfcnt": item.get("prfcnt"),
            "prfdtcnt": item.get("prfdtcnt"),
            "ntssnmrssm": item.get("ntssnmrssm"),
            "cancelnmrssm": item.get("cancelnmrssm"),
            "totnmrssm": item.get("totnmrssm"),
            "ntssamountsm": item.get("ntssamountsm"),
            "stdate": start_date,
            "eddate": end_date,
            "ststype": "day"
        }
        records.append(record)

    df = pd.DataFrame(records)
    # '합계' 행 제거
    df = df[df["prfdt"] != "합계"]

    # 컬럼명 매핑
    rename_dict = {
        "prfdt": "날짜",
        "prfcnt": "공연건수",
        "prfdtcnt": "상연횟수",
        "ntssnmrssm": "예매수",
        "cancelnmrssm": "취소수",
        "totnmrssm": "총티켓판매수",
        "ntssamountsm": "총티켓판매액",
        "stdate": "조회시작일",
        "eddate": "조회종료일",
        "ststype": "조회타입"
    }
    df = df.rename(columns=rename_dict)

    # DataFrame 반환
    return df
