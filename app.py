import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="마권연구소 v5.0", layout="wide")

# 2. 디자인 (CSS)
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
    .horse-header { display: flex; justify-content: space-between; align-items: center; }
    .horse-name { font-size: 18px; font-weight: bold; color: #111; }
    .stats-text { font-size: 13px; color: #666; margin-bottom: 8px; }
    .info-table { width: 100%; border-top: 1px solid #eee; padding-top: 8px; }
    .info-label { font-size: 11px; color: #888; text-align: center; }
    .info-value { font-size: 15px; font-weight: bold; text-align: center; color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐎 마권연구소 실시간 분석판 v5.0")

# 3. 데이터 가져오기 (실제 전체 출전표 변수를 여기에 넣으세요)
# 예: all_horses = get_today_entries() 
# 일단 전체가 나오는 걸 보여드리기 위해 12마리 예시로 루프를 돌립니다.
if 'all_horses' not in locals():
    # 데이터가 없을 때를 대비한 샘플 (실제 데이터 변수로 교체 필수!)
    all_horses = [
        {"no": i+1, "name": f"경주마{i+1}", "stats": "10전 1/1/1", "rate": "10%", "weight": "54kg", "jockey": "기수"} 
        for i in range(12) # 여기서 숫자를 바꾸거나 실제 리스트를 넣으면 전체가 나옵니다.
    ]

# 4. 전체 출력 (2열 레이아웃)
cols = st.columns(2)

for i, horse in enumerate(all_horses):
    with cols[i % 2]: # 0, 1번 컬럼을 번갈아가며 채움
        st.markdown(f"""
            <div class="horse-card">
                <div class="horse-header">
                    <span class="horse-name">[{horse['no']}] {horse['name']}</span>
                    <span style="color: #007bff; font-weight: bold;">{horse.get('source', '서울')}</span>
                </div>
                <div class="stats-text">통산전적: {horse.get('stats', '0전 0/0/0')}</div>
                <table class="info-table">
                    <tr>
                        <td class="info-label">연승률</td>
                        <td class="info-label">부중</td>
                        <td class="info-label">기수</td>
                    </tr>
                    <tr>
                        <td class="info-value">{horse['rate']}</td>
                        <td class="info-value">{horse['weight']}</td>
                        <td class="info-value" style="color:#333; font-size:13px;">{horse['jockey']}</td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
