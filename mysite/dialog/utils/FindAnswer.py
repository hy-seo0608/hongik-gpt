import pandas as pd
import os
import schedule


answer_file_path = "/dataset/answerfile.xlsx"
renew_file_path = "../../dataset/answerfile.xlsx"
df = pd.read_excel(answer_file_path)

def renew_df() :
    global df
    df = pd.read_excel(renew_file_path)
    print(df.iloc[0]['답변'])

def FindAnswer(idx):
    if pd.isna(df.iloc[idx]['버튼']) : 
        #if df.iloc[idx]["답변"] == '"연락처 검색"' : 
        return df.iloc[idx]["답변"], [], df.iloc[idx]["모드"]
    else :
        return df.iloc[idx]["답변"], list(df.iloc[idx]['버튼'].strip().split(',')), df.iloc[idx]["모드"]
