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
from ..apps import DialogConfig


model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
df = pd.read_excel("dataset/answerfile_template.xlsx")
sentences = [df.iloc[i, 1] for i in range(len(df))]
embedding_vectors = [model.encode(sentence) for sentence in sentences]


def predict(sentence):
    encoded_sentence = model.encode(sentence)
    encoded_sentence = torch.tensor(encoded_sentence)

    cos_sim = util.cos_sim(encoded_sentence, embedding_vectors)

    best_sim_idx = int(np.argmax(cos_sim))
    pred_sentence = df.iloc[best_sim_idx, 1]

    return best_sim_idx, pred_sentence
