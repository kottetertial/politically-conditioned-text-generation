from typing import Optional

from constants import TargetPath, Env, SourceName, SourceUrl
from processors.unification.base_unifier import BaseUnifier
from processors.unification.unified_document import UnifiedDocument
from scrapers.model.manifestos.manifesto import Manifesto
from utils import generate_full_path


class ManifestoUnifier(BaseUnifier):
    DOC_PATH = generate_full_path(Env.ROOT_PREFIX, TargetPath.MANIFESTOS)

    def _unify_document(self, document: Manifesto) -> UnifiedDocument:
        source: str = self.__detect_source(document.url)
        year: Optional[int] = document.date.year if document.date else None
        refactored_document: UnifiedDocument = UnifiedDocument(source,
                                                               document.url,
                                                               document.title,
                                                               document.text,
                                                               year,
                                                               document.party)
        return refactored_document

    def __detect_source(self, url: str) -> str:
        if url.startswith(SourceUrl.LABOUR):
            return SourceName.LABOUR_MANIFESTOS
        elif url.startswith(SourceUrl.LIBERAL):
            return SourceName.LIBERAL_MANIFESTOS
        elif url.startswith(SourceUrl.CONSERVATIVE):
            return SourceName.CONSERVATIVE_MANIFESTOS
