import streamlit as st
import pandas as pd
import io
import requests

# [1] 화면 설정
st.set_page_config(page_title="마권연구소 PRO", layout="wide")
st.title("🏇 마권연구소 모바일 분석판")

# [2] 구글 시트 연결
SHEET_ID = "1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk"
SHEET_NAME = "출전표"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=60)
def load_data():
    try:
        response = requests.get(URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.sidebar.header("🔍 검색 필터")
    
    # 1. 지역 선택
    meets = sorted(df['meet'].unique()) if 'meet' in df.columns else []
    target_meet = st.sidebar.selectbox("📍 지역 선택", meets)
    df = df[df['meet'] == target_meet]

    # 2. 날짜 선택
    df['rcDate'] = df['rcDate'].astype(str)
    dates = sorted(df['rcDate'].unique(), reverse=True)
    target_date = st.sidebar.selectbox("📅 날짜 선택", dates)
    df = df[df['rcDate'] == target_date]
    
    # 3. 경주 번호 선택
    races = sorted(df['rcNo'].unique())
    target_rc = st.sidebar.select_slider("🚩 경주 번호", options=races)
    
    # 데이터 필터링
    race_data = df[df['rcNo'] == target_rc].sort_values('chulNo')
    
    if not race_data.empty:
        # [4] 경주 거리 정보 - 상단 제목 옆으로 이동 (사용자 요청 반영)
        dist = race_data['rcDist'].iloc[0]
        st.subheader(f"📍 {target_date} [{target_meet}] - 제 {target_rc}경주 ({dist}m)")
        st.divider()

        # [5] 말 정보 카드 출력 (오류 해결 버전)
        cols = st.columns(2)
        for idx, row in race_data.reset_index().iterrows():
            with cols[idx % 2]:
                with st.container(border=True):
                    # 성별/나이/산지 정보 안전하게 가져오기
                    sex = row.get('sex', '?')
                    age = row.get('age', '?')
                    prd = row.get('prd', '?')
                    
                    # 제목: [번호] 말 이름 (상세스펙)
                    st.markdown(f"### **[{row['chulNo']}번] {row['hrName']}**")
                    st.caption(f"({sex} / {age}세 / {prd})")
                    
                    c1, c2 = st.columns(2)
                    c1.metric("기수", str(row['jkName']))
                    c2.metric("부중", f"{row['wgBudam']}kg")
                    
                    # 하단 조교사/마주 정보
                    tr = row.get('trName', '미정')
                    own = row.get('ownName', '미정')
                    st.write(f"🏇 **조교사:** {tr} | **마주:** {own}")
    else:
        st.info("데이터가 없습니다.")
else:
    st.error("📡 시트 데이터를 읽을 수 없습니다.")
