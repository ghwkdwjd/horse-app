import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 화면 설정
st.set_page_config(page_title="마권연구소 v5.0", layout="wide")

# 2. 데이터 불러오기 함수
@st.cache_data(ttl=600)
def load_data():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # 파일명이 secret_key.json 인지 꼭 확인!
    creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
    client = gspread.authorize(creds)
    
    # 주신 시트 ID
    sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
    # '부산' 탭 가져오기
    worksheet = sh.worksheet("부산")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# 3. 메인 화면 출력
try:
    df = load_data()
    st.title("🐎 마권연구소 실시간 분석판 v5.0")
    
    # 데이터가 잘 왔는지 확인용 (성공하면 나중에 경마책 디자인 입힐게요)
    st.success(f"데이터 연동 성공! 총 {len(df)}마리의 데이터가 확인되었습니다.")
    
    # 표 형태로 먼저 띄워보기
    st.dataframe(df)

except Exception as e:
    st.error(f"에러 발생: {e}")
    st.info("secret_key.json 파일이 깃허브에 있는지, 시트 공유 설정이 되어있는지 확인해주세요.")
