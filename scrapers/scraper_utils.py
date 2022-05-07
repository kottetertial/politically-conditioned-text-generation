from typing import Union, Callable, Any, Optional, Iterable

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from scrapers.implementation.abstract_scraper import AbstractScraper


def auto_navigate(function: Callable) -> Callable:
    def wrapper(obj: AbstractScraper, *args: Iterable[Any]) -> Any:
        obj.navigate(*args)
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
