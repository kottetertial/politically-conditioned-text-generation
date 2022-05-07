from datetime import datetime
from typing import Optional


class BaseDocument:

    def __init__(self,
                 url: str,
                 title: Optional[str],
                 date: Optional[datetime],
                 text: Optional[str]):
        self.url = url
        self.title = title
        self.date = date
        self.text = text
        self.created_timestamp = datetime.now()
