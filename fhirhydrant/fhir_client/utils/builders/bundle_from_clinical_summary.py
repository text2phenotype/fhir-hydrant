from functools import partial
from itertools import chain

from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhir.resources.condition import Condition
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.observation import Observation
from fhir.resources.resource import Resource
from text2phenotype.common.clinical_summary import SummaryResult, ClinicalSummary

from fhirhydrant.fhir_client.utils.converter.allergy import AllergyIntoleranceConverter
from fhirhydrant.fhir_client.utils.converter.condition import ConditionConverter
from fhirhydrant.fhir_client.utils.converter.drug_attributes import DrugAttributesConverter
from fhirhydrant.fhir_client.utils.converter.lab_attributes import LabAttributesConverter


def _lab_test_to_observation(result: SummaryResult, subject_reference: str) -> Observation:
    concept = result.concept
    attributes = result.attributes
    attributes.polarity = result.polarity

    observation = LabAttributesConverter.to_fhir(
        attributes,
        code=concept.code,
        coding_system=concept.codingScheme,
        subject_reference=subject_reference,
        text_span=result.text_span
    )
    return observation


def _medications_to_statement(result: SummaryResult, subject_reference: str) -> MedicationStatement:
    concept = result.concept
    attributes = result.attributes
    attributes.polarity = result.polarity

    statement = DrugAttributesConverter.to_fhir(
        attributes,
        subject_reference,
        drug_name=concept.preferredText,
        drug_code=concept.code,
        coding_system=concept.codingScheme,
        text_span=result.text_span
    )

    return statement


def _allergies_to_intolerance(result: SummaryResult, subject_reference: str) -> AllergyIntolerance:
    return AllergyIntoleranceConverter.to_fhir(
        result.concept,
        polarity=result.polarity,
        subject_reference=subject_reference,
        text_span=result.text_span
    )


def _disease_to_condition(result: SummaryResult, subject_reference: str) -> Condition:
    return ConditionConverter.to_fhir(
        result.concept,
        polarity=result.polarity,
        subject_reference=subject_reference,
        text_span=result.text_span
    )


def build_bundle_from_clinical_summary(summary: ClinicalSummary, ref_resource: Resource):
    resource_ref = f"{ref_resource.get('resourceType', '')}/{ref_resource.get('id', '')}"

    map_lab_test = partial(_lab_test_to_observation, subject_reference=resource_ref)
    map_medication = partial(_medications_to_statement, subject_reference=resource_ref)
    map_allergies = partial(_allergies_to_intolerance, subject_reference=resource_ref)
    map_conditions = partial(_disease_to_condition, subject_reference=resource_ref)

    observations = list(filter(None, map(map_lab_test, getattr(summary, 'Lab', []))))
    medication_statements = list(filter(None, map(map_medication, getattr(summary, 'Medication', []))))
    allergies = list(filter(None, map(map_allergies, getattr(summary, 'Allergy', []))))
    conditions = getattr(summary, 'DiseaseDisorder', []) + getattr(summary, 'SignSymptom', [])
    conditions = list(filter(None, map(map_conditions, conditions))) if conditions else []

    bundle = Bundle()
    bundle.type = 'batch'
    bundle.entry = []
    for resource in chain(observations, medication_statements, allergies, conditions):
        entry = BundleEntry()
        entry.request = BundleEntryRequest()
        entry.request.method = "POST"
        entry.request.url = "/{}".format(resource.resource_type)
        entry.resource = resource
        bundle.entry.append(entry)

    return bundle


def parse_bundle(bundle: Bundle):
    entries = bundle.entry
    dict_observations = list(filter(lambda b: b.resource.resource_type == 'Observation', entries))
    observations = list(map(lambda f: f.resource, dict_observations))

    dict_medications = list(filter(lambda b: b.resource.resource_type == 'MedicationStatement', entries))
    medication_statements = list(map(lambda f: f.resource, dict_medications))

    dict_allergies = list(filter(lambda b: b.resource.resource_type == 'AllergyIntolerance', entries))
    allergies = list(map(lambda f: f.resource, dict_allergies))

    dict_conditions = list(filter(lambda b: b.resource.resource_type == 'Condition', entries))
    conditions = list(map(lambda f: f.resource, dict_conditions))

    return {'bundle_id': bundle.id,
            'observations': observations,
            'medication_statements': medication_statements,
            'allergies': allergies,
            'conditions': conditions}
