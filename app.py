import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="🐎 마권연구소 v5.0", layout="wide")

def load_data():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        # 파일 이름을 확인하세요! 목록에 있는 것과 대소문자까지 똑같아야 합니다.
        creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
        client = gspread.authorize(creds)
        
        # 시트 ID 확인
        sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
        data = sh.worksheet("부산").get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        # 에러 메시지를 화면에 출력
        st.error(f"⚠️ 연결 실패: {e}")
        return pd.DataFrame()

st.title("🐎 부산 경마 출전표")

df = load_data()

if not df.empty:
    st.success("✅ 데이터 로드 성공!")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("데이터가 없습니다. 'secret_key.json' 내용을 다시 붙여넣고 저장해 보세요.")
