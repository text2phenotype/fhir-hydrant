from fhir.resources.annotation import Annotation

from text2phenotype.entity.attributes import TextSpan

from ..converter.base import BaseFHIRConverter
from ..converter.helpers import attach_range, get_range


class TextSpanConverter(BaseFHIRConverter):
    @classmethod
    def to_fhir(cls, obj: TextSpan):
        element = Annotation(dict(text=obj.text))
        element = attach_range(element, obj.start, obj.stop)
        return element

    @classmethod
    def from_fhir(cls, resource) -> TextSpan:
        span = TextSpan()
        span.text = resource.text
        span.start, span.stop = get_range(resource)
        return span
