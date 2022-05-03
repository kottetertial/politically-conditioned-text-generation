from datetime import datetime
from typing import List, Optional


class AmericanPresidencyDocument:

    def __init__(self,
                 url: str,
                 person_ref: Optional[str],
                 title: Optional[str],
                 date: Optional[datetime],
                 text: Optional[str],
                 categories: Optional[List[str]],
                 location: Optional[str]):
        self.url = url
        self.person_ref = person_ref
        self.title = title
        self.date = date
        self.text = text
        self.categories = categories
        self.location = location
        self.created_timestamp = datetime.now()
