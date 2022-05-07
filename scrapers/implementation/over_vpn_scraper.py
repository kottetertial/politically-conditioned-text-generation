from abc import ABC, abstractmethod

from selenium.webdriver.chrome.options import Options

from constants import Env
from scrapers.implementation.base_scraper import BaseScraper


class OverVPNScraper(BaseScraper, ABC):

    def _configure_driver_options(self) -> Options:
        chrome_options: Options = Options()
        chrome_options.add_argument(f"load-extension={Env.PATH_TO_VPN_EXTENSION}")
        return chrome_options

    @abstractmethod
    def _start_vpn(self) -> None: ...
