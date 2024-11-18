from pathlib import Path
import os

# 프로젝트 루트 디렉토리 경로
BASE_DIR = Path(__file__).resolve().parent


# EXCEL_FILE_PATH
ANSWER_FILE_PATH = os.path.join(BASE_DIR, "dataset", "answerfile.xlsx")
ANSWER_TEMPLATE_FILE_PATH = os.path.join(BASE_DIR, "dataset", "answerfile_template.xlsx")
RENEW_FILE_PATH = os.path.join(BASE_DIR, "dataset", "renew.xlsx")


# JSON_FILE_PATH
PHONE_NUMBER_FILE_PATH = os.path.join(BASE_DIR, "dataset", "json", "phone_number.json")
NOTICE_FILE_PATH = os.path.join(BASE_DIR, "dataset", "json", "notice_list.json")
FOOD_LIST_FILE_PATH = os.path.join(BASE_DIR, "dataset", "json", "food_list.json")


# CRAWLING URL
API_FOOD_URL = "https://napi.hongik.ac.kr/homepage/get_food_list.php"
NOTICE_URL = "https://ko.hongik.ac.kr/front/boardlist.do?bbsConfigFK=54&siteGubun=1&menuGubun=1"
NOTICE_ADD_URL = "https://wwwce.hongik.ac.kr/dept/0401.html?"
PHONE_NUMBER_PERSON_URL = "https://www.hongik.ac.kr/kr/introduction/search-for-faculty.do"
PHONE_NUMBER_OFFICE_URL = "https://www.hongik.ac.kr/kr/introduction/search-phone.do"
STUDYROOM_URL = ["http://203.249.67.222/", "http://203.249.65.81/", "http://223.194.83.66/"]


# WEATHER_API
API_KEY = "03b02b66a1b1128a7e13960350177355"
CITY = "Mapo-gu"
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&lang=kr&units=metric"


if __name__ == "__main__":
    print(PHONE_NUMBER_FILE_PATH)
