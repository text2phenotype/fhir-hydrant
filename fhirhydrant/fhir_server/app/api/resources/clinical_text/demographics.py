import traceback

from fhirhydrant.fhir_client.utils.enums.document_reference_source import DocumentReferenceSource
from fhirhydrant.fhir_server.app.utils.document_reference_linker import create_document_reference
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_client.utils.converter.patient import PatientConverter
from fhirhydrant.fhir_server.app.api.schemas.responses.document_reference import DocumentSchema
from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id
from fhirhydrant.fhir_server.app.api.schemas.demographics import DemographicsSchema
from requests.exceptions import HTTPError

from flask import request
from flask_apispec import MethodResource, doc, marshal_with

from fhir.resources.patient import Patient

from text2phenotype.apiclients.biomed import BioMedClient
from text2phenotype.common.demographics import Demographics


def text_to_demographics(clinical_text: str) -> Demographics:
    biomed_client = BioMedClient()
    demographics_data = biomed_client.get_demographics(clinical_text)
    schema = DemographicsSchema()

    return Demographics(**schema.load(demographics_data))


@doc(tags=['Demographics'])
class DemographicsResource(MethodResource):

    @doc(
        description='Allows create Patient and DocumentReference from clinical text',
        consumes='text/plain',
        parameters=[
            {
                'in': 'body',
                'name': 'clinical_text',
                'required': True,
                'schema': {
                    'type': 'string'
                }
            }
        ],
        params={'tenantId': {
            'in': 'header',
            'type': 'string'
        }}
    )
    @check_tenant_id
    @marshal_with(DocumentSchema(), code=201, description="Object successfully created")
    def post(self):
        try:
            clinical_text = request.get_data(as_text=True)
            demographics = text_to_demographics(clinical_text)
            patient = PatientConverter.to_fhir(demographics)
            created = MetaResource(Patient).create(patient)
            result = create_document_reference(clinical_text, DocumentReferenceSource.clinical_text, created)
            return result, 201

        except HTTPError as e:
            return 'BIOMED internal error', e.response.status_code
        except Exception:
            return f'FHIR Hydrant internal error: {traceback.format_exc()}', 500
