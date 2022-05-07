import re
from typing import Iterable, Any

import jsonpickle

from constants import Symbol


def generate_full_path(*args: Iterable[str]) -> str:
    return Symbol.SEP.join(args)


def generate_filename(items: Iterable[str], sep: str = " ", fformat: str = "json") -> str:
    string_items: Iterable[str] = map(str, items)
    return f"{preprocess_filename(sep.join(string_items))}.{fformat}"


# TODO: fix regex warnings
def preprocess_filename(filename: str) -> str:
    return re.sub("[<>:\"\/\\\|?*]", "", filename)[:128]


def json_dump(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(jsonpickle.encode(obj))


def json_load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as file:
        object_string: str = file.read()
        return jsonpickle.decode(object_string)
