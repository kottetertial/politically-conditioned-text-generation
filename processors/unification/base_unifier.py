import os
from abc import abstractmethod
from typing import List

from constants import Env, TargetPath, Symbol
from processors.unification.unified_document import UnifiedDocument
from scrapers.model.base_document import BaseDocument
from utils import generate_full_path, json_load, generate_filename, json_dump


class BaseUnifier:
    SOURCE = Symbol.EMPTY
    DOC_PATH = Symbol.EMPTY
    TARGET_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.DATA, TargetPath.DOCUMENTS)

    def __init__(self):
        self.doc_count = self._get_current_doc_count()

    def run(self) -> None:
        list_of_files: List[str] = os.listdir(self.DOC_PATH)
        for file in list_of_files:
            self.doc_count += 1
            document: BaseDocument = json_load(f"{self.DOC_PATH}/{file}")
            refactored_document: UnifiedDocument = self._unify_document(document)
            filename: str = generate_full_path(self.TARGET_PATH,
                                               generate_filename([self.doc_count, refactored_document.source]))
            json_dump(filename, refactored_document)

    @abstractmethod
    def _unify_document(self, document: BaseDocument) -> UnifiedDocument: ...

    def _get_current_doc_count(self) -> int:
        return len(os.listdir(self.TARGET_PATH))
