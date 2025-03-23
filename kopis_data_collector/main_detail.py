# main_detail.py
import pandas as pd
import os

from performance_detail_collector import collect_pblprfr_detail
from venue_detail_collector import collect_prfplc_detail

def main():
    os.makedirs("./data", exist_ok=True)

    # 공연 상세
    df_perf_detail = collect_pblprfr_detail("PF132236")
    if df_perf_detail is not None and not df_perf_detail.empty:
        df_perf_detail.to_csv("./data/perf_detail_PF132236.csv", index=False, encoding="utf-8-sig")
        print("[공연 상세] PF132236 CSV 저장 완료")

    # 공연시설 상세
    df_venue_detail = collect_prfplc_detail("FC001247")
    if df_venue_detail is not None and not df_venue_detail.empty:
        df_venue_detail.to_csv("./data/venue_detail_FC001247.csv", index=False, encoding="utf-8-sig")
        print("[공연시설 상세] FC001247 CSV 저장 완료")

if __name__ == "__main__":
    main()
