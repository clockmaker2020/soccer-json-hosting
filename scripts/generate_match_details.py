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
MATCH_DIR = os.path.join(os.getcwd(), "data", "matches")

# ✅ 1️⃣ 기존 JSON 파일 삭제
if os.path.exists(MATCH_DIR):
    for file in os.listdir(MATCH_DIR):
        if file.endswith(".json"):
            os.remove(os.path.join(MATCH_DIR, file))
    print(f"🗑️ 기존 경기 상세 JSON 파일 삭제 완료.")

# ✅ 폴더가 없으면 새로 생성
os.makedirs(MATCH_DIR, exist_ok=True)
print(f"📁 경기 상세 JSON 저장 폴더 생성 완료: {MATCH_DIR}")

# ✅ 2️⃣ API 요청 함수
def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("response", [])
    except requests.exceptions.RequestException as e:
        print(f"⚠️ [ERROR] API 요청 실패: {e}")
        return []

# ✅ 3️⃣ 오늘부터 한 달간의 경기 ID 가져오기
today = datetime.utcnow().strftime("%Y-%m-%d")
one_month_later = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")

fixture_url = f"https://v3.football.api-sports.io/fixtures?league={LEAGUE_ID}&season={SEASON}&from={today}&to={one_month_later}"
fixtures = fetch_data(fixture_url)

# ✅ 4️⃣ 개별 경기 상세 정보 가져오기 및 JSON 저장
for fixture in fixtures:
    match_id = fixture["fixture"]["id"]
    detail_url = f"https://v3.football.api-sports.io/fixtures?id={match_id}"
    match_details = fetch_data(detail_url)

    if not match_details:
        continue

    match_data = match_details[0]  # 첫 번째 응답 데이터 사용
    fixture = match_data["fixture"]
    teams = match_data["teams"]
    odds = match_data.get("odds", {})

    # 🕒 UTC → KST 변환
    utc_time = datetime.strptime(fixture["date"], "%Y-%m-%dT%H:%M:%S%z")
    kst_time = utc_time + timedelta(hours=9)

    # ✅ 저장할 경기 정보
    match_json = {
        "1. 경기 개요": {
            "경기 ID": match_id,
            "경기 날짜": kst_time.strftime("%Y-%m-%d %H:%M"),
            "경기장": fixture["venue"]["name"],
            "도시": fixture["venue"]["city"],
            "경기 상태": fixture["status"]["long"]
        },
        "2. 경기 예상 정보": {
            "배당률": {
                "홈 승리 확률": odds.get("home", "N/A"),
                "무승부 확률": odds.get("draw", "N/A"),
                "원정 승리 확률": odds.get("away", "N/A")
            }
        },
        "3. 실시간 경기 정보": {
            "현재 점수": f"{match_data['goals']['home']} - {match_data['goals']['away']}",
            "득점 기록": match_data["score"]["fulltime"]
        },
        "블로그 URL": ""
    }

    # ✅ JSON 파일 저장
    match_path = os.path.join(MATCH_DIR, f"match_{kst_time.strftime('%Y%m%d_%H%M')}.json")
    with open(match_path, "w", encoding="utf-8") as file:
        json.dump(match_json, file, indent=4, ensure_ascii=False)

    print(f"✅ 경기 상세 정보 저장 완료: {match_path}")
