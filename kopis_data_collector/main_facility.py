# main_facility.py
import pandas as pd
import os

from venue_list_collector import collect_prfplc_list
from production_company_list_collector import collect_mnfct_list
from festival_list_collector import collect_prffest_list
# 등등, 본인이 "한 번씩만" 호출하려는 collector들

def main():
    os.makedirs("./data", exist_ok=True)

    # (A) 공연시설 목록
    # 날짜 파라미터가 굳이 필요 없거나, afterdate 등 선택적으로
    df_venue = collect_prfplc_list(cpage=1, rows=100, shprfnmfct="", signgucode="11")  
    if df_venue is not None and not df_venue.empty:
        df_venue.to_csv("./data/venue_list.csv", index=False, encoding="utf-8-sig")
        print("[공연시설 목록] CSV 저장 완료:", len(df_venue))

    # (B) 기획/제작사 목록
    df_mnfct = collect_mnfct_list(cpage=1, rows=100)
    if df_mnfct is not None and not df_mnfct.empty:
        df_mnfct.to_csv("./data/mnfct_list.csv", index=False, encoding="utf-8-sig")
        print("[기획/제작사 목록] CSV 저장 완료:", len(df_mnfct))

    # (C) 축제 목록 (18번)
    # 축제 목록은 stdate~eddate를 넣어야 하긴 하지만, 필요 시 한 번만 호출
    df_festival = collect_prffest_list(stdate="20240101", eddate="20240131", cpage=1, rows=50)
    if df_festival is not None and not df_festival.empty:
        df_festival.to_csv("./data/festival_list.csv", index=False, encoding="utf-8-sig")
        print("[축제 목록] CSV 저장 완료:", len(df_festival))

    # 필요하다면 더 추가 (ex: 극작가 목록, 수상작 목록 등)
    # 사실 수상작 목록(17번)도 날짜 필요하지만, 짧은 구간이면 별도 루프 없이 한번 호출로 충분할 수도.

if __name__ == "__main__":
    main()
