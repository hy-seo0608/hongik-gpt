from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from .utils.intent import predict
from .utils.FindAnswer import FindAnswer
from .utils.scrapper import Scrapper
from .apps import DialogConfig
import time
import numpy as np

THRESHOLD = 0.6

# HTML 테이블 생성 함수
def generate_html_table(data):
    html = "<table border='1' cellpadding='5' cellspacing='0'>\n"
    # 첫 번째 줄 (헤더)
    html += "  <tr>\n"
    for header in data[0].values():
        html += f"    <th>{header}</th>\n"
    html += "  </tr>\n"

    # 데이터 행
    for row in data[1:]:
        html += "  <tr>\n"
        for value in row.values():
            html += f"    <td>{value}</td>\n"
        html += "  </tr>\n"

    html += "</table>\n"
    return html


class DialogConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        mode = int(text_data_json["mode"])

        pred, pred_sentence, cos_sim = predict(message)
        print(message, pred_sentence, mode, cos_sim)

        if mode == 0 and cos_sim < THRESHOLD :
            await  self.send(text_data=json.dumps({"message": "무슨 말인지 모르겠어요", "mode": 0, "button": []}))
            return 
        
        if mode == 0:  # 답변 주고 끝
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 1:
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 2:  # 열람실 현황 크롤링 후 return
            return_message = ""
            status_list = []
            if "학관 열람실" in message:
                status_list = Scrapper().get_studyroom_status(mode=0)
            elif "T동 열람실" in message:
                print("여기는 실행됨")
                status_list = Scrapper().get_studyroom_status(mode=1)
            elif "R동 열람실" in message:
                status_list = Scrapper().get_studyroom_status(mode=2)

            if status_list:
                return_message = generate_html_table(status_list)
            else:
                return_message = "열람실 정보를 찾을 수 없습니다."
            button_lst = []
            mode = 0
        elif mode == 3:  # 연락처 크롤링 후 return
            d1 = Scrapper().get_phone_number(message, 0)  # Office
            d2 = Scrapper().get_phone_number(message, 1)  # person

            if d1:
                return_message = f"{d1['name']} 연락처 입니다.\n\n전화번호 :{d1['phone_num']}"
            elif d2:
                return_message = f"{d2['name']}님의 연락처 입니다.\n\n전화번호 :{d2['phone_num']}"
            else:
                return_message = "연락처를 찾을 수 없습니다."
            button_lst = []
            mode = 0

        print(return_message, mode, button_lst)
        await self.send(text_data=json.dumps({"message": return_message, "mode": int(mode), "button": button_lst}))
