import requests
import urllib.parse
import base64
import json

def decode_url_values(data):
    """
    JSON 데이터의 모든 URL 인코딩된 문자열 값을 디코딩하는 함수
    """
    if isinstance(data, dict):
        return {key: decode_url_values(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode_url_values(item) for item in data]
    elif isinstance(data, str):
        return urllib.parse.unquote(data)
    else:
        return data


def fetch_and_save_json(api_url, output_file="output.json", headers=None):
    """
    API 요청을 보내고 URL 인코딩된 데이터를 디코딩하여 JSON 파일로 저장하는 함수

    Parameters:
    - api_url (str): 요청할 API URL
    - output_file (str): 저장할 JSON 파일명 (기본값: output.json)
    - headers (dict): 추가할 요청 헤더 정보 (기본값: None)
    """
    # 기본 User-Agent 헤더 설정
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 사용자 정의 헤더를 기본 헤더에 병합
    if headers:
        default_headers.update(headers)

    try:
        # GET 요청
        response = requests.get(api_url, headers=default_headers)
        response.raise_for_status()

        # JSON 데이터 파싱 및 디코딩
        data = response.json()
        decoded_data = decode_url_values(data)

        # JSON 파일로 저장
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(decoded_data, f, ensure_ascii=False, indent=4)

        print(f"디코딩된 데이터가 '{output_file}' 파일로 저장되었습니다.")

    except requests.exceptions.RequestException as e:
        print("API 요청 실패:", e)


# 예제 호출
custom_headers = {"ID": 0}
fetch_and_save_json("https://napi.hongik.ac.kr/homepage/get_food_list.php", "food_data.json")
fetch_and_save_json("https://napi.hongik.ac.kr//schedule/get_schedule.php", "schedule_data.json")
# fetch_and_save_json("https://napi.hongik.ac.kr/homepage/cnet_notice.php", "notice_data.json", custom_headers)
