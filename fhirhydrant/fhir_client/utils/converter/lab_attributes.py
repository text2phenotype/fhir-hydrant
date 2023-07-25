from typing import Optional

from fhir.resources.fhirreference import FHIRReference
from fhir.resources.observation import Observation
from fhir.resources.quantity import Quantity

from text2phenotype.entity.attributes import LabAttributes, TextSpan

from ..converter.base import BaseFHIRConverter
from ..converter.helpers import make_codeable_concept, attach_polarity, \
    get_polarity, attach_range, get_range


class LabAttributesConverter(BaseFHIRConverter):
    DEFAULT_STATUS = "preliminary"
    PREFERRED_VOCAB = "http://loinc.org"

    TEXT_SPANS = (
        "labValue",
        "labValueUnit"
    )

    @classmethod
    def to_fhir(cls,
                obj: LabAttributes,
                code: str,
                coding_system: str = None,
                status: str = None,
                subject_reference: str = None,
                text_span: TextSpan = None) -> Optional[Observation]:
        observation = Observation()
        observation.status = status or cls.DEFAULT_STATUS
        observation.code = make_codeable_concept(None, code, coding_system or cls.PREFERRED_VOCAB)

        if observation.code is None:
            return None

        if obj.labValue is not None and obj.labValueUnit is not None:
            quantity = Quantity()
            quantity.value = float(obj.labValue.text)
            quantity.unit = obj.labValueUnit.text
            observation.valueQuantity = quantity

        if subject_reference:
            observation.subject = FHIRReference()
            observation.subject.reference = subject_reference

        observation = attach_polarity(observation, obj.polarity)

        if text_span:
            observation = attach_range(observation, text_span.start, text_span.stop, text_span.text)

        for span_name in cls.TEXT_SPANS:
            text_span = getattr(obj, span_name)
            if text_span is not None:
                observation = attach_range(observation, text_span.start, text_span.stop, span_name)

        return observation

    @classmethod
    def from_fhir(cls, resource: Observation) -> LabAttributes:
        attributes = LabAttributes()
        attributes.polarity = get_polarity(resource)

        attributes.labValueUnit = TextSpan()
        attributes.labValue = TextSpan()
        quantity = resource.valueQuantity
        if not quantity:
            return attributes

        attributes.labValue.text = str(quantity.value)
        attributes.labValueUnit.text = quantity.unit

        for span_name in cls.TEXT_SPANS:
            text_span = getattr(attributes, span_name)
            text_span.start, text_span.stop = get_range(resource, span_name)

        return attributes
