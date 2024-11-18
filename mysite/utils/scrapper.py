from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests import get
import time
import json
from collections import OrderedDict
import re

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from configure import (
    NOTICE_URL,
    NOTICE_ADD_URL,
    NOTICE_FILE_PATH,
    PHONE_NUMBER_OFFICE_URL,
    PHONE_NUMBER_PERSON_URL,
    PHONE_NUMBER_FILE_PATH,
    STUDYROOM_URL,
)


class Scrapper:
    _instance = None
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Scrapper, cls).__new__(cls)
        return cls._instance

    def get_notice(self):

        self.browser.get(NOTICE_URL)
        self.browser.implicitly_wait(10)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")

        table = soup.find_all("table")[1]
        sub = re.compile(r"pkid=[0-9]*\^")
        data_list = []
        for notice in table.find_all("tr")[1:]:
            data = OrderedDict()
            td_list = notice.find_all("td")
            data["subject"] = td_list[1].find("span").text
            link = td_list[1].a["href"]
            link = sub.findall(link)[0][:-1]
            data["link"] = f"{NOTICE_ADD_URL}{link}"
            data["name"] = td_list[2].text
            data["date"] = td_list[4].text
            data_list.append(data)

        with open(NOTICE_FILE_PATH, "w") as f:
            json.dump(data_list, f, ensure_ascii=False, indent="\t")

    def get_phone_number(self, search_query, mode):
        ##mode 0 : office , 1 : person

        base_url = PHONE_NUMBER_OFFICE_URL if mode == 0 else PHONE_NUMBER_PERSON_URL

        if mode == 0:
            base_url = base_url + f"?mode=list&srSearchKey=name&srSearchVal={search_query}"
        else:
            base_url = base_url + f"?mode=list&srSearchKey=onename&srSearchVal={search_query}"

        self.browser.get(base_url)
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "bn-list-card")))
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        try:
            if mode == 1:
                query_result = soup.find("div", "bn-list-card faculty").ul.li
                data = OrderedDict()
                data["name"] = query_result.find("div", "b-name-box").p.text
                data["belong"] = query_result.find("p", "b-belong").text
                data["spot"] = query_result.find("p", "b-spot").text
                data["phone_num"] = query_result.find("a", {"title": "전화걸기"}).text.strip()

            else:
                data_list = []
                query_result = soup.find("div", "bn-list-card phone-search")
                for query in query_result.ul.find_all("li", recursive=False):
                    data = OrderedDict()
                    data["name"] = query.find("p").text.strip().replace(" ", "")
                    phone_num = query.find("ul", "ul-type01").li
                    data["phone_num"] = phone_num.text if phone_num is not None else "there is no phone number"
                    data_list.append(data)

            with open(PHONE_NUMBER_FILE_PATH, "w") as f:
                json.dump(data_list, f, ensure_ascii=False, indent="\t")
            return data
        except:
            return {}

    def get_studyroom_status(self, mode):
        # mode 0 : 학관, mode 1 : T동, mode 2 : R동
        """
        academy_studyroom_url = 'http://203.249.67.222/'
        T_studyroom_url = 'http://203.249.65.81/'
        R_studyroom_url = 'http://223.194.83.66/'
        """

        url_to_studyroom_num = {
            STUDYROOM_URL[0]: 4,
            STUDYROOM_URL[1]: 4,
            STUDYROOM_URL[2]: 1,
        }
        base_url = STUDYROOM_URL[mode]
        self.browser.get(base_url)
        self.browser.implicitly_wait(10)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")

        # Table 찾기
        tables = soup.find_all("table", {"cellpadding": "0", "cellspacing": "0", "border": "0", "width": "100%"})

        if tables:
            studyroom_status = []
            for table in tables:
                rows = table.find_all("tr")
                for row in rows[2:]:  # 첫 두 행은 제목 행일 가능성이 높으므로 스킵
                    cols = row.find_all("td")
                    if len(cols) == 5:  # 열의 개수가 5개인 경우
                        room_name = cols[0].text.strip()
                        total_seats = cols[1].text.strip()
                        used_seats = cols[2].text.strip()
                        remaining_seats = cols[3].text.strip()
                        utilization_rate = cols[4].text.strip()
                        studyroom_status.append(
                            {
                                "room_name": room_name,
                                "total_seats": total_seats,
                                "used_seats": used_seats,
                                "remaining_seats": remaining_seats,
                                "utilization_rate": utilization_rate,
                            }
                        )

            for status in studyroom_status:
                print(status)
            return studyroom_status
        else:
            print("No tables found.")
            return []

        # # 특정 <td> 요소 찾기
        # td_element = soup.find("td", {"id": "tbl_table", "colspan": "2"})

        # if td_element:
        #     print(td_element.prettify())
        # else:
        #     print("Element not found.")


if __name__ == "__main__":
    a = Scrapper()
    dormitory_url = "https://www.hongik.ac.kr/kr/life/seoul-cafeteria-view.do?articleNo=5414&restNo=2"
    staff_url = "https://www.hongik.ac.kr/kr/life/seoul-cafeteria-view.do?articleNo=5413&restNo=3"
    a.get_food_list()
    # print(a.get_notice())
    # d1 = a.get_phone_number("요건없을걸", 0)
    # d2 = a.get_phone_number("배성일", 1)
    # print(d1)
    # print(d2)
    # a.get_studyroom_status(0)
    # a.get_studyroom_status(1)
    # a.get_studyroom_status(2)
