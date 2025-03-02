import os
import json
import requests
from datetime import datetime, timedelta, timezone

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"
LEAGUE_ID = 39
SEASON = 2024
HEADERS = {"x-apisports-key": API_KEY}

# ✅ 저장할 폴더 설정
SAVE_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ API 요청 함수 (에러 처리 포함)
def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("response", [])
    except requests.exceptions.RequestException as e:
        print(f"⚠️ [ERROR] API 요청 실패: {e}")
        return []

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

# ✅ 금일 날짜 기준 한 달간 경기 일정 가져오기
today = datetime.now(timezone.utc)
one_month_later = today + timedelta(days=30)
from_date = today.strftime("%Y-%m-%d")
to_date = one_month_later.strftime("%Y-%m-%d")

# ✅ API 요청 (경기 일정 조회)
url = f"https://v3.football.api-sports.io/fixtures?league={LEAGUE_ID}&season={SEASON}&status=NS&from={from_date}&to={to_date}"
matches = fetch_data(url)

# ✅ 날짜순 정렬
matches.sort(key=lambda x: x["fixture"]["date"])

# ✅ JSON 데이터 구조화
schedule_data = {
    "league": "Premier League",
    "season": SEASON,
    "matches": []
}

for match in matches:
    fixture = match["fixture"]
    teams = match["teams"]

    # 🕒 UTC → KST 변환
    utc_time = datetime.strptime(fixture["date"], "%Y-%m-%dT%H:%M:%S%z")
    kst_time = utc_time + timedelta(hours=9)
    
    # ✅ 저장할 경기 정보 (경기장 정보 제거)
    game_info = {
        "date": kst_time.strftime("%Y-%m-%d"),
        "time": kst_time.strftime("%H:%M"),
        "home_team": TEAM_NAME_MAPPING.get(teams["home"]["name"], teams["home"]["name"]),
        "away_team": TEAM_NAME_MAPPING.get(teams["away"]["name"], teams["away"]["name"]),
        "status": fixture["status"]["long"]
    }
    schedule_data["matches"].append(game_info)

# ✅ JSON 파일로 저장
json_path = os.path.join(SAVE_DIR, "epl_schedule.json")
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(schedule_data, file, indent=4, ensure_ascii=False)

print(f"✅ 경기 일정 데이터 저장 완료: {json_path}")
