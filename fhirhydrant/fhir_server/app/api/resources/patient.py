from datetime import datetime
from fhirhydrant.fhir_client.utils.converter.patient import PatientConverter
from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id
from fhirhydrant.fhir_server.app.utils.schemas.generator import resource_to_schema
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from requests.exceptions import HTTPError

from fhir.resources.fhirabstractbase import FHIRValidationError
from flask import abort, request
from flask_apispec import MethodResource, doc, marshal_with

from fhir.resources.patient import Patient
from text2phenotype.common.demographics import Demographics


@doc(tags=['Patient'])
class PatientResource(MethodResource):
    patient_resource = MetaResource(Patient)
    patient_schema = resource_to_schema(Patient)

    @doc(
        params={
            'patient_id': {
                'description': 'Patient ID'
            },
            'tenantId': {
                'in': 'header',
                'type': 'string'
            }
        },
        description="Returns single instance of Patient object"
    )
    @check_tenant_id
    @marshal_with(patient_schema, 200)
    def get(self, patient_id: str):
        try:
            patient = Patient(self.patient_resource.get(patient_id))
            return patient, 200
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        parameters=[
            {
                'in': 'body',
                'name': 'patient',
                'required': True,
                'schema': {
                    'type': 'string'
                }
            }
        ],
        params={
            'tenantId': {
                'in': 'header',
                'type': 'string'
            },
        }
    )
    @check_tenant_id
    @marshal_with(patient_schema, code=201, description="Object successfully created", apply=False)
    def post(self):
        patient_json = request.get_json()

        try:
            patient = Patient(patient_json)

        except FHIRValidationError:
            patient_json['dob'] = datetime.strptime(patient_json['dob'][0][0], "%m/%d/%Y")
            demographics = Demographics(**patient_json)
            patient = PatientConverter.to_fhir(demographics)

        created_patient = self.patient_resource.create(patient)
        return created_patient, 201

    @check_tenant_id
    @doc(
        params={
            'patient_id': {
                'description': 'Patient ID'
            },
            'tenantId': {
                'in': 'header',
                'type': 'string'
            }
        },
        description="Delete instance of Patient object"
    )
    def delete(self, patient_id: str):
        deleted = self.patient_resource.delete(patient_id)
        if deleted:
            return None, 204
        else:
            abort(500)
