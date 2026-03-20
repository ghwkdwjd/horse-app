import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="🐎 마권연구소", layout="wide")

# 2. 데이터 불러오기 (초기 방식: 폴더 내 파일 직접 읽기)
def load_data():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        # 폴더에 있는 파일을 바로 읽습니다.
        creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
        client = gspread.authorize(creds)
        
        # 구글 시트 연결
        sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
        return pd.DataFrame(sh.worksheet("부산").get_all_records())
    except Exception as e:
        st.error(f"연결 실패: {e}")
        return pd.DataFrame()

# 3. 화면 출력
st.title("🐎 실시간 부산 출전표")

df = load_data()

if not df.empty:
    st.success("연결 성공!")
    st.dataframe(df, use_container_width=True)
else:
    st.info("데이터가 없습니다. 폴더에 'secret_key.json'이 있는지 확인해주세요.")
