import streamlit as st
import pandas as pd
import io
import requests

st.set_page_config(page_title="마권연구소 PRO", layout="wide")
st.title("🏇 마권연구소 실시간 분석판 v3.5")

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

df_main = get_sheet_df("출전표")

if not df_main.empty:
    st.sidebar.header("🔍 검색 필터")
    meets = sorted(df_main['meet'].unique()) if 'meet' in df_main.columns else ["제주", "서울", "부산"]
    target_meet = st.sidebar.selectbox("📍 지역 선택", meets)
    
    # 성적 데이터 로드
    df_stat = get_sheet_df(target_meet)
    
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
                    
                    # [핵심] 성적 데이터에서 해당 말의 모든 기록 찾기
                    # 보내주신 컬럼명 중 '마명'을 기준으로 필터링합니다.
                    hr_records = df_stat[df_stat['마명'] == hr_name]
                    
                    if not hr_records.empty:
                        # 보내주신 리스트의 '순위' 컬럼을 숫자로 변환
                        hr_records['순위_num'] = pd.to_numeric(hr_records['순위'], errors='coerce')
                        
                        rc_cnt = len(hr_records) # 이 말의 총 경주 기록 수
                        o1 = len(hr_records[hr_records['순위_num'] == 1]) # 1등 횟수
                        o2 = len(hr_records[hr_records['순위_num'] == 2]) # 2등 횟수
                        o3 = len(hr_records[hr_records['순위_num'] == 3]) # 3등 횟수
                        
                        # 연승률 (1~3등 합계 / 총 출전)
                        place_rate = round(((o1 + o2 + o3) / rc_cnt * 100), 1) if rc_cnt > 0 else 0
                        stat_text = f"{rc_cnt}전 {o1}/{o2}/{o3}"
                    else:
                        stat_text = "기록 없음"
                        place_rate = 0
                    
                    st.markdown(f"### **[{row['chulNo']}번] {hr_name}**")
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("통산 전적", stat_text)
                    m2.metric("연승률", f"{place_rate}%")
                    m3.metric("부중", f"{row['wgBudam']}kg")
                    
                    # 하단 정보 (기수명, 조교사명 등 보내주신 이름으로 매칭)
                    st.caption(f"🏇 기수: {row.get('기수명', row.get('jkName', '-'))} | 조교사: {row.get('조교사명', row.get('trName', '-'))}")
    else:
        st.info("데이터가 없습니다.")
else:
    st.error("📡 시트 연결 오류!")
