import pandas as pd
import os

answer_file_path = "dataset/answerfile.xlsx"
df = pd.read_excel(answer_file_path)

print(df.iloc[170])
print(df.columns)

def FindAnswer(idx):
    if pd.isna(df.iloc[idx]['버튼']) : 
        #if df.iloc[idx]["답변"] == '"연락처 검색"' : 
        return df.iloc[idx]["답변"], [], df.iloc[idx]["모드"]
    else :
        return df.iloc[idx]["답변"], list(df.iloc[idx]['버튼'].strip().split(',')), df.iloc[idx]["모드"]
