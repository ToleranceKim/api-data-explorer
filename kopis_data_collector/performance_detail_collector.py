import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_performance_detail(performance_id):
    """
    공연 상세 조회 API에서 DataFrame을 반환.
    """
    url = f"http://www.kopis.or.kr/openApi/restful/pblprfr/{performance_id}"
    params = {"service": SERVICE_KEY}
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.text)

    item = data_dict.get("dbs", {}).get("db", {})
    df = pd.DataFrame([item])

    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        # 필요하면 추가 매핑
    }
    df = df.rename(columns=rename_dict)

    return df
