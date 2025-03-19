import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_performance_detail(performance_id, filename=None):
    if filename is None:
        filename = f"data/performance_detail_{performance_id}.csv"
    url = f"http://www.kopis.or.kr/openApi/restful/pblprfr/{performance_id}"
    params = {"service": SERVICE_KEY}
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.text)
    item = data_dict.get("dbs", {}).get("db", {})
    df = pd.DataFrame([item])
    # 컬럼명 매핑 예시 (필요한 경우 추가 수정)
    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        # 다른 필드도 필요에 따라 추가
    }
    df = df.rename(columns=rename_dict)
    df.to_csv(filename, index=False, encoding="utf-8")
    return item
