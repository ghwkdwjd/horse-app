import streamlit as st
import pandas as pd
import io
import requests

# [1] 화면 설정: 아이패드/모바일 최적화
st.set_page_config(page_title="마권연구소 PRO", layout="wide")
st.title("🏇 마권연구소 모바일 분석판 v2.5")

# [2] 구글 시트 연결
SHEET_ID = "1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk"
SHEET_NAME = "출전표"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=60) # 1분마다 데이터 업데이트
def load_data():
    try:
        response = requests.get(URL)
        response.encoding = 'utf-8' # 한글 깨짐 방지
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = df.columns.str.strip() # 컬럼명 공백 제거
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
        # 경주 정보 상단 표시 (요청대로 거리 포함)
        dist = race_data['rcDist'].iloc[0]
        st.subheader(f"📍 {target_date} [{target_meet}] - 제 {target_rc}경주 ({dist}m)")
        st.divider()

        # [3] 말 정보 카드 출력 (2년 전적 중심으로 개편)
        cols = st.columns(2)
        for idx, row in race_data.reset_index().iterrows():
            with cols[idx % 2]:
                with st.container(border=True):
                    # 상단: 번호와 이름, 베스트 체중 (image_10.png 스타일)
                    best_wt = row.get('best_weight', '미정')
                    st.markdown(f"### **[{row['chulNo']}번] {row['hrName']}** <small style='color:red;'> (Best: {best_wt}kg)</small>", unsafe_allow_html=True)
                    
                    # 중간: 전체 성적 (파란색 박스)
                    r_cnt = int(row.get('rcCnt', 0)) # 전체 출전
                    o1 = int(row.get('ord1', 0))    # 1등
                    o2 = int(row.get('ord2', 0))    # 2등
                    st.info(f"📊 전체 성적: {r_cnt}전 {o1}/{o2}/..")

                    # [핵심 수정을 진행합니다] 메트릭 영역을 2년 전적 중심으로 변경
                    m1, m2, m3 = st.columns(3)
                    
                    # 1. 2년 전적 (예: 10전 2/1) - rcCnt2y, ord1_2y, ord2_2y 컬럼 필요
                    r_cnt_2y = int(row.get('rcCnt2y', 0))
                    o1_2y = int(row.get('ord1_2y', 0))
                    o2_2y = int(row.get('ord2_2y', 0))
                    m1.metric("2년 전적", f"{r_cnt_2y}전 {o1_2y}/{o2_2y}")
                    
                    # 2. 2년 복승률(%) 계산 및 표시
                    qa_rate_2y = round(((o1_2y + o2_2y) / r_cnt_2y * 100), 1) if r_cnt_2y > 0 else 0
                    m2.metric("2년 복승률", f"{qa_rate_2y}%")
                    
                    # 3. 부중
                    m3.metric("부중", f"{row['wgBudam']}kg")
                    
                    # 하단: 상세 정보 (기수 이름은 여기에 작게 표시)
                    st.write(f"🏇 기수: {row['jkName']} | {row.get('sex','?')}/{row.get('age','?')}세 | 조교사: {row.get('trName','-')}")
    else:
        st.info("데이터가 없습니다.")
else:
    st.error("📡 시트 데이터를 읽을 수 없습니다.")
