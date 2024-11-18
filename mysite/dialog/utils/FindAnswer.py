import pandas as pd
import os
import redis
import pickle

# Redis 연결
r = redis.Redis(host='localhost', port=6379, decode_responses=False)

answer_file_path = os.path.dirname(__file__) + "/../../dataset/answerfile.xlsx"
print(answer_file_path)
df = pd.read_excel(answer_file_path)

# DataFrame 직렬화 후 Redis에 저장
r.set('shared_df', pickle.dumps(df))
print("Redis에 데이터 저장 완료!")

def get_cwd() : 
    return os.getcwd()

def renew_df() :
    # Redis에서 데이터 가져오기 및 역직렬화
    df = pd.read_excel(answer_file_path)
    r.set('shared_df', pickle.dumps(df))
    print(df.iloc[0]['답변'])

def FindAnswer(idx):
    # Redis에서 데이터 가져오기 및 역직렬화
    data = r.get('shared_df')
    df = pickle.loads(data)
    if pd.isna(df.iloc[idx]['버튼']) : 
        #if df.iloc[idx]["답변"] == '"연락처 검색"' : 
        return df.iloc[idx]["답변"], [], df.iloc[idx]["모드"]
    else :
        return df.iloc[idx]["답변"], list(df.iloc[idx]['버튼'].strip().split(',')), df.iloc[idx]["모드"]
