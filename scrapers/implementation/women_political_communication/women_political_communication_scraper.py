import re
from datetime import datetime
from typing import List, Optional

from dateutil import parser
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from constants import Env, TargetPath, SourceUrl, Symbol
from scrapers.implementation.base_scraper import BaseScraper
from scrapers.scraper_constants import ClassName, Tag, Attribute, Selector
from scrapers.model.women_political_communication.women_political_communication_document import \
    WomenPoliticalCommunicationDocument
from scrapers.model.women_political_communication.women_political_communication_person import \
    WomenPoliticalCommunicationPerson
from scrapers.scraper_utils import auto_navigate, auto_quit, open_new_tab, close_tab
from utils import generate_full_path, generate_filename, json_dump


class WomenPoliticalCommunicationScraper(BaseScraper):
    DOC_COUNTER = 0

    DOC_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.WOMEN_POLITICAL_COMMUNICATION_DOCS)
    PERSON_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.WOMEN_POLITICAL_COMMUNICATION_PEOPLE)

    def __init__(self) -> None:
        super().__init__(SourceUrl.WOMEN_POLITICAL_COMMUNICATION + SourceUrl.SPEAKERS)
        self.profiles_urls: List[str] = self.__extract_profile_urls()

    @auto_navigate
    def __extract_profile_urls(self) -> List[str]:
        profiles_lists: List[WebElement] = self.driver.find_elements(By.CLASS_NAME, ClassName.PROFILES_LIST)
        profiles_urls: List[str] = [profile.get_attribute(Attribute.HREF)
                                    for profiles_list in profiles_lists
                                    for profile in profiles_list.find_elements(By.TAG_NAME, Tag.A)]
        return profiles_urls

    @auto_quit
    def run(self) -> None:
        for profile_url in self.profiles_urls:
            self.__extract_data_from_profile(profile_url)

    @open_new_tab
    @auto_navigate
    @close_tab
    def __extract_data_from_profile(self, url: str) -> None:
        self.__extract_person(url)

        document_groups: List[WebElement] = self.driver.find_elements(By.CLASS_NAME, ClassName.ARTICLES)
        document_urls: List[str] = [element.get_attribute(Attribute.HREF)
                                    for document_group in document_groups
                                    for element in document_group.find_elements(By.TAG_NAME, Tag.A)]
        for document_url in document_urls:
            self.__extract_document(document_url)

    def __extract_person(self, url: str) -> None:
        name: Optional[str] = self.__extract_name()
        party: Optional[str] = self.__extract_party()
        website: Optional[str] = self.__extract_website()
        person: WomenPoliticalCommunicationPerson = WomenPoliticalCommunicationPerson(url,
                                                                                      name,
                                                                                      party,
                                                                                      website)
        filename: str = generate_full_path(self.PERSON_PATH,
                                           generate_filename([name]))
        json_dump(filename, person)

    def __extract_name(self) -> Optional[str]:
        name: WebElement = self._find_element(By.TAG_NAME, Tag.H1)
        if name:
            return name.text

    def __extract_info_table(self) -> Optional[WebElement]:
        return self._find_element(By.TAG_NAME, Tag.TABLE)

    def __extract_info_entry_content(self, entry: Optional[WebElement]) -> Optional[WebElement]:
        if entry:
            content: List[WebElement] = entry.find_elements(By.TAG_NAME, Tag.TD)
            if len(content):
                return content[-1]

    def __extract_party(self) -> Optional[str]:
        info_table: Optional[WebElement] = self.__extract_info_table()
        if info_table:
            party_entry: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.PARTY, info_table)
            entry_content: Optional[WebElement] = self.__extract_info_entry_content(party_entry)
            if entry_content:
                return entry_content.text

    def __extract_website(self) -> Optional[str]:
        info_table: Optional[WebElement] = self.__extract_info_table()
        if info_table:
            website_entry: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.WEBSITE, info_table)
            entry_content: Optional[WebElement] = self.__extract_info_entry_content(website_entry)
            if entry_content:
                link: Optional[WebElement] = self._find_element(By.TAG_NAME, Tag.A, entry_content)
                if link:
                    return link.get_attribute(Attribute.HREF)

    @open_new_tab
    @auto_navigate
    @close_tab
    def __extract_document(self, url: str) -> None:
        self.DOC_COUNTER += 1
        person_ref: Optional[str] = self.__extract_person_ref()
        title: Optional[str] = self.__extract_title()
        date: Optional[datetime] = self.__extract_date()
        text: Optional[str] = self.__extract_text()
        categories: Optional[List[str]] = self.__extract_categories()
        location: Optional[str] = self.__extract_location()
        document: WomenPoliticalCommunicationDocument = WomenPoliticalCommunicationDocument(url,
                                                                                            person_ref,
                                                                                            title,
                                                                                            date,
                                                                                            text,
                                                                                            categories,
                                                                                            location)
        filename: str = generate_full_path(self.DOC_PATH,
                                           generate_filename([str(self.DOC_COUNTER), title]))
        json_dump(filename, document)

    def __extract_person_ref(self) -> Optional[str]:
        profile_info: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.PROFILE_INFO)
        if profile_info:
            return profile_info.get_attribute(Attribute.HREF)

    def __extract_title(self) -> Optional[str]:
        title: Optional[WebElement] = self._find_element(By.TAG_NAME, Tag.H1)
        if title:
            return title.text

    def __extract_date_element(self) -> Optional[WebElement]:
        return self._find_element(By.CLASS_NAME, ClassName.WOMENSPEECH_DATE)

    def __extract_date(self) -> Optional[datetime]:
        date_element: Optional[WebElement] = self.__extract_date_element()
        if date_element:
            return parser.parse(self.__extract_date_string(date_element.text))

    def __extract_date_string(self, date: str) -> str:
        date_list: List = re.findall(r"\w+\s\d{2},\s\d{4}", date)
        if len(date_list):
            return date_list[0]
        return date

    def __extract_text(self) -> Optional[str]:
        post_content: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.POST_CONTENT)
        if post_content:
            return post_content.text

    def __extract_categories(self) -> Optional[List[str]]:
        categories: Optional[WebElement] = self._find_element(By.CSS_SELECTOR, Selector.POST_CATEGORIES)
        if categories:
            return [category.text.capitalize() for category in categories.find_elements(By.TAG_NAME, Tag.A)]

    def __extract_location(self) -> Optional[str]:
        date_element: Optional[WebElement] = self.__extract_date_element()
        if date_element and Symbol.DASH in date_element.text:
            dash_index: int = date_element.text.index(Symbol.DASH)
            return date_element.text[dash_index + 1:].strip()
