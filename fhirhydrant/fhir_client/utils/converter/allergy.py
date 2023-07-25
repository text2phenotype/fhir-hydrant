from typing import Tuple, Optional

from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.fhirreference import FHIRReference

from text2phenotype.entity.attributes import Polarity, TextSpan
from text2phenotype.entity.concept import Concept

from ..converter.concept import ConceptConverter
from ..converter.base import BaseFHIRConverter
from ..converter.helpers import make_codeable_concept, attach_polarity, \
    get_polarity, attach_range


class AllergyIntoleranceConverter(BaseFHIRConverter):
    DEFAULT_TYPE = 'allergy'

    @classmethod
    def to_fhir(cls,
                obj: Concept,
                subject_reference: str,
                polarity: Polarity,
                intolerance_type: str = None,
                text_span: TextSpan = None
                ) -> AllergyIntolerance:
        intolerance = AllergyIntolerance()

        intolerance.type = intolerance_type or cls.DEFAULT_TYPE

        intolerance.patient = FHIRReference()
        intolerance.patient.reference = subject_reference

        intolerance.code = make_codeable_concept(obj.preferredText, obj.code, obj.codingScheme)
        intolerance = attach_polarity(intolerance, polarity)

        if text_span:
            intolerance = attach_range(intolerance, text_span.start, text_span.stop, text_span.text)

        return intolerance

    @classmethod
    def from_fhir(cls, resource: AllergyIntolerance) -> Tuple[Concept, Optional[Polarity]]:
        concept = ConceptConverter.from_fhir(resource.code)
        polarity = get_polarity(resource)
        if polarity is not None:
            polarity = Polarity(polarity)

        return concept, polarity
