from typing import List, Optional

from fhir.resources.dosage import DosageDoseAndRate, Dosage
from fhir.resources.fhirreference import FHIRReference
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.quantity import Quantity

from text2phenotype.entity.attributes import DrugAttributes, TextSpan

from ..converter.base import BaseFHIRConverter
from ..converter.helpers import make_codeable_concept, attach_polarity, \
    get_polarity, first, attach_range, get_range


class DrugAttributesConverter(BaseFHIRConverter):
    # It is possible to convert an medication route as CodeableConcept
    # https://www.hl7.org/fhir/valueset-route-codes.html

    DEFAULT_STATUS = 'intended'

    TEXT_SPANS = (
        "medStrengthNum",
        "medStrengthUnit",
        "medFrequencyNumber",
        "medFrequencyUnit"
    )

    @classmethod
    def to_fhir(cls,
                obj: DrugAttributes,
                subject_reference: str,
                drug_name: str,
                drug_code: str,
                coding_system: str,
                text_span: TextSpan = None
                ) -> Optional[MedicationStatement]:
        medication = MedicationStatement()
        medication.medicationCodeableConcept = make_codeable_concept(drug_name, drug_code, coding_system)
        if medication.medicationCodeableConcept is None:
            return None

        medication.status = cls.DEFAULT_STATUS
        medication.subject = FHIRReference()
        medication.subject.reference = subject_reference
        medication.dosage = DrugAttributesConverter.make_dosage(obj)
        medication = attach_polarity(medication, obj.polarity)

        if text_span:
            medication = attach_range(medication, text_span.start, text_span.stop, text_span.text)

        for span_name in cls.TEXT_SPANS:
            text_span = getattr(obj, span_name)
            medication = cls.annotate_range(text_span, span_name, medication)

        return medication

    @classmethod
    def from_fhir(cls, resource: MedicationStatement) -> DrugAttributes:
        attributes = DrugAttributes()
        attributes.medFrequencyNumber = TextSpan()
        attributes.medFrequencyUnit = TextSpan()
        attributes.medStrengthUnit = TextSpan()
        attributes.medStrengthNum = TextSpan()
        attributes.polarity = get_polarity(resource)

        dosage = first(resource.dosage)
        cls.extract_from_dosage(dosage, attributes)

        for span_name in cls.TEXT_SPANS:
            text_span = getattr(attributes, span_name)
            cls.extract_range(resource, text_span, span_name)

        return attributes

    @classmethod
    def make_dosage(cls, obj: DrugAttributes) -> List[Dosage]:
        dosage = Dosage()

        medStrengthNum = obj.medStrengthNum.text if obj.medStrengthNum.text is not None else ''
        medStrengthUnit = obj.medStrengthUnit.text if obj.medStrengthUnit.text is not None else ''
        medFrequencyNumber = obj.medFrequencyNumber.text if obj.medFrequencyNumber.text is not None else ''
        medFrequencyUnit = obj.medFrequencyUnit.text if obj.medFrequencyUnit.text is not None else ''
        dosage.text = ' '.join(filter(None, [medStrengthNum, medStrengthUnit, medFrequencyNumber, medFrequencyUnit]))

        dose_and_rate = DosageDoseAndRate()
        dose_and_rate.doseQuantity = cls.get_quantity(obj.medStrengthNum.text, obj.medStrengthUnit.text)
        dose_and_rate.rateQuantity = cls.get_quantity(obj.medFrequencyNumber.text, obj.medFrequencyUnit.text)
        dosage.doseAndRate = [dose_and_rate]

        return [dosage]

    @staticmethod
    def get_quantity(value: str, unit: str):
        q = Quantity()
        q.unit = unit
        try:
            q.value = float(value)
        except (ValueError, TypeError):
            q.value = None

        return q

    @classmethod
    def extract_from_dosage(cls, dosage: Dosage, obj: DrugAttributes):
        dosage_and_rate = first(dosage.doseAndRate)
        obj.medStrengthUnit.text = dosage_and_rate.doseQuantity.unit
        obj.medStrengthNum.text = str(dosage_and_rate.doseQuantity.value)

        obj.medFrequencyUnit.text = dosage_and_rate.rateQuantity.unit
        obj.medFrequencyNumber.text = str(dosage_and_rate.rateQuantity.value)

    @classmethod
    def annotate_range(cls, span: TextSpan, name: str, resource: MedicationStatement) -> MedicationStatement:
        return attach_range(resource, span.start, span.stop, name)

    @classmethod
    def extract_range(cls, resource: MedicationStatement, span: TextSpan, name: str):
        span.start, span.stop = get_range(resource, name)
