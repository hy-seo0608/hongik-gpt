import pandas as pd
import os
import schedule

import sys
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configure import ANSWER_FILE_PATH


df = pd.read_excel(ANSWER_FILE_PATH)


def renew_df():
    global df
    del [[df]]
    df = pd.read_excel(ANSWER_FILE_PATH)
    print(df.iloc[0]["답변"])


def FindAnswer(idx):
    global df
    print(df.iloc[0]["답변"])
    if pd.isna(df.iloc[idx]["버튼"]):
        # if df.iloc[idx]["답변"] == '"연락처 검색"' :
        return df.iloc[idx]["답변"], [], df.iloc[idx]["모드"]
    else:
        return df.iloc[idx]["답변"], list(df.iloc[idx]["버튼"].strip().split(",")), df.iloc[idx]["모드"]


if __name__ == "__main__":
    pass
