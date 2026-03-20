import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 구글 시트 연동 함수
def load_data():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # 깃허브에 올린 파일명이 secret_key.json 인지 확인!
    creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
    client = gspread.authorize(creds)
    
    # 주신 시트 ID 활용
    sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
    # '부산' 탭 가져오기
    worksheet = sh.worksheet("부산")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# 데이터 로드 시도
try:
    entries = load_data()
    
    # --- 여기서부터는 아까 드린 [디자인 코드]를 그대로 쓰시면 됩니다 ---
    st.title("🐎 마권연구소 실시간 분석판 v5.0")
    
    cols = st.columns(2)
    for i, row in entries.iterrows():
        with cols[i % 2]:
            st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <h3>[{row.get('no', i+1)}] {row.get('horseName', '미등록')}</h3>
                    <p>통산전적: {row.get('totalRun',0)}전 {row.get('firstPlace',0)}/{row.get('secondPlace',0)}/{row.get('thirdPlace',0)}</p>
                    <p>기수: {row.get('jockeyName', '-')}</p>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"에러 발생: {e}")
