import os
import json
import requests
from datetime import datetime, timedelta

# ✅ API 설정
API_KEY = "0776a35eb1067086efe59bb7f93c6498"
LEAGUE_ID = 39  # 프리미어리그 ID
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

# ✅ 금일 날짜 기준 한 달간 경기 일정 가져오기
today = datetime.utcnow()
one_month_later = today + timedelta(days=30)
from_date = today.strftime("%Y-%m-%d")
to_date = one_month_later.strftime("%Y-%m-%d")

# ✅ 경기 일정 API 요청
matches_url = f"https://v3.football.api-sports.io/fixtures?league={LEAGUE_ID}&season={SEASON}&status=NS&from={from_date}&to={to_date}"
matches = fetch_data(matches_url)

# ✅ 팀 순위 API 요청
standings_url = f"https://v3.football.api-sports.io/standings?league={LEAGUE_ID}&season={SEASON}"
standings_data = fetch_data(standings_url)

# ✅ 팀 순위 정보 저장 (딕셔너리 형태)
team_rankings = {}
if standings_data:
    for team_info in standings_data[0]["league"]["standings"][0]:  # 1위부터 마지막 팀까지
        team_name = team_info["team"]["name"]
        team_rankings[team_name] = team_info["rank"]

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
    venue = match.get("venue", {"name": "Unknown Venue"})  # 🔹 venue 예외 처리 추가

    # 🕒 UTC → KST 변환
    utc_time = datetime.strptime(fixture["date"], "%Y-%m-%dT%H:%M:%S%z")
    kst_time = utc_time + timedelta(hours=9)
    
    # ✅ 홈팀 및 원정팀 순위 가져오기
    home_team_name = teams["home"]["name"]
    away_team_name = teams["away"]["name"]
    home_team_rank = team_rankings.get(home_team_name, "N/A")
    away_team_rank = team_rankings.get(away_team_name, "N/A")

    # ✅ 저장할 경기 정보
    game_info = {
        "date": kst_time.strftime("%Y-%m-%d"),
        "time": kst_time.strftime("%H:%M"),
        "home_team": home_team_name,
        "away_team": away_team_name,
        "home_team_rank": home_team_rank,
        "away_team_rank": away_team_rank,
        "stadium": venue.get("name", "Unknown Venue"),
        "status": fixture["status"]["long"]
    }
    schedule_data["matches"].append(game_info)

# ✅ JSON 파일로 저장
json_path = os.path.join(SAVE_DIR, "epl_schedule.json")
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(schedule_data, file, indent=4, ensure_ascii=False)

print(f"✅ 경기 일정 데이터 저장 완료: {json_path}")
