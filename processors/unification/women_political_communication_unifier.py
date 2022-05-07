from typing import Optional

from constants import SourceName, Env, TargetPath
from processors.unification.has_person_ref_unifier import HasPersonRefUnifier
from processors.unification.unified_document import UnifiedDocument
from scrapers.model.women_political_communication.women_political_communication_document import \
    WomenPoliticalCommunicationDocument
from utils import generate_full_path


class WomenPoliticalCommunicationUnifier(HasPersonRefUnifier):
    SOURCE = SourceName.WOMEN_POLITICAL_COMMUNICATION
    DOC_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.WOMEN_POLITICAL_COMMUNICATION_DOCS)
    PERSON_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.WOMEN_POLITICAL_COMMUNICATION_PEOPLE)

    def _unify_document(self, document: WomenPoliticalCommunicationDocument) -> UnifiedDocument:
        party: Optional[str] = self.person_party_mapping.get(document.person_ref)
        year: Optional[int] = document.date.year if document.date else None
        refactored_document: UnifiedDocument = UnifiedDocument(self.SOURCE,
                                                               document.url,
                                                               document.title,
                                                               document.text,
                                                               year,
                                                               party,
                                                               document.location,
                                                               document.categories)
        return refactored_document
