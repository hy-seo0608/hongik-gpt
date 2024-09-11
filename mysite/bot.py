import threading #멀티 스레드 모듈
import json

# from utils.Database import Database
from utils.Botserver import BotServer
# from utils.Preprocess import Proeprocess
# from models.intent.IntentModel import IntentModel
from utils.Intent import predict
from utils.FindAnswer import FindAnswer

# 전처리 객체 생성

# 의도 파악 모델

def to_client(conn, addr, params) :
    # db = params['db']
    try :
        # db.connect()

        read = conn.recv(2048)
        print('Connection from: %s' % str(addr))

        if read is None or not read :
            print('클라이언트 연결 오류')
            exit(0)
        
        # json data로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['question_txt']

        # 의도파악
        pred = predict(query)
        intent_name = "학식"
        button_list =  []
        # 답변 검색
        try :
            f_answer, button_list = FindAnswer(pred)
            answer = "지금은 테스트고 예측한 의도는" + str(pred) + ": " + intent_name
            answer += "\n" + f_answer
            answer_image = None
        except : 
            answer = "무슨 말인지 모르겠어요"
            answer_image = None
        
        send_json_data_str = {
            "Query" :query,
            "Answer" : answer,
            "AnswerImageUrl" : answer_image,
            "Intent" : intent_name,
            "Button" : button_list if button_list else None,
        }

        message = json.dumps(send_json_data_str)
        conn.send(message.encode())
        
    except Exception as ex :
        print("Error in to_client : ", ex)

    finally :
        # if db is not None : 
        #     db.close()
        conn.close()

if __name__ == '__main__' :
    # # DB접속
    # db = Database(
    #     host=DB_HOST, user=DB_USER, password=DB_PASSWORD,db_name = DB_NAME
    # )
    # print('DB 접속')

    # 봇 서버 동작
    port = 5050
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True :
        conn, addr = bot.ready_for_client()
        print('socket을 받았습니다')
        params = {
            # "db" : db
        }
         
        client = threading.Thread(target=to_client, args=(
            conn, # 연결 소켓
            addr,  # 연결 주소 정보
            params # 스레드 함수 파라미터
        ))
        client.start()