import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="🐎 마권연구소 - 출전표", layout="wide")

# 2. 디자인 적용 (문법 에러 방지를 위해 깔끔하게 정리)
st.markdown("""
<style>
    .horse-card {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        background-color: white;
        margin-bottom: 15px;
    }
    .horse-no {
        font-size: 24px;
        font-weight: bold;
        color: white;
        background: #e74c3c;
        padding: 2px 10px;
        border-radius: 5px;
    }
    .horse-name {
        font-size: 20px;
        font-weight: bold;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
def load_data():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        # 파일이 같은 폴더에 있어야 합니다.
        creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
        client = gspread.authorize(creds)
        sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
        
        # 부산 시트 데이터 가져오기
        data = sh.worksheet("부산").get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame()

# 4. 화면 출력
st.title("🐎 부산 경마 출전표")

df = load_data()

if not df.empty:
    cols = st.columns(2)
    for i, row in df.iterrows():
        with cols[i % 2]:
            st.markdown(f"""
                <div class="horse-card">
                    <span class="horse-no">{row.get('no', i+1)}</span>
                    <span class="horse-name">{row.get('horseName', '미등록')}</span>
                    <div style="margin-top:10px;">
                        🏇 기수: {row.get('jockeyName', '-')} | ⚖️ 부중: {row.get('weight', '-')}kg<br>
                        📊 전적: {row.get('totalRun',0)}전 {row.get('firstPlace',0)}/{row.get('secondPlace',0)}/{row.get('thirdPlace',0)}
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("시트에 데이터가 없거나 연결이 안 되었습니다.")
