| **File Name**                            | **Service**                                           | **Description**                                                                                                                |
| ---------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **performance_list_collector.py**        | 1. 공연목록 조회 (pblprfrService)                     | 기간(최대 31일) 내 공연목록(공연ID, 공연명, 장르, 공연상태 등) 조회                                                            |
| **performance_detail_collector.py**      | 2. 공연 상세 조회 (pblprfrService)                    | 특정 공연ID의 상세 정보(출연진, 제작진, 런타임, 관람연령 등)                                                                   |
| **venue_list_collector.py**              | 3. 공연시설 목록 조회 (prfplcService)                 | 공연시설 목록(시설ID, 시설명, 지역, 공연장수, 개관연도 등) 조회                                                                |
| **venue_detail_collector.py**            | 4. 공연시설 상세 조회 (pblprfrService)                | 특정 공연시설ID의 상세 정보(좌석수, 편의시설, 전화번호, 주소 등), <br> 개발가이드 오류 - 엔드포인트 끝 pblprfr이 아닌 prfplc임 |
| **production_company_list_collector.py** | 5. 기획/제작사 목록 조회 (mnfctService)               | 기획/제작사 목록(기획사명, 장르, 전화번호, 최신작품 등) 조회                                                                   |
| **boxoffice_status_collector.py**        | 6. 예매상황판 조회 (boxofficeService)                 | 예매상황판(일자별/구간별 공연 순위, 공연명, 기간, 좌석수 등) 조회                                                              |
| **ticketstats_period_collector.py**      | 7. 예매통계 기간별 조회 (boxStatsService)             | 예매통계(일/주별) 예매수, 취소수, 총티켓판매수, 총티켓판매액 등 조회                                                           |
| **ticketstats_genre_collector.py**       | 8. 예매통계 장르별 조회 (boxStatsCateService)         | 장르별 예매통계(공연건수, 상연횟수, 예매수, 매출액 등) 조회                                                                    |
| **ticketstats_time_collector.py**        | 9. 예매통계 시간대별 조회 (boxStatsTimeService)       | 시간대별 예매통계(구간별 공연건수, 예매수, 판매액 등) 조회                                                                     |
| **ticketstats_price_collector.py**       | 10. 예매통계 가격대별 조회 (boxStatsPriceService)     | 가격대별 예매통계(예매수, 취소수, 총판매수, 매출액 등) 조회                                                                    |
| **perfstats_period_collector.py**        | 11. 기간별 통계 목록 조회 (prfstsTotalService)        | 공연통계(일/요일별) 개막편수, 상연횟수, 매출액, 관객수 등 조회                                                                 |
| **perfstats_area_collector.py**          | 12. 지역별 통계 목록 조회 (prfstsAreaService)         | 지역별 공연통계(공연시설수, 공연장수, 판매수, 매출액 등) 조회                                                                  |
| **perfstats_genre_collector.py**         | 13. 장르별 통계 목록 조회 (prfstsCateService)         | 장르별 공연통계(개막편수, 상연횟수, 매출액, 관객수 등) 조회                                                                    |
| **perfstats_byperformance_collector.py** | 14. 공연별 통계 목록 조회 (prfstsPrfByService)        | 공연별 통계(공연명, 공연시설명, 상연횟수, 기획/제작사 등) 조회                                                                 |
| **perfstats_byvenue_collector.py**       | 15. 공연시설별 통계 목록 조회 (prfstsPrfByFctService) | 공연시설별 통계(좌석수, 공연건수, 상연횟수, 총티켓판매수 등) 조회                                                              |
| **perfstats_price_collector.py**         | 16. 가격대별 통계 목록 조회 (prfstsPriceService)      | 가격대별 공연통계(예매수, 예매액, 취소수 등) 조회                                                                              |
| **awards_list_collector.py**             | 17. 수상작 목록 조회 (prfawadService)                 | 수상작 목록(공연ID, 공연명, 시설명, 수상실적 등) 조회                                                                          |
| **festival_list_collector.py**           | 18. 축제 목록 조회 (prffestService)                   | 축제 목록(공연ID, 공연명, 기간, 시설명, 축제여부 등) 조회                                                                      |
| **playwright_list_collector.py**         | 19. 극작가 목록 조회 (prferService)                   | 극작가 목록(공연명, 원작자·창작자, 공연장르, 공연상태 등) 조회                                                                 |

---

### cpage & rows 지원 서비스 목록

- (1번) 공연목록 조회   (pblprfrService) : cpage 로직 완료
- (3번) 공연시설 목록 조회   (prfplcService) : cpage 로직 완료
- (5번) 기획/제작사 목록 조회   (mnfctService) : cpage 로직 완료
- (14번) 공연별 통계 목록 조회   (prfstsPrfByService) : cpage 로직 완료
- (15번) 공연시설별 통계 목록 조회   (prfstsPrfByFctService) : cpage 로직 완료
- (17번) 수상작 목록 조회   (prfawadService) : cpage 로직 완료
- (18번) 축제 목록 조회   (prffestService) : cpage 로직 완료
- (19번) 극작가 목록 조회   (prferService) : cpage 로직 완료

다음 확인 사항

1. main_detail.py, main_facility.py 정상 동작 확인 o
2. (11) 기간별 통계 결과 없음, (12) 지역별 통계 결과 없음, (13) 장르별 통계 결과 없음 디버깅
3. 장기간 수집 테스트
4. 분석 모델링
