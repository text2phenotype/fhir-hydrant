import marshmallow
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.condition import Condition
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.observation import Observation
from fhirhydrant.fhir_server.app.utils.schemas.generator import resource_to_schema
from marshmallow import fields


class ClinicalResponseSchema(marshmallow.Schema):
    bundle_id = marshmallow.fields.String()
    observations = fields.Nested(resource_to_schema(Observation), required=True, many=True)
    medication_statements = fields.Nested(resource_to_schema(MedicationStatement), required=True, many=True)
    allergies = fields.Nested(resource_to_schema(AllergyIntolerance), required=True, many=True)
    conditions = fields.Nested(resource_to_schema(Condition), required=True, many=True)
