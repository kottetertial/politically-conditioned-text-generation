import os
from typing import Dict, Any, Optional, List

import jsonpickle
import pandas as pd
from pandas import Series, DataFrame

from processors.exploratory_analysis.analysis_constants import Field, Keywords, Party, Type


def convert_to_dict(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        content: Any = jsonpickle.decode(file.read())
        return content.__dict__


def generate_dataset_item(path: str, filename: str) -> Optional[Dict[str, Any]]:
    object_dict: Dict[str, Any] = convert_to_dict(path)
    if not object_dict.get(Field.TEXT):
        return

    object_dict.pop(Field.TEXT)
    object_dict[Field.FILE_REF] = filename
    return object_dict


def generate_dataset(directory: str) -> List[Dict[str, Any]]:
    dataset: List[Dict[str, Any]] = []
    list_of_files: List[str] = os.listdir(directory)
    for file in list_of_files:
        dataset_item: Optional[Dict[str, Any]] = generate_dataset_item(f"{directory}/{file}", file)
        if dataset_item:
            dataset.append(dataset_item)
    return dataset


def process_party(party: str) -> Optional[str]:
    liberal: bool = False
    conservative: bool = False

    if any(keyword.lower() in party.lower() for keyword in Keywords.LIBERAL):
        liberal = True
    if any(keyword.lower() in party.lower() for keyword in Keywords.CONSERVATIVE):
        conservative = True

    if not liberal ^ conservative:
        return None

    if liberal:
        return Party.LIBERAL
    else:
        return Party.CONSERVATIVE


def extend_list(lst: List[Any], container: List[Any]) -> None:
    container.extend(lst)


def process_categories(categories: List[str]) -> Optional[str]:
    if not categories:
        return

    spoken: bool = False
    written: bool = False

    for category in categories:
        category = category.lower()
        if any(keyword.lower() in category for keyword in Keywords.SPOKEN):
            spoken = True
        if any(keyword.lower() in category for keyword in Keywords.WRITTEN):
            written = True

    if not spoken ^ written:
        return Type.AMBIGUOUS

    if spoken:
        return Type.SPOKEN
    else:
        return Type.WRITTEN


def get_frequency_stats(series: Series) -> DataFrame:
    absolute: Series = Series(series.value_counts(), name="Absolute")
    normalized: Series = Series(series.value_counts(normalize=True), name="Normalized")
    return pd.concat([absolute, normalized], axis=1)
