import copy
from typing import Optional, Union

from fhir.resources.annotation import Annotation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.domainresource import DomainResource
from fhir.resources.extension import Extension
from fhir.resources.quantity import Quantity
from fhir.resources.range import Range

from text2phenotype.entity.attributes import Polarity
from ..converter.coding_system import vocab_to_coding_system

ANNOTATION_URL = "http://hl7.org/fhir/StructureDefinition/Annotation"
RANGE_ANNOTATION_TEXT = 'range'
POLARITY_ANNOTATION_TEXT = 'polarity'


def make_codeable_concept(text: str, code: str, scheme: str) -> Optional[CodeableConcept]:
    if not text and not code:
        return None
    coding = Coding()
    coding.system = vocab_to_coding_system(scheme, default=scheme)
    coding.code = code

    concept = CodeableConcept()
    concept.text = text
    concept.coding = [coding]

    return concept


def make_annotation(text: str, ext: Extension) -> Extension:
    annotation = Annotation()
    annotation.text = text

    extension = Extension()
    extension.url = ANNOTATION_URL
    extension.valueAnnotation = annotation
    annotation.extension = [ext]
    return extension


def first(iterable):
    return next(iter(iterable or []), None)


def attach_range(element: DomainResource, start: int, stop: int,
                 annotation: str = RANGE_ANNOTATION_TEXT) -> DomainResource:
    if start is None and stop is None:
        return element

    element = copy.deepcopy(element)
    if element.extension is None:
        element.extension = []

    extension = Extension()
    extension.url = "http://hl7.org/fhir/StructureDefinition/Range"
    extension.valueRange = Range()
    extension.valueRange.low = Quantity(dict(value=start))
    extension.valueRange.high = Quantity(dict(value=stop))

    element.extension.append(make_annotation(annotation, extension))
    return element


def attach_polarity(element: DomainResource, polarity: Union[str, Polarity]) -> DomainResource:
    if polarity is None:
        return element

    element = copy.deepcopy(element)
    polarity_value = polarity.polarity if isinstance(polarity, Polarity) else (polarity == Polarity.POSITIVE)

    if not polarity_value:
        if element.extension is None:
            element.extension = []

        extension = Extension()
        extension.url = "http://hl7.org/fhir/datatypes.html#boolean"
        extension.valueBoolean = polarity_value

        element.extension.append(make_annotation(POLARITY_ANNOTATION_TEXT, extension))
    return element


def extract_extension(element: DomainResource, annotation_text: str) -> Optional[Extension]:
    if element.extension is None:
        return None
    annotations = (a.valueAnnotation for a in filter(lambda x: x.valueAnnotation is not None, element.extension))
    annotation = first(filter(lambda a: a.text == annotation_text, annotations))
    if annotation is None:
        return None
    return first(annotation.extension)


def get_range(element: DomainResource, annotation: str = RANGE_ANNOTATION_TEXT) -> tuple:
    range_ext: Extension = extract_extension(element, annotation)
    if range_ext is None:
        return None, None
    range_ext = range_ext.valueRange
    return range_ext.low.value, range_ext.high.value


def get_polarity(element: DomainResource) -> Optional[str]:
    polarity_ext = extract_extension(element, POLARITY_ANNOTATION_TEXT)
    if polarity_ext is None:
        return None
    polarity_value = polarity_ext.valueBoolean

    if polarity_value:
        return Polarity.POSITIVE
    return Polarity.NEGATIVE
