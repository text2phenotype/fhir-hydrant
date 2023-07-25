from fhir.resources.codeableconcept import CodeableConcept

from text2phenotype.entity.concept import Concept
from ..converter.base import BaseFHIRConverter
from ..converter.coding_system import coding_system_to_vocab
from ..converter.helpers import make_codeable_concept


class ConceptConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir(cls, obj: Concept):
        return make_codeable_concept(obj.preferredText, obj.code, obj.codingScheme)

    @classmethod
    def from_fhir(cls, resource: CodeableConcept) -> Concept:
        concept = Concept()

        concept.preferredText = resource.text
        coding = next(iter(resource.coding or []), None)

        if coding:
            concept.codingScheme = coding_system_to_vocab(coding.system, default=coding.system)
            concept.code = coding.code

        return concept
