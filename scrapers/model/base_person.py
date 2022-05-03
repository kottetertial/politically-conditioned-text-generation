from datetime import datetime
from typing import Optional


class BasePerson:

    def __init__(self,
                 url: str,
                 name: Optional[str],
                 party: Optional[str]):
        self.url = url
        self.name = name
        self.party = party
        self.created_timestamp = datetime.now()
