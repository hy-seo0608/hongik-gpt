import pandas as pd
import os

answer_file_path = "./dataset/의도분류질문_test0728.xlsx"
df = pd.read_excel(answer_file_path)

print(df.iloc[170])

def FindAnswer(idx) :
    if pd.isna(df.iloc[idx]['버튼']):
        return df.iloc[idx]['답변'], []
    else : 
        return df.iloc[idx]['답변'], list(df.iloc[idx]['버튼'].split(','))