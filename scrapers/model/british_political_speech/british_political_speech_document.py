from datetime import datetime
from typing import Optional

from scrapers.model.base_document import BaseDocument


class BritishPoliticalSpeechDocument(BaseDocument):

    def __init__(self,
                 url: str,
                 title: Optional[str],
                 date: Optional[datetime],
                 text: Optional[str],
                 location: Optional[str],
                 party: Optional[str],
                 speaker: Optional[str]):
        super().__init__(url, title, date, text)
        self.party = party
        self.speaker = speaker
        self.location = location
