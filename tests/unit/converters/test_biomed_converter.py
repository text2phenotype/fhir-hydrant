from typing import Tuple, Optional

from text2phenotype.entity.attributes import (
    TextSpan,
    DrugAttributes,
    LabAttributes,
    Polarity
)
from text2phenotype.entity.concept import Concept

from fhirhydrant.fhir_client.utils.converter.concept import ConceptConverter
from fhirhydrant.fhir_client.utils.converter.text_span import TextSpanConverter
from fhirhydrant.fhir_client.utils.converter.lab_attributes import LabAttributesConverter
from fhirhydrant.fhir_client.utils.converter.drug_attributes import DrugAttributesConverter
from fhirhydrant.fhir_client.utils.converter.questionnaire import QuestionnaireAnswersConverter
from fhirhydrant.fhir_client.utils.converter.allergy import AllergyIntoleranceConverter
from fhirhydrant.fhir_client.utils.converter.condition import ConditionConverter
from fhirhydrant.fhir_client.utils.converter.base import BaseFHIRConverter
from tests.unit.schemas.test_demographics import TestCase


class BiomedConverterTest(TestCase):

    def make_concept(self) -> Concept:
        concept = Concept()
        concept.preferredText = "concept_text"
        concept.code = "012345"
        concept.codingScheme = "RXNORM"
        return concept

    def make_textspan(self):
        span = TextSpan()
        span.text = "text_span"
        span.start = 0
        span.stop = 42
        return span

    def make_labattributes(self) -> LabAttributes:
        attributes = LabAttributes()
        attributes.polarity = "positive"
        attributes.labValue = TextSpan(source=["6.3", 45, 67])
        attributes.labValueUnit = TextSpan(source=["mmol/l", 89, 112])
        return attributes

    def make_drug_attributes(self) -> DrugAttributes:
        attributes = DrugAttributes()
        attributes.polarity = "positive"
        attributes.medStrengthNum = TextSpan(source=["14.0", 1, 12])
        attributes.medStrengthUnit = TextSpan(source=["mg", 78, 112])
        attributes.medFrequencyNumber = TextSpan(["2", 0, 67])
        attributes.medFrequencyUnit = TextSpan("d")
        return attributes

    def make_allergy(self) -> Concept:
        concept = Concept()
        concept.preferredText = "Ambien"
        concept.code = "131725"
        concept.codingScheme = "RXNORM"

        return concept

    def make_condition(self) -> Concept:
        concept = Concept()
        concept.preferredText = "Heart failure"
        concept.code = "84114007"
        concept.codingScheme = "SNOMEDCT_US"

        return concept

    def assertConceptEquals(self, expected: Concept, actual: Concept):
        pass
        self.assertEqual(expected.preferredText, actual.preferredText)
        self.assertEqual(expected.code, actual.code)
        self.assertEqual(expected.codingScheme, actual.codingScheme)

    def assertTextSpanEquals(self, expected: TextSpan, actual: TextSpan):
        self.assertEqual(expected.text, actual.text)
        self.assertEqual(expected.start, actual.start)
        self.assertEqual(expected.stop, actual.stop)

    def assertPolarityEquals(self, expected: Polarity, actual: Polarity):
        if isinstance(expected, str):
            expected = Polarity(expected)

        if expected.polarity:
            self.assertIsNone(actual)
        else:
            self.assertEqual(expected.polarity, actual.polarity)

    def assertLabAttributesEquals(self, expected: LabAttributes, actual: LabAttributes):
        self.assertTextSpanEquals(expected.labValue, actual.labValue)
        self.assertTextSpanEquals(expected.labValueUnit, actual.labValueUnit)
        self.assertPolarityEquals(expected.polarity, actual.polarity)

    def assertDrugAttributesEquals(self, expected: DrugAttributes, actual: DrugAttributes):
        self.assertPolarityEquals(expected.polarity, actual.polarity)
        try:
            # cast all values represented as text to float,
            # because in DrugAttributes *Num.text could be represented as int or float
            # but in Quantity value could be only of a float type

            actual.medFrequencyNumber.text = str(float(actual.medFrequencyNumber.text))
            expected.medFrequencyNumber.text = str(float(expected.medFrequencyNumber.text))
            actual.medStrengthNum.text = str(float(actual.medStrengthNum.text))
            expected.medStrengthNum.text = str(float(expected.medStrengthNum.text))
        except ValueError:
            pass

        self.assertTextSpanEquals(expected.medStrengthNum, actual.medStrengthNum)
        self.assertTextSpanEquals(expected.medStrengthUnit, actual.medStrengthUnit)
        self.assertTextSpanEquals(expected.medFrequencyNumber, actual.medFrequencyNumber)
        self.assertTextSpanEquals(expected.medFrequencyUnit, actual.medFrequencyUnit)
        pass

    def assertAllergyEqual(self, expected: Concept, actual: Tuple[Concept, Optional[Polarity]]):
        self.assertConceptEquals(expected, actual[0])
        self.assertPolarityEquals(Polarity(True), actual[1])

    def setUp(self) -> None:
        super(BiomedConverterTest, self).setUp()
        self.concept = self.make_concept()
        self.text_span = self.make_textspan()
        self.lab_attributes = self.make_labattributes()
        self.drug_attributes = self.make_drug_attributes()
        self.polarity = Polarity(polarity=True)
        self.allergy = self.make_allergy()
        self.condition = self.make_condition()

    def make_test(self, obj, converter_cls: BaseFHIRConverter, asserter: callable, **extra_kwargs):
        if extra_kwargs:
            fhir_repr = converter_cls.to_fhir(obj, **extra_kwargs)
        else:
            fhir_repr = converter_cls.to_fhir(obj)

        reconstructed = converter_cls.from_fhir(fhir_repr)
        asserter(obj, reconstructed)
        json_repr = fhir_repr.as_json()
        self.assertEqual(dict, type(json_repr))

    def test_concept(self):
        self.make_test(self.concept, ConceptConverter, self.assertConceptEquals)

    def test_textspan(self):
        self.make_test(self.text_span, TextSpanConverter, self.assertTextSpanEquals)

    def test_labattributes(self):
        extra = dict(
            code="0123456"
        )
        self.make_test(self.lab_attributes, LabAttributesConverter, self.assertLabAttributesEquals, **extra)

    def test_drug_attributes(self):
        extra = dict(
            subject_reference="Patient/12345",
            drug_name="Example medication",
            drug_code="0123456",
            coding_system="RXNORM"
        )
        self.make_test(self.drug_attributes, DrugAttributesConverter, self.assertDrugAttributesEquals, **extra)

    def test_questionnaire(self):
        answers = {
            'question_boolean': True,
            'question_int': 42,
            'question_float': 4.2,
            'question_str': "string",
            'group1': {
                'gr1_question_int': 1,
                'subgroup': {
                    'gr1_subgr_question_string': 'subgr_str'
                }
            }
        }

        fhir_repr = QuestionnaireAnswersConverter.to_fhir(answers)
        reconstructed = QuestionnaireAnswersConverter.from_fhir(fhir_repr)

        self.assertDictEqual(answers, reconstructed)

    def test_allergy(self):
        exrta = dict(
            subject_reference="Patient/12345",
            polarity=Polarity(True)
        )
        self.make_test(self.allergy, AllergyIntoleranceConverter, self.assertAllergyEqual, **exrta)

    def test_condition(self):
        extra = dict(
            subject_reference="Patient/12345",
            polarity=Polarity(True)
        )

        self.make_test(self.condition, ConditionConverter, self.assertAllergyEqual, **extra)