from datetime import datetime

import pandas as pd
import spacy
from transformers import GPT2Tokenizer

from constants import Env, TargetPath
from utils import json_load


n = 511
nlp = spacy.load("en_core_web_sm", exclude=['tok2vec', 'parser', 'ner'])
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
dataframe = pd.read_csv(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/meta_exploratory.csv")
n_items = dataframe.shape[0]
target_file = f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/dataset_{n + 1}.tsv"


start = datetime.now()
with open(target_file, "w", encoding="utf-8") as file:
    for i, item in enumerate(zip(dataframe.party.values, dataframe.file_ref.values)):
        label = item[0]
        file_ref = item[1]

        text = json_load(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/{TargetPath.DOCUMENTS}/{file_ref}").text.replace("\n",
                                                                                                                " ")
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]

        chunk = []
        chunk_len = 0

        for j, sentence in enumerate(sentences):
            encoded_sentence = tokenizer.encode(sentence)
            sentence_len = len(encoded_sentence)

            if (j + 1) < len(sentences):
                if chunk_len + sentence_len <= n:
                    chunk_len += sentence_len
                    chunk.append(sentence)
                elif sentence_len > n:
                    file.write(f"{label}\t{' '.join(chunk)}\n")
                    for k in range(0, len(encoded_sentence), n):
                        file.write(f"{label}\t{tokenizer.decode(encoded_sentence[k:k + n])}\n")
                    chunk = []
                    chunk_len = 0
                elif chunk_len + sentence_len > n:
                    file.write(f"{label}\t{' '.join(chunk)}\n")
                    chunk = [sentence]
                    chunk_len = sentence_len

            elif (j + 1) == len(sentences):
                if chunk_len + sentence_len <= n:
                    chunk.append(sentence)
                    file.write(f"{label}\t{' '.join(chunk)}\n")
                elif chunk_len + sentence_len > n:
                    file.write(f"{label}\t{' '.join(chunk)}\n")
                    for k in range(0, len(encoded_sentence), n):
                        file.write(f"{label}\t{tokenizer.decode(encoded_sentence[k:k + n])}\n")

        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1} items out of {n_items} in {datetime.now() - start}.")
