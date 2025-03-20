import time
from datetime import datetime, timedelta
import pandas as pd

from performance_list_collector import collect_performance_list
from performance_stats_collector import collect_performance_stats
from boxoffice_collector import collect_boxstats_day
from venue_collector import collect_venue_list
from performance_detail_collector import collect_performance_detail

def main():
    # 전체 수집 기간 설정 (예: 20240101부터 20250131까지)
    start_date_str = "20240101"
    end_date_str = "20250131"
    
    current = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")
    
    # 각 수집 결과를 저장할 DataFrame 리스트
    performance_list_dfs = []
    performance_stats_dfs = []
    boxstats_dfs = []
    
    # 날짜 범위를 30일 단위로 분할하여 API 호출 후 DataFrame 반환 받기
    while current <= end_date:
        period_end = current + timedelta(days=30)
        if period_end > end_date:
            period_end = end_date
        
        segment_start_str = current.strftime("%Y%m%d")
        segment_end_str = period_end.strftime("%Y%m%d")
        
        print(f"수집 기간: {segment_start_str} ~ {segment_end_str}")
        
        # 공연목록 수집 (반환값이 DataFrame이라고 가정)
        df_list = collect_performance_list(segment_start_str, segment_end_str, cpage=1, rows=100)
        if df_list is not None:
            performance_list_dfs.append(df_list)
        
        # 특정 공연(장르 AAAA)에 대한 공연별 통계 수집
        df_stats = collect_performance_stats(segment_start_str, segment_end_str, shcate="AAAA", shprfnm="", cpage=1, rows=10)
        if df_stats is not None:
            performance_stats_dfs.append(df_stats)
        
        # 박스스탯(예매 통계) 수집
        df_box = collect_boxstats_day(segment_start_str, segment_end_str)
        if df_box is not None:
            boxstats_dfs.append(df_box)
        
        # API 과도 호출 방지를 위해 1초 대기
        time.sleep(1)
        
        # 다음 기간 시작일 업데이트
        current = period_end + timedelta(days=1)
    
    # 수집된 DataFrame들을 모두 병합하여 하나의 CSV 파일로 저장
    if performance_list_dfs:
        combined_performance_list = pd.concat(performance_list_dfs, ignore_index=True)
        combined_performance_list.to_csv("./data/performance_list_merged.csv", index=False, encoding="utf-8-sig")
        print(f"통합 공연목록 CSV 저장 완료: {len(combined_performance_list)} 건")
    
    if performance_stats_dfs:
        combined_performance_stats = pd.concat(performance_stats_dfs, ignore_index=True)
        combined_performance_stats.to_csv("./data/performance_stats_merged.csv", index=False, encoding="utf-8-sig")
        print(f"통합 공연별 통계 CSV 저장 완료: {len(combined_performance_stats)} 건")
    
    if boxstats_dfs:
        combined_boxstats = pd.concat(boxstats_dfs, ignore_index=True)
        combined_boxstats.to_csv("./data/boxstats_merged.csv", index=False, encoding="utf-8-sig")
        print(f"통합 박스스탯 CSV 저장 완료: {len(combined_boxstats)} 건")
    
    # # 공연시설 목록 수집 (날짜에 영향 없이 한번 호출)
    # df_venue = collect_venue_list(cpage=1, rows=10, shprfnmfct="예술의전당", signgucode="11", signgucodesub="1156")
    # if df_venue is not None:
    #     df_venue.to_csv("./data/venue_list.csv", index=False, encoding="utf-8-sig")
    #     print("공연시설 목록 CSV 저장 완료.")
    
    # 공연 상세 조회 (특정 공연 ID에 대해 한번 호출)
    df_detail = collect_performance_detail("PF132236")
    if df_detail is not None:
        df_detail.to_csv("./data/performance_detail_PF132236.csv", index=False, encoding="utf-8-sig")
        print("공연 상세 조회 CSV 저장 완료.")

if __name__ == "__main__":
    main()

