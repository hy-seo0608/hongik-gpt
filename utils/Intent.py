import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import pandas as pd
from tqdm import tqdm
from kobert_tokenizer import KoBERTTokenizer
from transformers import BertTokenizer, BertModel
import numpy as np
from sentence_transformers import SentenceTransformer,util
import matplotlib.pyplot as plt
import csv
from numpy.linalg import norm
from numpy import dot

device="cuda" if torch.cuda.is_available() else "cpu"

intent_to_num={"학식":0,"편의시설":1,"연락처":2,"학사일정":3,"공지사항":4,"학교 날씨":5,"학교 정보":6,"졸업 요건":7,"도서관, 열람실":8}
num_to_intent={value:key for key,value in intent_to_num.items()}
print(num_to_intent)

df = pd.read_excel("dataset/의도분류질문_test0728.xlsx")
print(df.head())

sentences=[df.iloc[i,1] for i in range(len(df))]
sentences_class=[intent_to_num[df.iloc[i,0]] for i in range(len(df))]
print(sentences_class)

# KoBERT 모델 및 토크나이저 로드
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

embedding_vectors=[model.encode(sentence) for sentence in sentences]
embedding_vectors=torch.tensor(np.array(embedding_vectors))

def predict(sentence):
    encoded_sentence=model.encode(sentence)
    encoded_sentence=torch.tensor(encoded_sentence)
    cos_sim=util.cos_sim(encoded_sentence,embedding_vectors)
    best_sim_idx=int(np.argmax(cos_sim))
    selected_question=sentences[best_sim_idx]
    if float(cos_sim.max()) < 0.45 :
        print(f"원래 문장 : {sentence}")
        print(f"가장 높은 코사인 유사도 idx: {int(np.argmax(cos_sim))}")
        print(f"선택된 질문 : {selected_question}")
        print(f"선태괸 질문과의 유사도 : {float(cos_sim.max())}")

    return best_sim_idx

s = "학교 교가는 뭐야?"
print(predict(s))

s = "전화번호가 궁금해?"
print(predict(s))