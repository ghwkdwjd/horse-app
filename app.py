import streamlit as st
import pandas as pd
import io
import requests

# [1] 화면 설정: 아이패드/모바일 최적화
st.set_page_config(page_title="마권연구소 PRO", layout="wide")
st.title("🏇 마권연구소 모바일 분석판")

# [2] 구글 시트 정보 (직접 연결 방식)
SHEET_ID = "1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk"
SHEET_NAME = "출전표"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=60)
def load_data():
    try:
        response = requests.get(URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(io.StringIO(response.text))
        # 항목 이름 앞뒤의 불필요한 공백을 완전히 제거
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # [3] 필터 설정 (사이드바)
    st.sidebar.header("🔍 검색 필터")
    
    # 날짜 컬럼 확인
    date_col = 'rcDate' if 'rcDate' in df.columns else df.columns[1] # rcDate가 없으면 두번째 컬럼 사용
    df[date_col] = df[date_col].astype(str)
    dates = sorted(df[date_col].unique(), reverse=True)
    target_date = st.sidebar.selectbox("📅 날짜 선택", dates)
    
    day_df = df[df[date_col] == target_date]
    
    # 경주번호 컬럼 확인
    rc_col = 'rcNo' if 'rcNo' in day_df.columns else 'rcNo'
    if rc_col in day_df.columns:
        races = sorted(day_df[rc_col].unique())
        target_rc = st.sidebar.select_slider("🚩 경주 번호", options=races)
        
        # [4] 결과 출력
        race_data = day_df[day_df[rc_col] == target_rc].sort_values('chulNo')
        st.subheader(f"📍 {target_date} - 제 {target_rc}경주")
        
        # 카드 형식 출력
        for idx, row in race_data.iterrows():
            with st.container(border=True):
                st.markdown(f"### **[{row['chulNo']}번] {row['hrName']}**")
                c1, c2, c3 = st.columns(3)
                c1.metric("기수", str(row['jkName']))
                c2.metric("부중", f"{row['wgBudam']}kg")
                c3.metric("거리", f"{row['rcDist']}m")
                # 에러 방지를 위해 안전하게 표시
                tr = row.get('trName', '미정')
                own = row.get('ownName', '미정')
                st.caption(f"🏇 조교사: {tr} | 마주: {own}")
else:
    st.error("📡 시트 데이터를 읽을 수 없습니다. 구글 시트 공유 설정을 확인하세요!")
