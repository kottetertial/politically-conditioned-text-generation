import json
import re
from typing import Union, Callable, Any, Optional, Iterable

import jsonpickle
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from scrapers.abstract_scraper import AbstractScraper
from scrapers.constants import Misc


def auto_navigate(function: Callable) -> Callable:
    def wrapper(obj: AbstractScraper, *args: Iterable[Any]) -> Any:
        obj.start(*args)
        result = function(obj, *args)
        return result
    return wrapper


def auto_quit(function: Callable) -> Callable:
    def wrapper(obj: AbstractScraper, *args: Iterable[Any]) -> Any:
        result = function(obj, *args)
        obj.stop()
        return result
    return wrapper


def open_new_tab(function: Callable) -> Callable:
    def wrapper(obj: AbstractScraper, *args: Iterable[Any]) -> Any:
        obj.open_new_tab(*args)
        result = function(obj, *args)
        return result
    return wrapper


def close_tab(function: Callable) -> Callable:
    def wrapper(obj: AbstractScraper, *args: Iterable[Any]) -> Any:
        result = function(obj, *args)
        obj.close_tab()
        return result
    return wrapper


def element_exists(by: str, value: Any, location: Union[WebElement, WebDriver]) -> bool:
    try:
        location.find_element(by, value)
    except NoSuchElementException:
        return False
    return True


def check_exists(function: Callable) -> Callable:
    def wrapper(obj: AbstractScraper, by: str, value: Any, location: Optional[WebElement] = None) -> Optional[Any]:
        if not location:
            location = obj.driver
        if element_exists(by, value, location):
            return function(obj, by, value, location)
        return None
    return wrapper


def generate_full_path(*args: Iterable[str]) -> str:
    return Misc.SEP.join(args)


def generate_filename(items: Iterable[str], sep: str = " ", fformat: str = "json") -> str:
    string_items: Iterable[str] = map(str, items)
    return preprocess_filename(f"{sep.join(string_items)[:128]}.{fformat}")


def preprocess_filename(filename: str):
    return re.sub("[<>:\"\/\\\|?*]", "", filename)


def json_dump(path: str, obj: Any):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(jsonpickle.encode(obj), file, ensure_ascii=False, indent=4)
