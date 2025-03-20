import time
from datetime import datetime, timedelta
from performance_list_collector import collect_performance_list
from performance_stats_collector import collect_performance_stats
from venue_collector import collect_venue_list
from boxoffice_collector import collect_boxstats_day
from performance_detail_collector import collect_performance_detail

def main():
    # 전체 수집 기간 설정 (예: 20240101부터 20250131까지)
    start_date_str = "20240101"
    end_date_str = "20250131"
    
    current = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")
    
    # 공연목록, 공연별 통계, 박스스탯은 날짜 범위가 필요하므로 기간 분할하여 호출
    while current <= end_date:
        # 최대 31일 이하로 조회 (여기서는 30일 단위로 설정)
        period_end = current + timedelta(days=30)
        if period_end > end_date:
            period_end = end_date
        
        segment_start_str = current.strftime("%Y%m%d")
        segment_end_str = period_end.strftime("%Y%m%d")
        
        print(f"수집 기간: {segment_start_str} ~ {segment_end_str}")
        
        # 공연목록 수집
        collect_performance_list(segment_start_str, segment_end_str, cpage=1, rows=100)
        
        # 특정 공연(장르 AAAA)에 대한 공연별 통계 수집
        collect_performance_stats(segment_start_str, segment_end_str, shcate="AAAA", shprfnm="", cpage=1, rows=10)
        
        # 박스스탯(예매 통계) 수집
        collect_boxstats_day(segment_start_str, segment_end_str)
        
        # 호출 후 1초 대기 (API 과도 호출 방지)
        time.sleep(1)
        
        # 다음 기간 시작일 업데이트
        current = period_end + timedelta(days=1)
    
    # 공연시설 목록은 날짜에 영향을 받지 않으므로 별도로 한번 호출
    collect_venue_list(cpage=1, rows=10, shprfnmfct="예술의전당", signgucode="11", signgucodesub="1111")
    
    # 공연 상세 조회는 특정 공연 ID에 대해 호출 (날짜와 무관하므로 한번만 호출)
    collect_performance_detail("PF132236")

if __name__ == "__main__":
    main()

