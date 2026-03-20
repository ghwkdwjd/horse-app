import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 디자인 (넓게, CSS)
st.set_page_config(page_title="마권연구소 v5.0", layout="wide")

st.markdown("""
    <style>
    .horse-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        background-color: white;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .horse-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .horse-name { font-size: 19px; font-weight: bold; color: #111; }
    .stats-text { font-size: 14px; color: #666; font-family: 'Malgun Gothic', sans-serif; }
    .info-table { width: 100%; border-top: 1px solid #eee; padding-top: 8px; margin-top: 8px; }
    .info-label { font-size: 11px; color: #888; text-align: center; }
    .info-value { font-size: 16px; font-weight: bold; text-align: center; color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐎 마권연구소 실시간 분석판 v5.0")
st.subheader("📍 [부산경남] - 이번주 출전마 분석")

# 2. 시트 데이터 연동 부분 (기존 코드를 활용하세요)
# 만약 gspread 등으로 가져온 pandas DataFrame이 있다면 그대로 쓰시면 됩니다.
# 여기서는 'entries'라는 DataFrame이나 리스트가 있다고 가정합니다.
# 예: entries = get_sheet_data_as_dataframe() 

# --- 안전장치: 데이터가 없을 때를 대비한 샘플 (실제 데이터로 교체 필수!) ---
if 'entries' not in locals():
    st.error("❌ 시트 데이터를 불러오지 못했습니다. 연동 코드를 확인해주세요.")
    # 임시 확인용 데이터 (실제 실행 시엔 이 블록을 지우거나 무시하세요)
    entries = pd.DataFrame([
        {"no": 1, "horseName": "억새", "totalRun": 12, "firstPlace": 1, "secondPlace": 2, "thirdPlace": 3, "weight": "52.0", "jockeyName": "남정혁"},
        {"no": 10, "horseName": "달빛위에", "totalRun": 8, "firstPlace": 0, "secondPlace": 1, "thirdPlace": 2, "weight": "53.0", "jockeyName": "손경민"},
        {"no": 11, "horseName": "경복포르토스", "totalRun": 15, "firstPlace": 3, "secondPlace": 1, "thirdPlace": 0, "weight": "56.5", "jockeyName": "신윤섭"},
        {"no": 12, "horseName": "새내힐", "totalRun": 5, "firstPlace": 0, "secondPlace": 0, "thirdPlace": 1, "weight": "54.5", "jockeyName": "채상현"},
    ])
# ------------------------------------------------------------------

# 3. 데이터 루프 (데이터가 있는 만큼 전체 출력)
cols = st.columns(2) # 2열로 나열

# 데이터프레임의 각 행(row)을 반복
for i, (_, row) in enumerate(entries.iterrows()):
    with cols[i % 2]: # 0, 1번 컬럼을 번갈아가며 채움
        
        # --- 통산 전적 문자열 만들기 (안전하게 처리) ---
        total = row.get('totalRun', 0)
        f = row.get('firstPlace', 0)
        s = row.get('secondPlace', 0)
        t = row.get('thirdPlace', 0)
        stats_str = f"{total}전 {f}/{s}/{t}"
        
        # --- 연 승률 계산 (1~3위 입상 / 총 출전) ---
        win_rate = "0%"
        if total > 0:
            rate = ((f + s + t) / total) * 100
            win_rate = f"{rate:.1f}%"

        # --- 경마지 스타일 HTML 출력 (실제 마명과 데이터 사용) ---
        st.markdown(f"""
            <div class="horse-card">
                <div class="horse-header">
                    <span class="horse-name">[{row.get('no', i+1)}] {row.get('horseName', '이름없음')}</span>
                </div>
                <div class="stats-text">통산전적: {stats_str}</div>
                <table class="info-table">
                    <tr>
                        <td class="info-label">연승률(%)</td>
                        <td class="info-label">부중(kg)</td>
                        <td class="info-label">기수</td>
                    </tr>
                    <tr>
                        <td class="info-value">{win_rate}</td>
                        <td class="info-value">{row.get('weight', '-')}</td>
                        <td class="info-value" style="color:#333; font-size:14px;">{row.get('jockeyName', '-')}</td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
