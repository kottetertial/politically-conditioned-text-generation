from datetime import datetime
from datetime import datetime
from multiprocessing import Process

import numpy as np
import pandas as pd
import spacy
from sklearn.model_selection import ParameterGrid

from constants import Env, TargetPath
from processors.exploratory_analysis.analysis_constants import Party
from processors.text_normalization.text_normalizer import TextNormalizer
from utils import json_load

dataframe = pd.read_csv(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/meta_exploratory.csv")

processing_params = {
    "n_samples": [5000, 10000, 20000],
    "processed": [False, True]
}

processing_grid = np.array_split(list(ParameterGrid(processing_params)), 4)

nlp = spacy.load("en_core_web_sm", exclude=['tok2vec', 'parser', 'ner', 'senter'])
processor = TextNormalizer(nlp)


def prepare_data(grid):
    for config in grid:
        logs = []

        n_samples = config.get("n_samples")
        processed = config.get("processed")

        data_sampled = pd.concat(objs=[dataframe[dataframe["party"] == Party.LIBERAL].sample(n=n_samples, random_state=42),
                                       dataframe[dataframe["party"] == Party.CONSERVATIVE].sample(n=n_samples, random_state=42)])[["party", "file_ref"]]
        train_data = data_sampled.sample(frac=0.7, random_state=42)
        test_data = data_sampled.drop(train_data.index)

        config_str = f"{n_samples // 1000}k_{'processed' if processed else 'raw'}"
        train_file_name = f"{config_str}.train"
        test_file_name = f"{config_str}.test"
        logs_file_name = f"{config_str}.log"

        start_proc = datetime.now()
        logs.append(f"Started processing at: {start_proc}\n")

        with open(train_file_name, "w", encoding="utf-8") as target_file:
            for label, file_ref in zip(train_data.party.values, train_data.file_ref.values):
                if processed:
                    text = processor.process(json_load(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/{TargetPath.DOCUMENTS}/{file_ref}").text)
                    target_file.write(f"__label__{label} {' '.join(text)}\n")
                else:
                    text = json_load(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/{TargetPath.DOCUMENTS}/{file_ref}").text.replace("\n", " ")
                    target_file.write(f"__label__{label} {text}\n")

        with open(test_file_name, "w", encoding="utf-8") as target_file:
            for label, file_ref in zip(test_data.party.values, test_data.file_ref.values):
                if processed:
                    text = processor.process(json_load(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/{TargetPath.DOCUMENTS}/{file_ref}").text)
                    target_file.write(f"__label__{label} {' '.join(text)}\n")
                else:
                    text = json_load(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/{TargetPath.DOCUMENTS}/{file_ref}").text.replace("\n", " ")
                    target_file.write(f"__label__{label} {text}\n")

        end_proc = datetime.now()
        logs.append(f"Finished processing at: {end_proc}\n")

        logs.append(f"Total time spent: {end_proc - start_proc}\n")

        with open(logs_file_name, "w", encoding="utf-8") as target_file:
            target_file.writelines(logs)


if __name__ == '__main__':
    procs = []

    for index, grd in enumerate(processing_grid):
        proc = Process(target=prepare_data, args=(grd,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
