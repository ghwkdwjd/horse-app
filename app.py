import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="마권연구소 v5.0", layout="wide")

# 1. 디자인 (경마책 스타일)
st.markdown("""
    <style>
    .horse-card { border: 1px solid #ddd; border-radius: 10px; padding: 15px; background-color: white; margin-bottom: 12px; }
    .horse-name { font-size: 20px; font-weight: bold; color: #111; }
    .stats { font-size: 14px; color: #666; margin: 5px 0; }
    .grid { display: flex; justify-content: space-around; border-top: 1px solid #eee; padding-top: 10px; margin-top: 10px; }
    .val { font-size: 16px; font-weight: bold; color: #d32f2f; text-align: center; }
    .lbl { font-size: 11px; color: #888; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 불러오기 (캐시 적용으로 속도 향상)
@st.cache_data(ttl=600)
def get_data():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # 깃허브에 있는 secret_key.json 활용
    creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
    client = gspread.authorize(creds)
    # 주신 시트 ID
    sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
    # '부산' 탭 가져오기
    rows = sh.worksheet("부산").get_all_records()
    return pd.DataFrame(rows)

try:
    df = get_data()
    st.title("🐎 마권연구소 실시간 분석판 v5.0")
    
    cols = st.columns(2)
    for i, row in df.iterrows():
        with cols[i % 2]:
            # 통산전적 문자열 조합
            t, f, s, th = row.get('totalRun',0), row.get('firstPlace',0), row.get('secondPlace',0), row.get('thirdPlace',0)
            rate = f"{((f+s+th)/t*100):.1f}%" if t > 0 else "0%"
            
            st.markdown(f"""
                <div class="horse-card">
                    <div class="horse-name">[{row.get('no', i+1)}] {row.get('horseName', '미등록')}</div>
                    <div class="stats">📊 통산전적: {t}전 {f}/{s}/{th}</div>
                    <div class="grid">
                        <div><div class="lbl">연승률</div><div class="val">{rate}</div></div>
                        <div><div class="lbl">부중</div><div class="val">{row.get('weight', '-')}kg</div></div>
                        <div><div class="lbl">기수</div><div class="val" style="color:#333;">{row.get('jockeyName', '-')}</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"데이터 연동 에러: {e}")
