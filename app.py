def get_career_stats(entries, historical_data):
    """
    entries: 오늘자 출전표 리스트 (마명 포함)
    historical_data: 구글 시트 등에서 가져온 전체 말 전적 데이터
    """
    # 1. 전적 데이터를 마명(horse_name) 키로 딕셔너리화 (속도 최적화)
    stats_map = {}
    for data in historical_data:
        name = data.get('horseName') # 시트의 마명 컬럼명 확인 필요
        if name:
            # 예: "15전 2/3/1" 형태의 데이터를 만들기 위해 필요한 값들
            total = data.get('totalRun', 0) # 총 출전수
            first = data.get('firstPlace', 0) # 1위
            second = data.get('secondPlace', 0) # 2위
            third = data.get('thirdPlace', 0) # 3위
            
            stats_map[name] = f"{total}전 {first}/{second}/{third}"

    # 2. 출전표를 돌면서 전적 문자열 추가
    for entry in entries:
        horse = entry['horse_name']
        # 시트에서 찾은 전적이 있으면 넣고, 없으면 신마(0전 0/0/0) 처리
        entry['career_summary'] = stats_map.get(horse, "0전 0/0/0")

    return entries

# --- 사용 예시 ---
# entries = [{'horse_name': '억새', 'race_no': 1}, {'horse_name': '달빛위에', 'race_no': 1}]
# updated_entries = get_career_stats(entries, sheet_data)

# 이제 프론트엔드(HTML)에서는 아래처럼 출력하면 됩니다:
# <div>{{ horse_name }}</div>
# <div style="font-size: 0.8em; color: gray;">{{ career_summary }}</div>
