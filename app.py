import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="🐎 마권연구소 - 출전표", layout="wide")

# 데이터 로드 함수
def load_data():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        # 깃허브에 올린 secret_key.json 파일을 읽습니다.
        creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
        client = gspread.authorize(creds)
        
        # 구글 시트 ID 연결
        sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
        
        # '부산' 시트 데이터 가져오기
        data = sh.worksheet("부산").get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame()

# 화면 출력
st.title("🐎 부산 경마 출전표")

df = load_data()

if not df.empty:
    # 모바일에서 보기 좋게 표 형태로 먼저 출력
    st.write("### 실시간 출전마 명단")
    st.dataframe(df, use_container_width=True)
else:
    st.info("시트에 데이터가 없거나 'secret_key.json' 인식이 안 되었습니다.")
