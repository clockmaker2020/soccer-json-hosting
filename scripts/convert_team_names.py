import json
import os

# ✅ JSON 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_JSON_PATH = os.path.join(BASE_DIR, "data/epl_schedule.json")
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, "data/epl_schedule_ko.json")

# ✅ 영어 팀명을 한국어로 변환하는 매핑
TEAM_NAME_MAPPING = {
    "Liverpool": "리버풀",
    "Arsenal": "아스널",
    "Nottingham Forest": "노팅엄 포레스트",
    "Manchester City": "맨 시티",
    "Chelsea": "첼시",
    "Newcastle": "뉴캐슬",
    "Bournemouth": "본머스",
    "Brighton": "브라이턴",
    "Fulham": "풀럼",
    "Aston Villa": "애스턴 빌라",
    "Brentford": "브렌트퍼드",
    "Crystal Palace": "크리스털 팰리스",
    "Tottenham": "토트넘",
    "Manchester United": "맨유",
    "West Ham": "웨스트 햄",
    "Everton": "에버턴",
    "Wolves": "울브스",
    "Ipswich": "입스위치",
    "Leicester City": "레스터 시티",
    "Southampton": "사우샘프턴"
}

def convert_team_names():
    """JSON 데이터를 읽고 팀명을 한국어로 변환하여 새로운 JSON 파일로 저장"""
    try:
        # ✅ JSON 파일 로드
        with open(INPUT_JSON_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        # ✅ JSON 데이터의 팀명을 한국어로 변환
        for match in data.get("matches", []):
            match["home_team"] = TEAM_NAME_MAPPING.get(match["home_team"], match["home_team"])
            match["away_team"] = TEAM_NAME_MAPPING.get(match["away_team"], match["away_team"])

        # ✅ 변환된 JSON 저장
        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"✅ 변환 완료! '{OUTPUT_JSON_PATH}'에 저장되었습니다.")

    except Exception as e:
        print(f"❌ 변환 중 오류 발생: {e}")

if __name__ == "__main__":
    convert_team_names()
