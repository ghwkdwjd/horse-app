import streamlit as st
import pandas as pd

# [1] 웹 화면 설정 (아이패드/모바일 최적화)
st.set_page_config(page_title="마권연구소 PRO", layout="wide")

st.title("🏇 마권연구소 모바일 분석판")

# [2] 구글 시트 연결 (직접 연결 방식)
# image_a8fc20.png에서 확인된 시트 ID를 사용합니다.
SHEET_ID = "1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=출전표"

@st.cache_data(ttl=600) # 10분마다 데이터 갱신
def load_data():
    try:
        df = pd.read_csv(URL)
        return df
    except:
        return pd.DataFrame()

# 데이터 불러오기
df = load_data()

if df.empty:
    st.error("📡 구글 시트 연결에 실패했습니다. 시트가 '링크가 있는 모든 사용자'에게 공개되어 있는지 확인해주세요.")
else:
    # [3] 필터 설정 (사이드바)
    st.sidebar.header("🔍 검색 필터")
    
    # 날짜 선택
    dates = sorted(df['rcDate'].unique(), reverse=True)
    target_date = st.sidebar.selectbox("경주 날짜", dates)
    
    # 해당 날짜의 경주 번호 추출
    available_rc = sorted(df[df['rcDate'] == target_date]['rcNo'].unique())
    target_rc = st.sidebar.select_slider("경주 번호", options=available_rc)

    # [4] 분석 카드 출력
    current_race = df[(df['rcDate'] == target_date) & (df['rcNo'] == target_rc)].sort_values('chulNo')
    
    st.subheader(f"📍 {target_date} - {target_rc}경주 출전 명단")
    
    # 아이패드 2열 배치
    cols = st.columns(2)
    for idx, row in current_race.reset_index().iterrows():
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### **[{row['chulNo']}번] {row['hrName']}**")
                
                c1, c2 = st.columns(2)
                c1.metric("기수", row['jkName'])
                c2.metric("부중", f"{row['wgBudam']}kg")
                
                st.caption(f"🏇 조교사: {row['trName']} | 거리: {row['rcDist']}m")
                st.divider()

st.sidebar.markdown("---")
st.sidebar.write("v1.0 Mobile Web")