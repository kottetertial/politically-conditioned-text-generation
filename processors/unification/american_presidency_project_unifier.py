from typing import Optional

from constants import Env, TargetPath, SourceName
from processors.unification.has_person_ref_unifier import HasPersonRefUnifier
from processors.unification.unified_document import UnifiedDocument
from scrapers.model.american_presidency_project.american_presidency_project_document import AmericanPresidencyDocument
from utils import generate_full_path


class AmericanPresidencyProjectUnifier(HasPersonRefUnifier):
    SOURCE = SourceName.AMERICAN_PRESIDENCY_PROJECT
    DOC_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.AMERICAN_PRESIDENCY_PROJECT_DOCS)
    PERSON_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.AMERICAN_PRESIDENCY_PROJECT_PEOPLE)

    def _unify_document(self, document: AmericanPresidencyDocument) -> UnifiedDocument:
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
