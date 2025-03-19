import requests
import pandas as pd
import time
import os
from datetime import datetime, timedelta
import xmltodict
from dotenv import load_dotenv

# 환경변수에서 서비스 키 가져오기
load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_boxstats_day(start_date, end_date):
    # boxStats 일별 조회 후 CSV 저장
    # start_date, end_date는 YYYYMMDD 형식의 문자열

    url = "http://www.kopis.or.kr/openApi/restful/boxStats"
    params = {
        "service": SERVICE_KEY,
        "ststype": "day", 
        "stdate": start_date,
        "eddate": end_date
    }

    # GET 요청 보내기
    response = requests.get(url, params=params)

    # XML 응답을 딕셔너리로 파싱
    data_dict = xmltodict.parse(response.text)

    # box-statsofs -> boxStatsof 하위 항목에 데이터가 있음
    items = data_dict.get("box-statsofs", {}).get("boxStatsof", [])
    # 만약 한 개의 데이터면 dict 형태이므로, 리스트로 변환
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "prfdt": item.get("prfdt"),              # 날짜
            "prfcnt": item.get("prfcnt"),            # 공연 건수
            "prfdtcnt": item.get("prfdtcnt"),        # 상연 횟수
            "ntssnmrssm": item.get("ntssnmrssm"),    # 예매 수
            "cancelnmrssm": item.get("cancelnmrssm"),  # 취소 수
            "totnmrssm": item.get("totnmrssm"),        # 총 티켓 판매 수
            "ntssamountsm": item.get("ntssamountsm"),  # 총 티켓 판매액
            "stdate": start_date,                    # 요청 시작일
            "eddate": end_date,                      # 요청 종료일
            "ststype": "day"                         # 조회 유형
        }
        records.append(record)

    # records 리스트를 pandas DataFrame으로 변환
    df = pd.DataFrame(records)

    # 'prfdt'의 값이 "합계"인 행을 제거하여 개별 날짜 데이터만 남김
    df = df[df["prfdt"] != "합계"]

    # 열 이름을 사람이 읽기 쉬운 이름으로 변경
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

    # CSV 파일에 데이터를 추가(append) 모드로 저장
    df.to_csv("boxstats_period.csv", mode="a", index=False, header=False, encoding="utf-8")

def main():
    current = datetime(2024, 1, 1)
    end = datetime(2025, 2, 28)

    while current < end:
        period_end = current + timedelta(days=30) # 최대 31일 단위로 조회 (날짜 제한)
        if period_end > end:
            period_end = end

        st_str = current.strftime("%Y%m%d")
        ed_str = period_end.strftime("%Y%m%d")

        collect_boxstats_day(st_str, ed_str)

        # 다음 기간의 시작일로 업데이트
        current = period_end + timedelta(days=1)
        time.sleep(1) # API 과도 호출 방지

if __name__ == "__main__":
    main()