import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 구글 시트 연동 (캐싱 처리로 속도 향상)
@st.cache_data
def get_data_from_sheets():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    # 파일명은 본인의 JSON 키 파일 이름으로 확인하세요!
    creds = Credentials.from_service_account_file('key.json', scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 제목 확인: '마권연구소 데이터'
    spreadsheet = client.open("마권연구소 데이터")
    sheet = spreadsheet.get_worksheet(0)
    
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# 2. 웹 화면 구성
st.set_page_config(page_title="마권연구소 분석기", layout="wide")
st.title("🏇 마권연구소 데이터 대시보드")

try:
    df = get_data_from_sheets()

    # 사이드바: 필터 설정
    st.sidebar.header("🔍 검색 및 필터")
    
    # 말이름(hrName)으로 검색
    search_horse = st.sidebar.text_input("말이름(hrName) 검색", "")
    
    # 기수명(jkName)으로 선택 필터
    all_jockeys = ["전체"] + sorted(df['jkName'].unique().tolist())
    selected_jockey = st.sidebar.selectbox("기수(jkName) 선택", all_jockeys)

    # 데이터 필터링 로직
    filtered_df = df.copy()
    if search_horse:
        filtered_df = filtered_df[filtered_df['hrName'].str.contains(search_horse, na=False)]
    if selected_jockey != "전체":
        filtered_df = filtered_df[filtered_df['jkName'] == selected_jockey]

    # 메인 화면 레이아웃
    st.success(f"총 {len(filtered_df)}개의 데이터를 불러왔습니다.")
    
    # 표 출력
    st.dataframe(filtered_df, use_container_width=True)

    # 간단한 통계 (예: 거리별 데이터 수)
    if not filtered_df.empty:
        st.divider()
        st.subheader("📊 간단 요약")
        dist_count = filtered_df['dist'].value_counts()
        st.bar_chart(dist_count)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.info("팁: 구글 시트 이름과 JSON 키 파일 경로를 다시 확인해 보세요!")
