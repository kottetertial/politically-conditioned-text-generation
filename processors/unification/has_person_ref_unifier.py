import os
from abc import ABC
from typing import List, Dict

from constants import Symbol
from processors.unification.base_unifier import BaseUnifier
from scrapers.model.base_person import BasePerson
from utils import json_load


class HasPersonRefUnifier(BaseUnifier, ABC):
    PERSON_PATH = Symbol.EMPTY

    def __init__(self) -> None:
        super().__init__()
        self.person_party_mapping: Dict[str, str] = self.__extract_person_ref_to_party_mapping()

    def __extract_person_ref_to_party_mapping(self) -> Dict[str, str]:
        list_of_files: List[str] = os.listdir(self.PERSON_PATH)
        mapping: Dict[str, str] = {}
        for file in list_of_files:
            person: BasePerson = json_load(f"{self.PERSON_PATH}/{file}")
            mapping[person.url] = person.party
        return mapping
