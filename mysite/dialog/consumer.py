from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from .utils.intent import predict
from .utils.FindAnswer import FindAnswer
from .utils.scrapper import Scrapper
from .apps import DialogConfig


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
        print(pred_sentence, mode)

        if mode == 0 : # 답변 주고 끝
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 1 : 
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 2 : # 열람실 현황 크롤링 후 return
            return_message = "열람실 현황 크롤링" #Scrapper.get_studyroom_status()
            button_lst = []
            mode = 0
        elif mode == 3 : # 연락처 크롤링 후 return
            return_message = "연락처 크롤링" #Scrapper.get_phone_number()
            button_lst = []
            mode = 0
        
        print(return_message, mode, button_lst)
        await self.send(text_data=json.dumps({"message": return_message, "mode" : mode, "button" : button_lst}))
