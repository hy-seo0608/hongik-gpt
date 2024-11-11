import schedule
import time
import updatefile
import renew

renewfile_path = '../../dataset/renew.xlsx'
std_excel_file_path = '../../dataset/answerfile_template.xlsx'         # 원본 엑셀 파일 경로
renew_excel_file_path = '../../dataset/renew.xlsx'         # 크롤링 후 갱신하는 파일 경로
new_file_path = '../../dataset/answerfile.xlsx'       # 새롭게 저장할 엑셀 파일 경로

# 정해진 시간마다 실행할 함수 정의
def run_updatefile():
    print("Running updatefile tasks...")
    updatefile.update_date(renewfile_path)
    updatefile.update_food_list(renewfile_path)
    updatefile.update_notice(renewfile_path)
    updatefile.update_weather(renewfile_path)

def run_renew():
    print("Running renew tasks...")
    renew.replace_marker_and_save_new_file(std_excel_file_path, renew_excel_file_path, new_file_path)

# 스케줄 설정: 2시간마다 실행
# schedule.every(2).hours.do(run_updatefile)  # 2시간마다 updatefile 작업 실행
# schedule.every(2).hours.do(run_renew)       # 2시간마다 renew 작업 실행

# 1분마다 실행 테스트
schedule.every(1).minutes.do(run_updatefile)
schedule.every(1).minutes.do(run_renew)

# 스케줄을 계속 실행시키기 위한 루프
while True:
    schedule.run_pending()
    time.sleep(1)  # 1초마다 스케줄을 확인