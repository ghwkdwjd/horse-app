import streamlit as st
import pandas as pd
import io
import requests

# [1] 화면 설정
st.set_page_config(page_title="마권연구소 Mobile", layout="wide")
st.title("🏇 마권연구소 모바일 분석판")

# [2] 구글 시트 정보 (전달해주신 ID 반영)
SHEET_ID = "1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk"
SHEET_NAME = "출전표" 
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=60)
def load_data():
    try:
        # 한글 에러 방지를 위해 requests로 데이터를 먼저 받아온 뒤 인코딩 지정
        response = requests.get(URL)
        response.encoding = 'utf-8' # 한글 깨짐 방지 핵심 설정
        df = pd.read_csv(io.StringIO(response.text))
        
        # 컬럼명 공백 제거
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # [3] 필터 설정 (사이드바)
    st.sidebar.header("🔍 검색 필터")
    
    # 날짜(rcDate) 확인
    if 'rcDate' in df.columns:
        df['rcDate'] = df['rcDate'].astype(str)
        dates = sorted(df['rcDate'].unique(), reverse=True)
        target_date = st.sidebar.selectbox("📅 날짜 선택", dates)
        
        day_df = df[df['rcDate'] == target_date]
        
        # 경주번호(rcNo) 확인
        if 'rcNo' in day_df.columns:
            races = sorted(day_df['rcNo'].unique())
            target_rc = st.sidebar.select_slider("🚩 경주 번호", options=races)
            
            # [4] 결과 출력
            race_data = day_df[day_df['rcNo'] == target_rc].sort_values('chulNo')
            
            st.subheader(f"📍 {target_date} - 제 {target_rc}경주")
            
            # 2열 배치
            cols = st.columns(2)
            for idx, row in race_data.reset_index().iterrows():
                with cols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"### **[{row['chulNo']}번] {row['hrName']}**")
                        
                        m1, m2, m3 = st.columns(3)
                        m1.metric("기수", str(row['jkName']))
                        m2.metric("부중", f"{row['wgBudam']}kg")
                        m3.metric("거리", f"{row['rcDist']}m")
                        
                        st.write(f"🏇 조교사: {row['trName']} | 마주: {row['ownName']}")
        else:
            st.warning("시트에 'rcNo' 컬럼이 없습니다.")
    else:
        st.warning("시트에 'rcDate' 컬럼이 없습니다.")
else:
    st.error("📡 데이터를 불러올 수 없습니다. 구글 시트 [공유] 설정이 '링크가 있는 모든 사용자-뷰어'인지 꼭 확인하세요!")

st.sidebar.markdown("---")
st.sidebar.caption("v1.6 한글 인코딩 보완판")
