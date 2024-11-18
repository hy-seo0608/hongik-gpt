import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import pandas as pd
from tqdm import tqdm
from kobert_tokenizer import KoBERTTokenizer
from transformers import BertTokenizer, BertModel
import numpy as np
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt
import csv
from numpy.linalg import norm
from numpy import dot
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configure import ANSWER_FILE_PATH

# from ..apps import DialogConfig


model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
df = pd.read_excel(ANSWER_FILE_PATH)
sentences = [df.iloc[i, 1] for i in range(len(df))]
embedding_vectors = [model.encode(sentence) for sentence in sentences]


def predict(sentence):
    encoded_sentence = model.encode(sentence)
    encoded_sentence = torch.tensor(encoded_sentence)

    cos_sim = util.cos_sim(encoded_sentence, embedding_vectors)

    best_sim_idx = int(np.argmax(cos_sim))
    cos_max = cos_sim[0, best_sim_idx].item()  # 최댓값을 float로 변환
    pred_sentence = df.iloc[best_sim_idx, 1]

    return best_sim_idx, pred_sentence, float(cos_max)


# 메인 실행
if __name__ == "__main__":
    output_file = "predictions.txt"  # 결과를 저장할 텍스트 파일
    with open(output_file, "a", encoding="utf-8") as file:  # 파일을 열기 (append 모드)
        while True:
            s = input("입력: ")
            if s.lower() == "exit":  # 종료 조건
                print("프로그램 종료.")
                break

            idx, sen, cos = predict(s)
            print(f"Index: {idx}, Sentence: {sen}, Cosine Similarity: {cos:.4f}")

            # 결과를 텍스트 파일에 저장
            file.write(f"Input: {s}\t")
            file.write(f"Index: {idx}, Sentence: {sen}, Cosine Similarity: {cos:.4f}\t\n")
            file.write("-" * 50 + "\n")  # 구분선 추가
