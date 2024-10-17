from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from .utils.intent import predict
from .utils.FindAnswer import FindAnswer
from .utils.scrapper import Scrapper
from .apps import DialogConfig

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

        pred, pred_sentence = predict(message)
        print(message, pred_sentence, mode)

        if mode == 0:  # 답변 주고 끝
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 1:
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 2:  # 열람실 현황 크롤링 후 return
            return_message = "" 
            scrapper = Scrapper()
            status_list = []
            if message == "학관 열람실" : 
                status_list = scrapper.get_studyroom_status(0)
            elif message == "T동 열람실" : 
                status_list = scrapper.get_studyroom_status(1)
            elif message == "R동 열람실 " : 
                status_list = scrapper.get_studyroom_status(2)
            
            if status_list : 
                return_message = generate_html_table(status_list)
            else : 
                return_message = "열람실 정보를 찾을 수 없습니다."
            button_lst = []
            mode = 0
        elif mode == 3:  # 연락처 크롤링 후 return
            scrapper = Scrapper()
            d1 = scrapper.get_phone_number(message, 0)  # Office
            d2 = scrapper.get_phone_number(message, 1)  # person

            if d1 :
                return_message = f"{d1['name']} 연락처 입니다.\n\n전화번호 :{d1['phone_num']}"
            elif d2 : 
                return_message = f"{d2['name']}님의 연락처 입니다.\n\n전화번호 :{d2['phone_num']}"
            else : 
                return_message = "연락처를 찾을 수 없습니다."
            button_lst = []
            mode = 0

        print(return_message, mode, button_lst)
        await self.send(text_data=json.dumps({"message": return_message, "mode": mode, "button": button_lst}))
