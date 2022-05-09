from typing import List

from spacy import Language
from spacy.tokens import Doc


class TextNormalizer:

    def __init__(self,
                 nlp: Language) -> None:
        self.nlp = nlp

    def process(self, text: str) -> List[str]:
        doc: Doc = self.nlp(text)
        return [token.lemma_ for token in doc if not token.is_punct and not token.is_stop and not token.is_space]
