import streamlit as st

# 1. 페이지 설정 (넓게 보기)
st.set_page_config(page_title="마권연구소 실시간 분석판 v5.0", layout="wide")

# 2. 스타일 시트 (경마책 느낌 내기)
st.markdown("""
    <style>
    .horse-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
    }
    .horse-name {
        font-size: 20px;
        font-weight: bold;
        color: #333;
    }
    .stats-text {
        font-size: 14px;
        color: #666;
        margin-top: -5px;
    }
    .main-info {
        font-size: 18px;
        font-weight: bold;
        color: #d32f2f;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🐎 마권연구소 실시간 분석판 v5.0")
st.subheader("📍 20260322 [부산경남] - 제 1경주")

# 3. 가짜 데이터 (여기에 나중에 시트 연동 함수를 넣으시면 됩니다)
# 실제로는 historical_data에서 가져온 전적을 매칭하는 로직이 들어갈 자리입니다.
horses = [
    {"no": 1, "name": "억새", "stats": "12전 1/2/3", "rate": "25%", "weight": "52.0kg", "jockey": "남정혁"},
    {"no": 10, "name": "달빛위에", "stats": "8전 0/1/2", "rate": "12%", "weight": "53.0kg", "jockey": "손경민"},
    {"no": 11, "name": "경복포르토스", "stats": "15전 3/1/0", "rate": "26%", "weight": "56.5kg", "jockey": "신윤섭"},
    {"no": 12, "name": "새내힐", "stats": "5전 0/0/1", "rate": "0%", "weight": "54.5kg", "jockey": "채상현"},
]

# 4. 화면 레이아웃 (2열 구성)
cols = st.columns(2)

for i, horse in enumerate(horses):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="horse-card">
                <div class="horse-name">[{horse['no']}] {horse['name']}</div>
                <div class="stats-text">통산 전적: {horse['stats']}</div>
                <hr style="margin: 10px 0;">
                <table style="width:100%">
                    <tr style="text-align: center; color: gray; font-size: 12px;">
                        <td>연승률</td>
                        <td>부중</td>
                    </tr>
                    <tr style="text-align: center;">
                        <td class="main-info">{horse['rate']}</td>
                        <td class="main-info">{horse['weight']}</td>
                    </tr>
                </table>
                <div style="font-size: 12px; color: #888; margin-top: 10px;">
                    🏇 기수: {horse['jockey']} | 조교사: 정보없음
                </div>
            </div>
        """, unsafe_allow_html=True)
