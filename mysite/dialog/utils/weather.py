import requests
import openpyxl
from datetime import datetime, timedelta

# OpenWeatherMap API 설정
API_KEY = "03b02b66a1b1128a7e13960350177355"
CITY = "Mapo-gu"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&lang=kr&units=metric"

def get_weather(date):
    # API 호출
    response = requests.get(URL)
    data = response.json()

    if response.status_code == 200:
        tomorrow = date
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        
        temps = []
        min_temps = []
        max_temps = []
        weather_descriptions = []

        for forecast in data["list"]:
            forecast_time = forecast["dt_txt"]
            if tomorrow_str in forecast_time:  # 내일 날짜에 해당하는 데이터만 추출
                temps.append(forecast["main"]["temp"])
                min_temps.append(forecast["main"]["temp_min"])
                max_temps.append(forecast["main"]["temp_max"])
                weather_descriptions.append(forecast["weather"][0]["description"])

        if temps:
            avg_temp = sum(temps) / len(temps)
            min_temp = min(min_temps)
            max_temp = max(max_temps)
            weather = max(set(weather_descriptions), key=weather_descriptions.count)  # 가장 많이 나온 날씨

            return {
                "온도": round(avg_temp, 2),
                "날씨": weather,
                "최저온도": round(min_temp, 2),
                "최고온도": round(max_temp, 2),
                "미세먼지 농도": "정보 없음"  # 미세먼지 정보는 따로 제공하지 않음
            }
        else:
            print("내일 날씨 정보를 찾을 수 없습니다.")
            return None
    else:
        print("Error fetching weather data:", data.get("message", "Unknown error"))
        return None

def save_to_excel(weather_data, date):
    # 엑셀 파일 생성 또는 열기
    try:
        workbook = openpyxl.load_workbook("weather_data.xlsx")
        sheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # 첫 번째 행에 제목 삽입
        sheet.append(["날짜", "온도", "날씨", "최저온도", "최고온도", "미세먼지 농도"])

    # 내일 날짜
    tomorrow = date.strftime("%Y-%m-%d")

    # 엑셀 파일에 날씨 데이터 저장
    sheet.append([
        tomorrow,
        weather_data["온도"],
        weather_data["날씨"],
        weather_data["최저온도"],
        weather_data["최고온도"],
        weather_data["미세먼지 농도"]
    ])

    # 엑셀 파일 저장
    workbook.save("weather_data.xlsx")
    print("Weather data saved to weather_data.xlsx")

# 메인 함수
if __name__ == "__main__":
    weather_data = get_weather(datetime.now())
    if weather_data:
        save_to_excel(weather_data, datetime.now())