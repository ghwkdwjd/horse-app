import streamlit as st
import pandas as pd
import io
import requests

# [1] 화면 및 기본 설정
st.set_page_config(page_title="마권연구소 PRO", layout="wide")
st.title("🏇 마권연구소 실시간 분석판 v4.0")

# 구글 시트 ID (공유 설정 확인 필수)
SHEET_ID = "1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk"

@st.cache_data(ttl=60)
def get_sheet_df(sheet_name):
    """구글 시트의 특정 탭을 읽어오는 함수"""
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        res = requests.get(url)
        res.encoding = 'utf-8'
        df = pd.read_csv(io.StringIO(res.text))
        # 데이터 정제: 모든 컬럼명과 텍스트 데이터의 앞뒤 공백 제거
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        return pd.DataFrame()

# [2] 메인 데이터 로드 (출전표 탭)
df_main = get_sheet_df("출전표")

if not df_main.empty:
    # 사이드바 필터 설정
    st.sidebar.header("🔍 검색 필터")
    
    # 1. 지역 선택 (서울/부산/제주)
    meets = sorted(df_main['meet'].unique()) if 'meet' in df_main.columns else ["서울", "제주", "부산"]
    target_meet = st.sidebar.selectbox("📍 지역 선택", meets)
    
    # 2. 선택한 지역의 성적 탭 로드 (서울 선택 시 '서울' 탭 읽기)
    df_stat = get_sheet_df(target_meet)
    
    # 3. 날짜 및 경주 번호 선택
    df_main['rcDate'] = df_main['rcDate'].astype(str)
    dates = sorted(df_main[df_main['meet'] == target_meet]['rcDate'].unique(), reverse=True)
    if not dates:
        dates = ["데이터 없음"]
    target_date = st.sidebar.selectbox("📅 날짜 선택", dates)
    
    r_list = df_main[(df_main['meet']==target_meet) & (df_main['rcDate']==target_date)]['rcNo'].unique()
    target_rc = st.sidebar.select_slider("🚩 경주 번호", options=sorted(r_list)) if len(r_list) > 0 else 1
    
    # [3] 필터링된 경주 데이터
    race_data = df_main[(df_main['meet']==target_meet) & (df_main['rcDate']==target_date) & (df_main['rcNo']==target_rc)].sort_values('chulNo')
    
    if not race_data.empty:
        # 상단 경주 정보 (거리 표시)
        dist = race_data['rcDist'].iloc[0] if 'rcDist' in race_data.columns else "-"
        st.subheader(f"📍 {target_date} [{target_meet}] - 제 {target_rc}경주 ({dist}m)")
        st.divider()

        # [4] 말 정보 카드 출력 (2열 배치)
        cols = st.columns(2)
        for idx, row in race_data.reset_index().iterrows():
            with cols[idx % 2]:
                with st.container(border=True):
                    # 고유번호(hrNo)와 이름 가져오기
                    hr_no = str(row.get('hrNo', '')).strip()
                    hr_name = row.get('hrName', '이름없음')
                    
                    # [핵심] 성적 탭에서 고유번호(마번)로 데이터 매칭
                    # 성적 탭의 고유번호 컬럼명이 '마번'인지 확인
                    stat_col = '마번' if '마번' in df_stat.columns else 'hrNo'
                    
                    if not df_stat.empty and stat_col in df_stat.columns:
                        # 고유번호로 필터링 (문자열로 변환하여 비교)
                        hr_records = df_stat[df_stat[stat_col].astype(str).str.strip() == hr_no]
                        
                        if not hr_records.empty:
                            # 순위 데이터를 숫자로 변환하여 1, 2, 3등 계산
                            hr_records['순위_num'] = pd.to_numeric(hr_records['순위'], errors='coerce')
                            
                            rc_cnt = len(hr_records)
                            o1 = len(hr_records[hr_records['순위_num'] == 1])
                            o2 = len(hr_records[hr_records['순위_num'] == 2])
                            o3 = len(hr_records[hr_records['순위_num'] == 3])
                            
                            # 연승률 (1~3등 합계 / 총 출전)
                            place_rate = round(((o1 + o2 + o3) / rc_cnt * 100), 1) if rc_cnt > 0 else 0
                            stat_text = f"{rc_cnt}전 {o1}/{o2}/{o3}"
                        else:
                            stat_text = "기록 없음"
                            place_rate = 0
                    else:
                        stat_text = "성적탭 연결 오류"
                        place_rate = 0
                    
                    # 카드 내용 구성
                    st.markdown(f"### **[{row['chulNo']}번] {hr_name}**")
                    st.caption(f"ID: {hr_no}")
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("통산 전적", stat_text)
                    m2.metric("연승률", f"{place_rate}%")
                    m3.metric("부중", f"{row.get('wgBudam', '-')}kg")
                    
                    # 하단 정보 표시
                    jk = row.get('jkName', '-')
                    tr = row.get('trName', '-')
                    st.write(f"🏇 기수: {jk} | 조교사: {tr}")
    else:
        st.info("데이터가 없습니다. 지역과 날짜를 다시 확인해주세요.")
else:
    st.error("📡 구글 시트에서 데이터를 가져올 수 없습니다. SHEET_ID와 공유 설정을 확인하세요.")
