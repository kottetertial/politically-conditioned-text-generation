from datetime import datetime
from typing import List, Optional, Tuple

from dateutil import parser
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from scrapers.constants import Source, Tag, Attribute, Env, TargetPath, Misc
from scrapers.implementation.base_scraper import BaseScraper
from scrapers.model.manifestos.manifesto import Manifesto
from scrapers.scraper_utils import auto_navigate, json_dump, open_new_tab, close_tab, element_exists, \
    generate_full_path, generate_filename


class ManifestoScraper(BaseScraper):
    DOC_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.MANIFESTOS)

    def __init__(self, starting_point: str) -> None:
        super().__init__(starting_point)
        self.party = self.__detect_party()

    def __detect_party(self) -> str:
        match self.starting_point:
            case Source.LABOUR:
                return "Labour"
            case Source.LIBERAL:
                return "Liberal"
            case Source.CONSERVATIVE:
                return "Conservative"

    @auto_navigate
    def run(self) -> None:
        manifestos: List[WebElement] = self.driver.find_elements(By.TAG_NAME, Tag.LI)
        for manifesto in manifestos:
            self.__extract_manifesto(manifesto)

    def __extract_manifesto(self, manifesto: WebElement):
        if not manifesto:
            return

        link: Optional[WebElement] = self._find_element(By.TAG_NAME, Tag.A, manifesto)
        date: Optional[datetime] = parser.parse(link.text, default=Misc.DEFAULT_DATETIME) if link else None
        url: Optional[str] = link.get_attribute(Attribute.HREF) if link else None
        if not url:
            return

        title, text = self.__extract_text(url)
        person: List[str] = [element.text for element in manifesto.find_elements(By.TAG_NAME, Tag.B)
                             if Misc.WIN not in element.text
                             and not element.text.isdigit()]

        document: Manifesto = Manifesto(url,
                                        title,
                                        date,
                                        text,
                                        person,
                                        self.party)
        filename: str = generate_full_path(self.DOC_PATH,
                                           generate_filename([date.year, title]))
        json_dump(filename, document)

    @open_new_tab
    @auto_navigate
    @close_tab
    def __extract_text(self, url: str) -> Optional[Tuple[Optional[str], Optional[str]]]:
        text_element: Optional[WebElement] = self._find_embedded_element([
            (By.TAG_NAME, Tag.LI),
            (By.TAG_NAME, Tag.A)
        ])
        if text_element and Misc.FULL_TEXT in text_element.text:
            self.driver.get(text_element.get_attribute(Attribute.HREF))
        text_row: Optional[WebElement] = self.__extract_text_row()
        if text_row:
            title: Optional[str] = self.__extract_title(text_row)
            text: str = text_row.text.replace(title, "")
            return title, text
        return None, None

    def __extract_text_row(self) -> Optional[WebElement]:
        table_rows: List[WebElement] = self.driver.find_elements(By.TAG_NAME, Tag.TR)
        text_row: Optional[WebElement] = None
        for row in table_rows:
            if element_exists(By.TAG_NAME, Tag.H1, row) \
                    or element_exists(By.TAG_NAME, Tag.H2, row):  # for the only manifesto with its title formatted
                text_row = row                                    # as h2: labour 1983
                break
        return text_row

    def __extract_title(self, text_row: WebElement) -> Optional[str]:
        title_element: Optional[WebElement] = self._find_element(By.TAG_NAME, Tag.H1, text_row)
        if not title_element:
            title_element: Optional[WebElement] = self._find_element(By.TAG_NAME,  # for the only manifesto
                                                                     Tag.H2,       # with its title
                                                                     text_row)     # formatted as h2: labour 1983
        if title_element:
            return title_element.text
