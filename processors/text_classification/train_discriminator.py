import csv
import sys

import pandas as pd

from constants import Env, TargetPath
from processors.exploratory_analysis.analysis_constants import Party
from processors.text_classification.PPLM.run_pplm_discrim_train import train_discriminator
from utils import json_load

max_int = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)


dataframe = pd.read_csv(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/meta_exploratory.csv")

data_sampled = pd.concat(objs=[dataframe[dataframe["party"] == Party.LIBERAL].sample(n=10000, random_state=42),
                               dataframe[dataframe["party"] == Party.CONSERVATIVE].sample(n=10000, random_state=42)])[
    ["party", "file_ref"]]

with open("datasetb.tsv", "wb") as target_file:
    for label, file_ref in zip(data_sampled.party.values, data_sampled.file_ref.values):
        text = json_load(f"{Env.ROOT_PREFIX}/{TargetPath.DATA}/{TargetPath.DOCUMENTS}/{file_ref}").text.replace("\n",
                                                                                                                " ")
        target_file.write(f"{label}\t{text}\n".encode("cp1251", errors="ignore"))

args = {
    "dataset": "generic",
    "dataset_fp": "datasetb.tsv"
}

train_discriminator(**args)
