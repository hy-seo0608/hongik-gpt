from apscheduler.schedulers.background import BackgroundScheduler
import schedule
import time
from utils import updatefile
from utils import renew
from utils import FindAnswer
import os
from configure import ANSWER_FILE_PATH, ANSWER_TEMPLATE_FILE_PATH, RENEW_FILE_PATH


def job():
    run_updatefile()
    run_renew()
    FindAnswer.renew_df()
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


def main():
    job()
    sched = BackgroundScheduler()
    sched.add_job(job, "interval", minutes=1, id="test")
    sched.start()
