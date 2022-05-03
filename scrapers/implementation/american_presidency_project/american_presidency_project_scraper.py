import os
from datetime import datetime
from os import path
from typing import List, Dict, Optional, Tuple, Set, Iterable

from dateutil import parser
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from scrapers.model.american_presidency_project.american_presidency_project_document import AmericanPresidencyDocument
from scrapers.model.american_presidency_project.american_presidency_project_person import AmericanPresidencyPerson
from scrapers.implementation.base_scraper import BaseScraper
from scrapers.constants import Tag, Attribute, Source, ClassName, Selector, TargetPath, Misc
from scrapers.scraper_utils import element_exists, auto_navigate, generate_filename, json_dump, \
    generate_full_path, auto_quit, close_tab, open_new_tab


# TODO: refactor
class AmericanPresidencyProjectScraper(BaseScraper):
    DOC_COUNTER: int = 0

    DOC_PATH = generate_full_path(Misc.ROOT_PREFIX, TargetPath.AMERICAN_PRESIDENCY_PROJECT_DOCS)
    PERSON_PATH = generate_full_path(Misc.ROOT_PREFIX, TargetPath.AMERICAN_PRESIDENCY_PROJECT_PEOPLE)

    def __init__(self) -> None:
        super().__init__(Source.AMERICAN_PRESIDENCY_PROJECT + Source.DOCUMENTS)
        self.categories: List[str] = self.__extract_categories()

    @auto_navigate
    def __extract_categories(self) -> List[str]:
        main_doc_menu: WebElement = self.driver.find_element(By.CLASS_NAME, ClassName.FIELD_DOC_COUNT)
        category_menus: List[WebElement] = main_doc_menu.find_elements(By.CLASS_NAME, ClassName.DROPDOWN_MENU)
        category_elements: List[WebElement] = []
        for categories_container in category_menus:
            category_elements.extend(categories_container.find_elements(By.TAG_NAME, Tag.LI))
        last_category: WebElement = main_doc_menu.find_element(By.CSS_SELECTOR, Selector.LAST_CATEGORY)
        category_elements.append(last_category)
        return [element.find_element(By.TAG_NAME, Tag.A).get_attribute(Attribute.HREF)
                for element in category_elements]

    @auto_quit
    def run(self) -> None:
        for category in self.categories:
            self.__extract_rows_from_category(category)

    @auto_quit
    def resume_from_page(self, page_url: str, next_category: str) -> None:
        self.__get_current_doc_count()
        self.__extract_rows_from_category(page_url)
        self.resume_from_category(next_category)

    @auto_quit
    def resume_from_category(self, url: str) -> None:
        self.__get_current_doc_count()
        remaining_categories: List[str] = self.categories[self.categories.index(url):]
        for category in remaining_categories:
            self.__extract_rows_from_category(category)

    @auto_quit
    def extract_items_selective(self, urls: List[str]) -> None:
        self.__get_current_doc_count()
        self.__extract_documents(urls)
        person_urls: Set[str] = {self.__extract_link_to_person_from_doc(url) for url in urls}
        self.__extract_people(person_urls)

    @auto_quit
    def extract_docs_selective(self, urls: List[str]) -> None:
        self.__get_current_doc_count()
        self.__extract_documents(urls)

    @auto_quit
    def extract_people_selective(self, urls: List[str]) -> None:
        self.__extract_people(urls)

    def __get_current_doc_count(self) -> None:
        self.DOC_COUNTER = len(os.listdir(self.DOC_PATH))

    @auto_navigate
    def __extract_rows_from_category(self, url: str) -> None:
        self.__set_max_items_per_page()
        rows: Tuple[Set[Optional[str]], Set[Optional[str]]] = self.__extract_links_to_items()
        self.__extract_data_from_rows(rows)
        while element_exists(By.CLASS_NAME, ClassName.NEXT, self.driver):
            self.__go_to_the_next_page()
            rows: Tuple[Set[Optional[str]], Set[Optional[str]]] = self.__extract_links_to_items()
            self.__extract_data_from_rows(rows)

    def __extract_links_to_items(self) -> Tuple[Set[Optional[str]], Set[Optional[str]]]:
        content: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.VIEW_CONTENT)
        if content:
            rows: List[WebElement] = content.find_elements(By.CLASS_NAME, ClassName.ROW)
            doc_links, person_links = set(), set()
            for row in rows:
                doc_links.add(self.__extract_link_to_document(row))
                person_links.add(self.__extract_link_to_person(row))
            return doc_links, person_links

    def __extract_data_from_rows(self, rows: Tuple[Set[Optional[str]], Set[Optional[str]]]) -> None:
        self.__extract_documents(rows[0])
        self.__extract_people(rows[1])

    def __set_max_items_per_page(self) -> None:
        max_button: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.TAX_COUNT)
        if max_button and len(max_button.find_elements(By.TAG_NAME, Tag.A)):
            max_button.find_elements(By.TAG_NAME, Tag.A)[-1].click()

    def __go_to_the_next_page(self) -> None:
        next_button: Optional[WebElement] = self._find_embedded_element([
            (By.CLASS_NAME, ClassName.NEXT),
            (By.TAG_NAME, Tag.A)
        ])
        if next_button:
            next_button.click()

    def __extract_link_to_document(self, row: WebElement) -> Optional[str]:
        link: Optional[WebElement] = self._find_embedded_element([
            (By.CLASS_NAME, ClassName.FIELD_TITLE),
            (By.TAG_NAME, Tag.P),
            (By.TAG_NAME, Tag.A)
        ], row)
        if link:
            return link.get_attribute(Attribute.HREF)

    def __extract_link_to_person(self, row: WebElement) -> Optional[str]:
        link: Optional[WebElement] = self._find_embedded_element([
            (By.CLASS_NAME, ClassName.COL_MARGIN_TOP),
            (By.TAG_NAME, Tag.P),
            (By.TAG_NAME, Tag.A)
        ], row)
        if link:
            return link.get_attribute(Attribute.HREF)

    def __extract_documents(self, doc_links: Iterable[Optional[str]]) -> None:
        for doc_link in doc_links:
            self.__extract_document(doc_link)

    def __extract_people(self, person_links: Iterable[Optional[str]]) -> None:
        for person_link in person_links:
            self.__extract_person(person_link)

    @open_new_tab
    @auto_navigate
    @close_tab
    def __extract_document(self, url: str) -> None:
        self.DOC_COUNTER += 1
        person_ref: Optional[str] = self.__extract_person_ref()
        title: Optional[str] = self.__extract_title()
        date: Optional[datetime] = self.__extract_date()
        text: Optional[str] = self.__extract_text()
        categories: Optional[List[str]] = self.__extract_category_labels()
        location: Optional[str] = self.__extract_location()
        document: AmericanPresidencyDocument = AmericanPresidencyDocument(url,
                                                                          person_ref,
                                                                          title,
                                                                          date,
                                                                          text,
                                                                          categories,
                                                                          location)
        filename: str = generate_full_path(self.DOC_PATH,
                                           generate_filename([str(self.DOC_COUNTER), title]))
        json_dump(filename, document)

    @auto_navigate
    def __extract_link_to_person_from_doc(self, url: str) -> Optional[str]:
        return self.__extract_person_ref()

    def __extract_person_ref(self) -> Optional[str]:
        docs_person_title: Optional[WebElement] = self._find_embedded_element([
            (By.CLASS_NAME, ClassName.FIELD_DOCS_PERSON),
            (By.CLASS_NAME, ClassName.FIELD_TITLE),
            (By.TAG_NAME, Tag.H3),
            (By.TAG_NAME, Tag.A)
        ])
        if docs_person_title:
            return docs_person_title.get_attribute(Attribute.HREF)

    def __extract_title(self) -> Optional[str]:
        docs_text_title: Optional[WebElement] = self._find_embedded_element([
            (By.CLASS_NAME, ClassName.FIELD_DOCS_PERSON),
            (By.TAG_NAME, Tag.H1)
        ])
        if docs_text_title:
            return docs_text_title.text

    def __extract_date(self) -> Optional[datetime]:
        date_element: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.DATE_DISPLAY_SINGLE)
        if date_element and date_element.get_attribute(Attribute.CONTENT):
            return parser.parse(date_element.get_attribute(Attribute.CONTENT))

    def __extract_text(self) -> Optional[str]:
        content: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.FIELD_DOCS_CONTENT)
        if content:
            return content.text

    def __extract_meta(self) -> Optional[WebElement]:
        return self._find_element(By.CLASS_NAME, ClassName.GROUP_META)

    def __extract_category_labels(self) -> Optional[List[str]]:
        meta: Optional[WebElement] = self.__extract_meta()
        if meta:
            divs: List[WebElement] = meta.find_elements(By.TAG_NAME, Tag.DIV)
            return [div.text for div in divs if element_exists(By.TAG_NAME, Tag.A, div)
                    and div.find_element(By.TAG_NAME, Tag.A).get_attribute(Attribute.PROPERTY)
                    and Misc.PREFLABEL in div.find_element(By.TAG_NAME, Tag.A).get_attribute(Attribute.PROPERTY)]

    def __extract_location(self) -> Optional[str]:
        state: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.FIELD_SPOT_STATE)
        if state:
            return state.text

    @open_new_tab
    @auto_navigate
    @close_tab
    def __extract_person(self, url: str) -> None:
        name: Optional[str] = self.__extract_name()
        filename: str = generate_full_path(self.PERSON_PATH,
                                           generate_filename([name]))
        if not path.exists(filename):
            party: Optional[str] = self.__extract_party()
            person: AmericanPresidencyPerson = AmericanPresidencyPerson(url,
                                                                        name,
                                                                        party)
            json_dump(filename, person)

    def __extract_name(self) -> Optional[str]:
        field_title: Optional[WebElement] = self._find_element(By.CLASS_NAME, ClassName.FIELD_TITLE)
        if field_title:
            return field_title.text

    def __extract_party(self) -> Optional[str]:
        info: Dict[WebElement, WebElement] = dict(zip(self.driver.find_elements(By.CLASS_NAME, ClassName.LABEL_ABOVE),
                                                      self.driver.find_elements(By.CLASS_NAME, ClassName.F_ITEM)))
        party: List[str] = [value.text for key, value in info.items() if Misc.PARTY in key.text]
        if len(party):
            return party[0]
