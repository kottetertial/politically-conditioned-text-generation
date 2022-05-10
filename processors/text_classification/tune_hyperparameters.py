import os
from datetime import datetime
from multiprocessing import Process

import fasttext
import numpy as np
from sklearn.model_selection import ParameterGrid

model_params = {
    "n_samples": [5000, 10000, 20000],
    "processed": [False, True],
    "epoch": [5, 15, 25],
    "lr": [0.5, 1.0],
    "wordNgrams": [3, 5],
    "loss": ["softmax", "hs"]
}

model_grid = np.array_split(list(ParameterGrid(model_params)), 4)


def grid_search(grid):
    for config in grid:
        logs = []

        n_samples = config.get("n_samples")
        epoch = config.get("epoch")
        loss = config.get("loss")
        lr = config.get("lr")
        processed = config.get("processed")
        wordNgrams = config.get("wordNgrams")

        config_str = f"{n_samples // 1000}k_{epoch}_epochs_{loss}_loss_{lr}_lr_{'processed' if processed else 'raw'}_{wordNgrams}_ngrams"
        train_file_name = f"{n_samples // 1000}k_{'processed' if processed else 'raw'}.train"
        test_file_name = f"{n_samples // 1000}k_{'processed' if processed else 'raw'}.test"
        logs_file_name = f"{config_str}.log"

        start_tr = datetime.now()
        logs.append(f"Started training at: {start_tr}\n")

        model = fasttext.train_supervised(input=train_file_name, epoch=epoch, lr=lr, wordNgrams=wordNgrams, loss=loss, verbose=0)

        end_tr = datetime.now()
        logs.append(f"Finished training at: {end_tr}\n")

        logs.append(f"Total time spent: {end_tr - start_tr}\n")

        logs.append(f"Config: {config}\n")

        result = model.test(test_file_name)
        logs.append(f"Precision: {result[1]}; Recall: {result[2]}\n")

        logs.append(f"Process id: {os.getpid()}")

        with open(logs_file_name, "w", encoding="utf-8") as target_file:
            target_file.writelines(logs)


if __name__ == '__main__':
    procs = []

    for index, grd in enumerate(model_grid):
        proc = Process(target=grid_search, args=(grd,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
