from abc import abstractmethod, ABC
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class AbstractScraper(ABC):

    def __init__(self, starting_point: str) -> None:
        self.__configure_driver()
        self.starting_point = starting_point

    def _configure_driver_options(self) -> Options:
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        return chrome_options

    def __configure_driver(self) -> None:
        chrome_options: Options = self._configure_driver_options()
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()

    def navigate(self, url: Optional[str] = None) -> None:
        if not url:
            self.driver.get(self.starting_point)
        else:
            self.driver.get(url)

    def open_new_tab(self, url: str) -> None:
        self.driver.execute_script(f"window.open('about:blank', '{url}');")
        self.driver.switch_to.window(url)

    @abstractmethod
    def run(self) -> None: ...

    def switch_to_first_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def close_tab(self) -> None:
        self.driver.close()
        self.switch_to_first_tab()

    def stop(self) -> None:
        if self.driver.service.process:
            self.driver.quit()
