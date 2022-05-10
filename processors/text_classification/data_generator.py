from typing import List

import numpy as np
import tensorflow
from fasttext import FastText
from pandas import Series

from processors.text_normalization.text_normalizer import TextNormalizer
from utils import json_load


class DataGenerator(tensorflow.keras.utils.Sequence):
    def __init__(self,
                 root_prefix: str,
                 data_source: Series,
                 labels: Series,
                 model: FastText,
                 processor: TextNormalizer,
                 batch_size: int = 32,
                 shuffle: bool = True):
        self.root_prefix = root_prefix
        self.data_source = data_source
        self.processor = processor
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.model = model

        self.on_epoch_end()

        self.labels = labels.values

    def __len__(self):
        return int(np.floor(len(self.data_source) / self.batch_size))

    def __getitem__(self, index: int):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        self.sequences = [self.get_phrase_embedding(text) for text in self.process_batch(indexes)]

        X = np.zeros((self.batch_size, self.model.get_dimension()))
        for i, sequence in enumerate(self.sequences[indexes]):
            for j, item in enumerate(sequence):
                X[i, j] = item
        y = self.labels[indexes]

        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.data_source))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def process_batch(self, indexes: List):
        data_slice = self.data_source[indexes]
        return (self.processor.process(json_load(f"{self.root_prefix}/{filename}").text) for filename in data_slice)

    def get_phrase_embedding(self, text: List[str]):
        """
        Convert a phrase to a vector by aggregating its word embeddings
        """
        vector = np.zeros([self.model.get_dimension()], dtype="float32")

        vectors_in_phrase = [self.model.get_word_vector(token) for token in text]

        if vectors_in_phrase:
            vector = np.mean(vectors_in_phrase, axis=0)

        return vector
