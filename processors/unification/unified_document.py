from typing import Optional, List


class UnifiedDocument:

    def __init__(self,
                 source: str,
                 url: str,
                 title: str,
                 text: str,
                 year: int,
                 party: str,
                 location: Optional[str] = None,
                 categories: Optional[List[str]] = None):
        self.url = url
        self.title = title
        self.text = text
        self.year = year
        self.source = source
        self.party = party
        self.location = location
        self.categories = categories
