from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id

from fhirhydrant.fhir_server.app.utils.schemas.generator import resource_to_schema

from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from flask import abort, request
from flask_apispec import MethodResource, doc, marshal_with
from requests.exceptions import HTTPError

from fhir.resources.documentreference import DocumentReference
from fhir.resources.fhirabstractbase import FHIRValidationError


@doc(tags=['Document Reference'])
class DocumentReferenceResource(MethodResource):
    document_reference_resource = MetaResource(DocumentReference)
    document_reference_schema = resource_to_schema(DocumentReference)

    @doc(
        description='Allows create DocumentReference',
        consumes='text/plain',
        parameters=[
            {
                'in': 'body',
                'name': 'document_reference',
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
    @marshal_with(document_reference_schema, 201)
    def post(self):
        document_reference_json = request.get_json()
        try:
            new_document_reference = DocumentReference(document_reference_json)
            created_document_reference = self.document_reference_resource.create(new_document_reference)
            return DocumentReference(created_document_reference), 201

        except FHIRValidationError:
            abort(422)
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        params={
            'document_reference_id': {
                'description': 'Document Reference ID'
            }
        },
        description="Returns single instance or list of Document Reference object"
    )
    @check_tenant_id
    @marshal_with(document_reference_schema, 201)
    def get(self, document_reference_id: str):
        try:
            result = self.document_reference_resource.get(document_reference_id)
            return result, 200
        except HTTPError as e:
            abort(e.response.status_code)

    @check_tenant_id
    def delete(self, document_reference_id: str):
        deleted = self.document_reference_resource.delete(document_reference_id)
        if deleted:
            return None, 204
        else:
            abort(500)
