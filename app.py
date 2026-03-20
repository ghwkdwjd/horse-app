import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 페이지 설정 (아이패드에서 보기 좋게 넓게 설정)
st.set_page_config(page_title="🐎 마권연구소 v5.0", layout="wide")

# 2. 데이터 로드 함수 (오류 처리를 더 꼼꼼하게 보강)
def load_data():
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        # 같은 폴더에 있는 secret_key.json 파일을 사용합니다.
        creds = Credentials.from_service_account_file("secret_key.json", scopes=scope)
        client = gspread.authorize(creds)
        
        # 구글 시트 ID 연결
        sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
        
        # '부산' 시트 데이터 가져오기 (가장 흔하게 쓰는 방식)
        worksheet = sh.worksheet("부산")
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    
    except Exception as e:
        # 인증 오류(JWT Signature) 등이 발생하면 구체적인 메시지를 띄웁니다.
        st.error(f"⚠️ 데이터 로드 실패: {e}")
        return pd.DataFrame()

# 3. 메인 화면 출력
st.title("🐎 부산 경마 출전표")

df = load_data()

if not df.empty:
    st.success("✅ 데이터를 성공적으로 불러왔습니다!")
    # 데이터가 너무 많을 수 있으니 상위 20개만 먼저 확인
    st.dataframe(df, use_container_width=True)
else:
    st.warning("현재 표시할 데이터가 없습니다. 'secret_key.json' 내용이 원본과 일치하는지 확인해주세요.")
