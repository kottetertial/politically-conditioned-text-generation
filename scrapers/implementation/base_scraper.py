from abc import ABC
from typing import Any, Optional, List, Tuple

from selenium.webdriver.remote.webelement import WebElement

from scrapers.implementation.abstract_scraper import AbstractScraper
from scrapers.scraper_utils import check_exists


class BaseScraper(AbstractScraper, ABC):

    @check_exists
    def _find_element(self, by: str, value: Any, location: Optional[WebElement] = None) -> Optional[WebElement]:
        if not location:
            return self.driver.find_element(by, value)
        return location.find_element(by, value)

    def _find_embedded_element(self, by_value: List[Tuple[str, Any]], location: Optional[WebElement] = None) \
            -> Optional[WebElement]:
        element: Optional[WebElement] = None
        for by, value in by_value:
            element = self._find_element(by, value, location)
            if not element:
                break
            location: WebElement = element
        return element
