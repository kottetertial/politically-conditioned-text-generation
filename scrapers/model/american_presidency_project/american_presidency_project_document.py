from datetime import datetime
from typing import Optional, List

from scrapers.model.base_document import BaseDocument


class AmericanPresidencyDocument(BaseDocument):

    def __init__(self,
                 url: str,
                 person_ref: Optional[str],
                 title: Optional[str],
                 date: Optional[datetime],
                 text: Optional[str],
                 categories: Optional[List[str]],
                 location: Optional[str]):
        super().__init__(url, title, date, text, location)
        self.person_ref = person_ref
        self.categories = categories
