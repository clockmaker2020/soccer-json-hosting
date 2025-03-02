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

# ✅ 팀명 한글 변환 매핑
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

# ✅ 팀별 순위 가져오기
standings_url = f"https://v3.football.api-sports.io/standings?league={LEAGUE_ID}&season={SEASON}"
standings_data = fetch_data(standings_url)

# ✅ 순위 정보를 저장할 딕셔너리
team_rankings = {}

if standings_data:
    for league in standings_data:
        for team_info in league["league"]["standings"][0]:  # 1위부터 마지막 팀까지
            team_name = team_info["team"]["name"]
            rank = team_info["rank"]
            team_rankings[team_name] = rank

# ✅ 금일 날짜 기준 한 달간 경기 일정 가져오기
today = datetime.now(timezone.utc)
one_month_later = today + timedelta(days=30)
from_date = today.strftime("%Y-%m-%d")
to_date = one_month_later.strftime("%Y-%m-%d")

# ✅ 경기 일정 데이터 가져오기
fixtures_url = f"https://v3.football.api-sports.io/fixtures?league={LEAGUE_ID}&season={SEASON}&status=NS&from={from_date}&to={to_date}"
matches = fetch_data(fixtures_url)

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
    
    # ✅ 홈팀 및 원정팀 이름 변환
    home_team_eng = teams["home"]["name"]
    away_team_eng = teams["away"]["name"]
    
    home_team_kor = TEAM_NAME_MAPPING.get(home_team_eng, home_team_eng)
    away_team_kor = TEAM_NAME_MAPPING.get(away_team_eng, away_team_eng)

    # ✅ 팀 순위 정보 추가
    home_team_rank = team_rankings.get(home_team, "Unknown")
    away_team_rank = team_rankings.get(away_team, "Unknown")

    # ✅ 저장할 경기 정보 (경기장 정보 제거)
    game_info = {
        "date": kst_time.strftime("%Y-%m-%d"),
        "time": kst_time.strftime("%H:%M"),
        "home_team": home_team_kor,
        "away_team": away_team_kor,
        "home_team_rank": home_team_rank,
        "away_team_rank": away_team_rank,
        "status": fixture["status"]["long"]
    }
    schedule_data["matches"].append(game_info)

# ✅ JSON 파일로 저장
json_path = os.path.join(SAVE_DIR, "epl_schedule.json")
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(schedule_data, file, indent=4, ensure_ascii=False)

print(f"✅ 경기 일정 데이터 저장 완료: {json_path}")
