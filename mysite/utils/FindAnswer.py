import pandas as pd
import os

answer_file_path = "dataset/의도분류질문_test0728.xlsx"
df = pd.read_excel(answer_file_path)

print(df.iloc[170])


def FindAnswer(idx):
    return df.iloc[idx]["답변"]
