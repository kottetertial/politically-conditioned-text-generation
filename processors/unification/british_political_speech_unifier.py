from typing import Optional

from constants import SourceName, TargetPath, Env
from processors.unification.base_unifier import BaseUnifier
from processors.unification.unified_document import UnifiedDocument
from scrapers.model.british_political_speech.british_political_speech_document import BritishPoliticalSpeechDocument
from utils import generate_full_path


class BritishPoliticalSpeechUnifier(BaseUnifier):
    SOURCE = SourceName.BRITISH_POLITICAL_SPEECH
    DOC_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.BRITISH_POLITICAL_SPEECH_DOCS)

    def _unify_document(self, document: BritishPoliticalSpeechDocument) -> UnifiedDocument:
        year: Optional[int] = document.date.year if document.date else None
        refactored_document: UnifiedDocument = UnifiedDocument(self.SOURCE,
                                                               document.url,
                                                               document.title,
                                                               document.text,
                                                               year,
                                                               document.party,
                                                               document.location)
        return refactored_document
