from datetime import datetime
from typing import Optional, List

from scrapers.model.base_document import BaseDocument


class Manifesto(BaseDocument):

    def __init__(self,
                 url: str,
                 title: Optional[str],
                 date: Optional[datetime],
                 text: Optional[str],
                 person: List[str],
                 party: Optional[str]):
        super().__init__(url, title, date, text)
        self.person = person
        self.party = party
