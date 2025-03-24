# main_facility.py
import pandas as pd
import os

from venue_list_collector import collect_prfplc_list
from production_company_list_collector import collect_mnfct_list
from festival_list_collector import collect_prffest_list
# 등등, 본인이 "한 번씩만" 호출하려는 collector들

def main():
    os.makedirs("./data", exist_ok=True)

    # 3. 공연시설 목록
    # 날짜 파라미터가 굳이 필요 없거나, afterdate 등 선택적으로
    df_venue = collect_prfplc_list(rows=100, shprfnmfct="", signgucode="11")  
    if df_venue is not None and not df_venue.empty:
        df_venue.to_csv("./data/venue_list.csv", index=False, encoding="utf-8-sig")
        print("[공연시설 목록] CSV 저장 완료:", len(df_venue))

    # 5. 기획/제작사 목록
    df_mnfct = collect_mnfct_list(rows=100)
    if df_mnfct is not None and not df_mnfct.empty:
        df_mnfct.to_csv("./data/mnfct_list.csv", index=False, encoding="utf-8-sig")
        print("[기획/제작사 목록] CSV 저장 완료:", len(df_mnfct))

if __name__ == "__main__":
    main()
