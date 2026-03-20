import streamlit as st
import pandas as pd
import io
import requests

# [1] 화면 설정
st.set_page_config(page_title="마권연구소 PRO", layout="wide")
st.title("🏇 마권연구소 모바일 분석판 v3.0")

SHEET_ID = "1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk"

@st.cache_data(ttl=60)
def get_sheet_df(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        res = requests.get(url)
        res.encoding = 'utf-8'
        df = pd.read_csv(io.StringIO(res.text))
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# [2] 메인 데이터 로드 (출전표)
df_main = get_sheet_df("출전표")

if not df_main.empty:
    st.sidebar.header("🔍 검색 필터")
    
    # 1. 지역 선택 (이 선택에 따라 성적 탭도 바뀝니다)
    meets = sorted(df_main['meet'].unique()) if 'meet' in df_main.columns else ["제주", "서울", "부산"]
    target_meet = st.sidebar.selectbox("📍 지역 선택", meets)
    
    # 2. 해당 지역 성적 탭 미리 로드
    df_stat = get_sheet_df(target_meet) # '제주' 선택시 '제주' 탭 로드
    
    # 날짜/경주 필터링
    df_main['rcDate'] = df_main['rcDate'].astype(str)
    dates = sorted(df_main['rcDate'].unique(), reverse=True)
    target_date = st.sidebar.selectbox("📅 날짜 선택", dates)
    
    races = sorted(df_main[(df_main['meet']==target_meet) & (df_main['rcDate']==target_date)]['rcNo'].unique())
    target_rc = st.sidebar.select_slider("🚩 경주 번호", options=races)
    
    race_data = df_main[(df_main['meet']==target_meet) & (df_main['rcDate']==target_date) & (df_main['rcNo']==target_rc)].sort_values('chulNo')
    
    if not race_data.empty:
        dist = race_data['rcDist'].iloc[0]
        st.subheader(f"📍 {target_date} [{target_meet}] - 제 {target_rc}경주 ({dist}m)")
        st.divider()

        cols = st.columns(2)
        for idx, row in race_data.reset_index().iterrows():
            with cols[idx % 2]:
                with st.container(border=True):
                    hr_name = row['hrName']
                    
                    # [핵심] 성적 탭에서 해당 마필의 데이터 찾기
                    # 성적 탭의 말 이름 컬럼이 '마명' 또는 'hrName'이라고 가정합니다.
                    hr_stat = df_stat[df_stat['마명'] == hr_name] if '마명' in df_stat.columns else df_stat[df_stat['hrName'] == hr_name]
                    
                    # 2년 전적 데이터 추출 (항목명은 시트 상황에 맞게 보정)
                    # 예: '2년전적', '1착', '2착', '3착' 등
                    rc_cnt_2y = hr_stat['2년전적'].iloc[0] if not hr_stat.empty and '2년전적' in hr_stat.columns else 0
                    o1 = hr_stat['1착'].iloc[0] if not hr_stat.empty and '1착' in hr_stat.columns else 0
                    o2 = hr_stat['2착'].iloc[0] if not hr_stat.empty and '2착' in hr_stat.columns else 0
                    o3 = hr_stat['3착'].iloc[0] if not hr_stat.empty and '3착' in hr_stat.columns else 0
                    
                    # 연승률 계산 (1,2,3등 합계 / 총 출전)
                    place_rate = round(((o1 + o2 + o3) / rc_cnt_2y * 100), 1) if rc_cnt_2y > 0 else 0
                    
                    st.markdown(f"### **[{row['chulNo']}번] {hr_name}**")
                    
                    # 2년 전적 메트릭
                    m1, m2, m3 = st.columns(3)
                    m1.metric("2년 전적", f"{int(rc_cnt_2y)}전 {int(o1)}/{int(o2)}/{int(o3)}")
                    m2.metric("연승률", f"{place_rate}%")
                    m3.metric("부중", f"{row['wgBudam']}kg")
                    
                    st.caption(f"🏇 기수: {row['jkName']} | {row.get('sex','?')}/{row.get('age','?')}세 | 조교사: {row.get('trName','-')}")
    else:
        st.info("데이터를 찾을 수 없습니다.")
else:
    st.error("📡 시트 연결 오류!")
