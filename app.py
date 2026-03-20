import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="마권연구소 v5.0", layout="wide")

st.markdown("""
    <style>
    .horse-card { border: 1px solid #ddd; border-radius: 10px; padding: 15px; background-color: white; margin-bottom: 12px; box-shadow: 2px 2px 8px rgba(0,0,0,0.05); }
    .horse-name { font-size: 20px; font-weight: bold; color: #111; }
    .stats-line { font-size: 14px; color: #666; margin: 8px 0; }
    .grid-val { font-size: 16px; font-weight: bold; color: #d32f2f; text-align: center; }
    .grid-label { font-size: 11px; color: #888; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. 구글 시트 연동 (보여주신 secret_key.json 데이터 활용)
@st.cache_data(ttl=600) # 10분마다 데이터 새로고침
def load_sheet_data():
    # secret_key.json 내용을 기반으로 인증 (파일이 같은 폴더에 있어야 함)
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
    client = gspread.authorize(creds)
    
    # 시트 ID로 열기
    spreadsheet = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
    
    # 일단 '부산' 탭 데이터를 가져옵니다 (서울로 바꾸려면 이름만 변경)
    sheet = spreadsheet.worksheet("부산") 
    data = sheet.get_all_records()
    return pd.DataFrame(data)

try:
    df = load_sheet_data()
    
    st.title("🐎 마권연구소 실시간 분석판 v5.0")
    st.info("✅ 구글 시트 데이터 연동 성공!")

    # 3. 화면 출력 (2열 레이아웃)
    cols = st.columns(2)

    for i, row in df.iterrows():
        with cols[i % 2]:
            # 데이터 추출 (시트 컬럼명 기준)
            name = row.get('horseName', '미등록')
            total = row.get('totalRun', 0)
            f = row.get('firstPlace', 0)
            s = row.get('secondPlace', 0)
            t = row.get('thirdPlace', 0)
            weight = row.get('weight', '-')
            jockey = row.get('jockeyName', '-')
            
            # 연승률 계산
            rate = f"{((f+s+t)/total*100):.1f}%" if total > 0 else "0%"

            st.markdown(f"""
                <div class="horse-card">
                    <div class="horse-name">[{row.get('no', i+1)}] {name}</div>
                    <div class="stats-line">📊 통산전적: {total}전 {f}/{s}/{t}</div>
                    <div style="display: flex; justify-content: space-around; border-top: 1px solid #eee; padding-top: 10px;">
                        <div><div class="grid-label">연승률</div><div class="grid-val">{rate}</div></div>
                        <div><div class="grid-label">부중</div><div class="grid-val">{weight}kg</div></div>
                        <div><div class="grid-label">기수</div><div class="grid-val" style="color:#333; font-size:14px;">{jockey}</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ 데이터 로드 중 에러 발생: {e}")
    st.write("1. secret_key.json 파일이 깃허브에 있는지 확인하세요.")
    st.write("2. 구글 시트 공유 설정에 ghwkdwjd@ghwkdwjd.iam.gserviceaccount.com 이 추가되어 있는지 확인하세요.")
