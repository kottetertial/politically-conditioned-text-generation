from abc import abstractmethod
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class AbstractScraper:

    def __init__(self, starting_point: str) -> None:
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.starting_point = starting_point

    def start(self, url: Optional[str] = None) -> None:
        if not url:
            self.driver.get(self.starting_point)
        else:
            self.driver.get(url)

    def open_new_tab(self, url: str) -> None:
        self.driver.execute_script(f"window.open('about:blank', '{url}');")
        self.driver.switch_to.window(url)

    @abstractmethod
    def run(self) -> None: ...

    def close_tab(self) -> None:
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def stop(self) -> None:
        if self.driver.service.process:
            self.driver.quit()
