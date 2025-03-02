import json
import requests

# ✅ API 요청 (EPL 경기 일정 데이터 가져오기)
API_URL = "https://api-football.com/epl_schedule"

try:
    response = requests.get(API_URL, timeout=10)  # 10초 제한
    response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

    # ✅ 응답 검증: JSON 데이터 확인
    if response.text.strip() == "":
        raise ValueError("❌ API 응답이 비어 있습니다.")

    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError("❌ API 응답이 JSON 형식이 아닙니다.")

except requests.exceptions.RequestException as e:
    raise SystemExit(f"❌ API 요청 실패: {e}")

# ✅ 영어 팀명을 한국어로 변환하는 매핑
TEAM_NAME_MAPPING = {
    "Nottingham Forest": "노팅엄 포레스트",
    "Manchester City": "맨 시티",
    "Liverpool": "리버풀",
    "Southampton": "사우샘프턴",
    "Brighton": "브라이턴",
    "Fulham": "풀럼",
    "Crystal Palace": "크리스털 팰리스",
    "Ipswich": "입스위치",
    "Brentford": "브렌트퍼드",
    "Aston Villa": "애스턴 빌라",
    "Wolves": "울브스",
    "Everton": "에버턴",
    "Tottenham": "토트넘",
    "Bournemouth": "본머스",
    "Chelsea": "첼시",
    "Leicester": "레스터 시티",
    "Manchester United": "맨유",
    "Arsenal": "아스널",
    "West Ham": "웨스트 햄",
    "Newcastle": "뉴캐슬"
}

# ✅ JSON 데이터에서 팀명을 변환
for match in data.get("matches", []):
    match["home_team"] = TEAM_NAME_MAPPING.get(match["home_team"], match["home_team"])
    match["away_team"] = TEAM_NAME_MAPPING.get(match["away_team"], match["away_team"])

# ✅ 변환된 JSON을 저장
OUTPUT_JSON_PATH = "data/epl_schedule.json"
with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"✅ 변환 완료! '{OUTPUT_JSON_PATH}'에 저장되었습니다.")
