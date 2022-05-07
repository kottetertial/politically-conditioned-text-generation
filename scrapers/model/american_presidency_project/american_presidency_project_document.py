from datetime import datetime
from typing import Optional, List

from scrapers.model.has_person_ref_document import HasPersonRefDocument


class AmericanPresidencyDocument(HasPersonRefDocument):

    def __init__(self,
                 url: str,
                 person_ref: Optional[str],
                 title: Optional[str],
                 date: Optional[datetime],
                 text: Optional[str],
                 categories: Optional[List[str]],
                 location: Optional[str]):
        super().__init__(url, person_ref, title, date, text)
        self.categories = categories
        self.location = location
