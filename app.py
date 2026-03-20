import streamlit as st

# 1. 디자인 (CSS) - 기존 메뉴와 레이아웃을 경마지 스타일로 변신
st.markdown("""
    <style>
    .horse-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: #ffffff;
        margin-bottom: 12px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .horse-name { font-size: 22px; font-weight: bold; color: #1a1a1a; margin-bottom: 5px; }
    .stats-line { font-size: 15px; color: #555; margin-bottom: 10px; font-weight: 500; }
    .info-grid { display: flex; justify-content: space-around; border-top: 1px solid #eee; padding-top: 10px; }
    .info-item { text-align: center; }
    .info-label { font-size: 12px; color: #888; margin-bottom: 2px; }
    .info-val { font-size: 17px; font-weight: bold; color: #d32f2f; }
    .jockey-text { font-size: 13px; color: #777; margin-top: 8px; border-top: 1px dashed #eee; padding-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 출력 로직
# 'entries' 변수에 이미 시트 데이터가 들어있다고 가정합니다.
if 'entries' in locals() and not entries.empty:
    cols = st.columns(2) # 경마책처럼 2열로 나열
    
    for i, (_, row) in enumerate(entries.iterrows()):
        with cols[i % 2]:
            # 통산 전적 계산/추출
            total = row.get('totalRun', 0)
            f = row.get('firstPlace', 0)
            s = row.get('secondPlace', 0)
            t = row.get('thirdPlace', 0)
            
            # 연승률 계산
            rate = ((f + s + t) / total * 100) if total > 0 else 0
            
            # 카드 렌더링
            st.markdown(f"""
                <div class="horse-card">
                    <div class="horse-name">[{row.get('no', i+1)}] {row.get('horseName', '미등록')}</div>
                    <div class="stats-line">통산전적: {total}전 {f}/{s}/{t}</div>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">연승률</div>
                            <div class="info-val">{rate:.1f}%</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">부중</div>
                            <div class="info-val">{row.get('weight', '-')}kg</div>
                        </div>
                    </div>
                    <div class="jockey-text">
                        🏇 기수: {row.get('jockeyName', '-')} | 조교사: {row.get('trainerName', '-')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("⚠️ 현재 시트에서 불러온 출전마 데이터가 없습니다. 시트 연동 함수를 먼저 실행해 주세요.")
