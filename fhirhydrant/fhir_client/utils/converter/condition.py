from typing import Tuple, Optional

from fhir.resources.condition import Condition
from fhir.resources.fhirreference import FHIRReference

from text2phenotype.entity.attributes import Polarity, TextSpan
from text2phenotype.entity.concept import Concept

from ..converter.concept import ConceptConverter
from ..converter.base import BaseFHIRConverter
from ..converter.helpers import make_codeable_concept, attach_polarity, \
    get_polarity, attach_range


class ConditionConverter(BaseFHIRConverter):
    DEFAULT_TYPE = 'allergy'

    @classmethod
    def to_fhir(cls,
                obj: Concept,
                subject_reference: str,
                polarity: Polarity,
                intolerance_type: str = None,
                text_span: TextSpan = None) -> Condition:
        condition = Condition()

        condition.subject = FHIRReference()
        condition.subject.reference = subject_reference

        condition.code = make_codeable_concept(obj.preferredText, obj.code, obj.codingScheme)
        condition = attach_polarity(condition, polarity)

        if text_span:
            condition = attach_range(condition, text_span.start, text_span.stop, text_span.text)

        return condition

    @classmethod
    def from_fhir(cls, resource: Condition) -> Tuple[Concept, Optional[Polarity]]:
        concept = ConceptConverter.from_fhir(resource.code)
        polarity = get_polarity(resource)
        if polarity is not None:
            polarity = Polarity(polarity)

        return concept, polarity
