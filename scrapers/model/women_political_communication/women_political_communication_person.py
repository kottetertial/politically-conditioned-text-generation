from typing import Optional

from scrapers.model.base_person import BasePerson


class WomenPoliticalCommunicationPerson(BasePerson):

    def __init__(self,
                 url: str,
                 name: Optional[str],
                 party: Optional[str],
                 website: Optional[str]):
        super().__init__(url, name, party)
        self.website = website
