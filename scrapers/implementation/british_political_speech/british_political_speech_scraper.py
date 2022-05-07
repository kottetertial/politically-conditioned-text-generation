import re
from datetime import datetime
from time import sleep
from typing import Optional, List, Tuple

from dateutil import parser
from dateutil.parser import parserinfo
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from constants import Env, SourceUrl, TargetPath
from scrapers.scraper_constants import Selector, ClassName, Tag, Attribute, Misc
from scrapers.implementation.over_vpn_scraper import OverVPNScraper
from scrapers.model.british_political_speech.british_political_speech_document import BritishPoliticalSpeechDocument
from scrapers.scraper_utils import auto_navigate, close_tab, auto_quit, open_new_tab
from utils import generate_full_path, generate_filename, json_dump


class BritishPoliticalSpeechScraper(OverVPNScraper):
    DOC_COUNTER = 0

    DOC_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.BRITISH_POLITICAL_SPEECH_DOCS)

    def __init__(self) -> None:
        super().__init__(SourceUrl.BRITISH_POLITICAL_SPEECH + SourceUrl.ARCHIVE)
        self._start_vpn()

    @auto_navigate
    @auto_quit
    def run(self) -> None:
        table: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.RESULTS_TABLE)
        if table:
            table_entries: List[WebElement] = table.find_elements(By.TAG_NAME, Tag.TR)
            for table_entry in table_entries:
                self.__extract_data_from_entry(table_entry)

    @close_tab
    def _start_vpn(self) -> None:
        sleep(3)
        self.switch_to_first_tab()
        self.driver.get(f"chrome-extension://{Env.EXTENSION_ID}/{Env.PATH_TO_HTML}")
        sleep(3)
        self._find_element(By.CSS_SELECTOR, Selector.BUTTON_SELECTOR).click()

    def __extract_data_from_entry(self, entry: WebElement) -> None:
        entry_data: List[WebElement] = entry.find_elements(By.TAG_NAME, Tag.TD)

        if len(entry_data) != 4 or not all(isinstance(item, WebElement) for item in entry_data):
            return

        url: Optional[str] = self.__extract_href(entry_data[3])

        if not url:
            return

        title: str = entry_data[3].text
        date: datetime = self.__extract_date(entry_data[0])
        party: str = entry_data[1].text
        speaker: str = entry_data[2].text

        location, text, speaker_from_text = self.__extract_text_info(url)

        speaker: str = speaker if not speaker_from_text else speaker_from_text

        self.DOC_COUNTER += 1
        document: BritishPoliticalSpeechDocument = BritishPoliticalSpeechDocument(url,
                                                                                  title,
                                                                                  date,
                                                                                  text,
                                                                                  location,
                                                                                  party,
                                                                                  speaker)

        filename: str = generate_full_path(self.DOC_PATH,
                                           generate_filename([str(self.DOC_COUNTER), title]))
        json_dump(filename, document)

    def __extract_date(self, entry: WebElement) -> datetime:
        parser_info: parserinfo = parserinfo(dayfirst=True)
        return parser.parse(entry.text, parser_info)

    def __extract_href(self, entry: WebElement) -> Optional[str]:
        link_element: Optional[WebElement] = self._find_element(By.TAG_NAME, Tag.A, entry)
        if link_element:
            return link_element.get_attribute(Attribute.HREF)

    @open_new_tab
    @auto_navigate
    @close_tab
    def __extract_text_info(self, url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        location: Optional[str] = self.__extract_location()
        text: Optional[str] = self.__extract_text()
        speaker: Optional[str] = self.__extract_speaker_from_text()
        return location, text, speaker

    def __extract_location(self) -> Optional[str]:
        location: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.SPEECH_LOCATION)
        if location:
            return location.text.removeprefix(Misc.LOCATION).strip()

    def __extract_text(self) -> Optional[str]:
        content: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.SPEECH_CONTENT)
        if content:
            return content.text

    def __extract_speaker_from_text(self) -> Optional[str]:
        speaker: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.SPEECH_SPEAKER)
        if speaker:
            return re.sub(r"\(\w+\)", "", speaker.text).strip()
