import streamlit as st
import pandas as pd
import io
import requests

# [1] 화면 설정
st.set_page_config(page_title="마권연구소 PRO", layout="wide")
st.title("🏇 마권연구소 모바일 분석판 v2.0")

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
    
    # 지역/날짜/경주 선택
    meets = sorted(df['meet'].unique()) if 'meet' in df.columns else []
    target_meet = st.sidebar.selectbox("📍 지역 선택", meets)
    df = df[df['meet'] == target_meet]

    df['rcDate'] = df['rcDate'].astype(str)
    dates = sorted(df['rcDate'].unique(), reverse=True)
    target_date = st.sidebar.selectbox("📅 날짜 선택", dates)
    df = df[df['rcDate'] == target_date]
    
    races = sorted(df['rcNo'].unique())
    target_rc = st.sidebar.select_slider("🚩 경주 번호", options=races)
    
    race_data = df[df['rcNo'] == target_rc].sort_values('chulNo')
    
    if not race_data.empty:
        # 경주 정보 상단 표시
        dist = race_data['rcDist'].iloc[0]
        st.subheader(f"📍 {target_date} [{target_meet}] - 제 {target_rc}경주 ({dist}m)")
        st.divider()

        # [3] 말 정보 카드 출력 (요청하신 상세 성적 추가)
        cols = st.columns(2)
        for idx, row in race_data.reset_index().iterrows():
            with cols[idx % 2]:
                with st.container(border=True):
                    # 상단: 번호와 이름, 그리고 베스트 체중
                    best_wt = row.get('best_weight', '미정') # 시트에 베스트 체중 컬럼이 있다고 가정
                    st.markdown(f"### **[{row['chulNo']}번] {row['hrName']}** <span style='color:red; font-size:15px;'> (Best: {best_wt}kg)</span>", unsafe_allow_html=True)
                    
                    # 중간: 성적 데이터 (예: 1전 1/0/0 100%)
                    r_cnt = int(row.get('rcCnt', 0)) # 총 출전 횟수
                    o1 = int(row.get('ord1', 0))      # 1위 횟수
                    o2 = int(row.get('ord2', 0))      # 2위 횟수
                    o3 = int(row.get('ord3', 0))      # 3위 횟수
                    win_rate = round((o1 / r_cnt * 100), 1) if r_cnt > 0 else 0
                    
                    st.info(f"📊 성적: {r_cnt}전 {o1}/{o2}/{o3} | 승률: {win_rate}%")

                    # 하단 메트릭: 기수 정보 및 기승 횟수
                    c1, c2, c3 = st.columns(3)
                    c1.metric("기수", str(row['jkName']))
                    c2.metric("부중", f"{row['wgBudam']}kg")
                    # 기수와 말의 호흡 (시트에 관련 컬럼이 있다면 사용)
                    jk_rc_cnt = row.get('jk_rc_cnt', '-') 
                    c3.metric("기승횟수", f"{jk_rc_cnt}회")
                    
                    # 상세 정보
                    st.write(f"🏇 {row.get('sex','?')}/{row.get('age','?')}세 | 조교사: {row.get('trName','-')} | 마주: {row.get('ownName','-')}")
    else:
        st.info("데이터가 없습니다.")
else:
    st.error("📡 시트 데이터를 읽을 수 없습니다.")
