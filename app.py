from flask import Flask, render_template
import json

app = Flask(__name__)

# 1. 시트에서 가져온 통산전적 데이터를 딕셔너리로 변환하는 함수
def get_processed_stats(historical_data):
    stats_map = {}
    for row in historical_data:
        # 시트 구조에 따라 인덱스(D열=3 등)는 직접 확인 필요
        try:
            name = row[3].strip() # 마명
            total = row[5] # 총 출전
            f = row[6]     # 1위
            s = row[7]     # 2위
            t = row[8]     # 3위
            stats_map[name] = f"{total}전 {f}/{s}/{t}"
        except (IndexError, AttributeError):
            continue
    return stats_map

@app.route('/')
def index():
    # 2. 오늘자 출전표 데이터 (DB나 파일에서 가져온다고 가정)
    # 실제 마권연구소 출전표 리스트 가져오는 로직을 여기에 넣으세요.
    today_entries = [
        {"horse_name": "억새", "weight": "52.0kg"},
        {"horse_name": "달빛위에", "weight": "53.0kg"},
        {"horse_name": "경복포르토스", "weight": "56.5kg"},
        {"horse_name": "새내힐", "weight": "54.5kg"}
    ]

    # 3. 시트 데이터 로드 (실제 시트 연동 함수 호출)
    # raw_sheet_data = get_sheet_data() 
    raw_sheet_data = [] # 예시를 위해 빈 리스트
    stats_dict = get_processed_stats(raw_sheet_data)

    # 4. 데이터 매칭 (화면 날림 방지용 안전 장치)
    for entry in today_entries:
        name = entry['horse_name']
        # 시트에 정보가 없으면 "기록 없음"을 강제로 넣어줌
        entry['career_summary'] = stats_dict.get(name, "기록 없음")
        # 연승률도 계산 로직 없으면 일단 0%로 고정
        if 'winning_rate' not in entry:
            entry['winning_rate'] = "0%"

    return render_template('index.html', entries=today_entries)

if __name__ == '__main__':
    app.run(debug=True)
