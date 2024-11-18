import schedule
import time
import updatefile
import renew
import FindAnswer
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from configure import RENEW_FILE_PATH, ANSWER_FILE_PATH, ANSWER_TEMPLATE_FILE_PATH


# 정해진 시간마다 실행할 함수 정의
def run_updatefile():
    print("Running updatefile tasks...")
    updatefile.update_date(RENEW_FILE_PATH)
    updatefile.update_food_list(RENEW_FILE_PATH)
    updatefile.update_notice(RENEW_FILE_PATH)
    updatefile.update_weather(RENEW_FILE_PATH)


def run_renew():
    print("Running renew tasks...")
    renew.replace_marker_and_save_new_file(ANSWER_TEMPLATE_FILE_PATH, RENEW_FILE_PATH, ANSWER_FILE_PATH)


# 스케줄 설정: 2시간마다 실행
# schedule.every(2).hours.do(run_updatefile)  # 2시간마다 updatefile 작업 실행
# schedule.every(2).hours.do(run_renew)       # 2시간마다 renew 작업 실행

# 1분마다 실행 테스트
schedule.every(1).minutes.do(run_updatefile)
schedule.every(1).minutes.do(run_renew)
schedule.every(1).minutes.do(FindAnswer.renew_df)
# 스케줄을 계속 실행시키기 위한 루프
while True:
    schedule.run_pending()
    time.sleep(1)  # 1초마다 스케줄을 확인
