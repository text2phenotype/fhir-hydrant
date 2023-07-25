from enum import Enum


class DocumentReferenceSource(Enum):
    storage = 0,
    clinical_text = 1,
    de_id = 2
