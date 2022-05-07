from datetime import datetime
from typing import Optional

from scrapers.model.base_document import BaseDocument


class HasPersonRefDocument(BaseDocument):

    def __init__(self,
                 url: str,
                 person_ref: Optional[str],
                 title: Optional[str],
                 date: Optional[datetime],
                 text: Optional[str]):
        super().__init__(url, title, date, text)
        self.person_ref = person_ref
