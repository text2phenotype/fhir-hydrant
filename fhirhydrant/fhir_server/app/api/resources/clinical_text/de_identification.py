import traceback
from requests.exceptions import HTTPError
from flask import request
from flask_apispec import MethodResource, doc, marshal_with

from text2phenotype.apiclients.biomed import BioMedClient

from fhirhydrant.fhir_client.utils.enums.document_reference_source import DocumentReferenceSource
from fhirhydrant.fhir_server.app.utils.document_reference_linker import create_document_reference
from fhirhydrant.fhir_server.app.api.schemas.responses.document_reference import DocumentSchema
from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id
from fhirhydrant.fhir_server.app.api.decorators.limit_payload_size import limit_payload_size
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv


def text_de_identification(clinical_text: str) -> str:
    # maybe need to create a global biomed client,
    # because it used also in clinical_text
    biomed_client = BioMedClient()
    text_deid = biomed_client.get_redacted_text(clinical_text)
    return text_deid


@doc(tags=['De-identification'])
class DeIdentificationResource(MethodResource):

    @doc(
        description='Allows to de-identify the clinical text and create DocumentReference',
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
    @limit_payload_size(FhirServerEnv.MAX_CONTENT_LENGTH.value)
    @marshal_with(DocumentSchema(), code=201, description="De-identified object successfully created")
    def post(self):
        try:
            clinical_text: str = request.get_data(as_text=True, cache=False)
            deid_text: str = text_de_identification(clinical_text)
            result = create_document_reference(deid_text, DocumentReferenceSource.de_id)
            return result, 201

        except HTTPError as e:
            return 'BIOMED internal error', e.response.status_code
        except Exception:
            return f'FHIR Hydrant internal error: {traceback.format_exc()}', 500
