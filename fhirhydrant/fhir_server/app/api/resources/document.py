import base64

from fhirhydrant.fhir_client.utils.enums.document_reference_source import DocumentReferenceSource

from fhirhydrant.fhir_server.app.api.schemas.responses.document_reference import DocumentSchema

from fhirhydrant.fhir_server.app.utils.document_reference_linker import get_binary_id_by_document_reference_id, \
    create_document_reference, get_document_reference_by_provenance_id

from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource

from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id
from requests.exceptions import HTTPError

from flask import abort, request
from flask_apispec import doc, marshal_with
from flask_apispec import MethodResource

import marshmallow

from fhir.resources.binary import Binary
from fhir.resources.documentreference import DocumentReference
from fhir.resources.provenance import Provenance


class BinarySchema(marshmallow.Schema):
    document_id = marshmallow.fields.String()


@doc(tags=['Document'])
class DocumentResource(MethodResource):
    @doc(
        params={
            'document_id': {
                'description': 'Document ID'
            },
            'tenantId': {
                    'in': 'header',
                    'type': 'string'
                }
        },
        description="Returns single instance of Document object"
    )
    @check_tenant_id
    def get(self, document_id: str = None):
        try:
            if document_id is None:
                provenance_bundle = MetaResource(Provenance).get_all()
                provenances = provenance_bundle.get('entry', {})
                return provenances, 200
            else:
                binary_id: str = get_binary_id_by_document_reference_id(document_id)
                content: str = ""
                if binary_id:
                    document = MetaResource(Binary).get(binary_id)
                    content = base64.b64decode(document.get('data')).decode('utf-8')
                document_reference_meta = MetaResource(DocumentReference).get(document_id).get('meta')

                result = {
                    'content': content,
                    'meta': document_reference_meta
                }
                return result, 200
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        description='Allows create Document',
        consumes='text/plain',
        parameters=[
            {
                'in': 'body',
                'name': 'document_content',
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
            document_content = request.get_data(as_text=True)
            result = create_document_reference(document_content, DocumentReferenceSource.storage)
            return result, 201
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        params={
            'document_id': {
                'description': 'Document ID'
            },
            'tenantId': {
                'in': 'header',
                'type': 'string'
            }
        },
        description="Delete instance of Document object"
    )
    @check_tenant_id
    @marshal_with(DocumentSchema(), code=200)
    def delete(self, document_id: str):
        # here document_id is a provenance id, because document_id is used as pk

        document_reference_id = get_document_reference_by_provenance_id(document_id)
        binary_id = get_binary_id_by_document_reference_id(document_reference_id)
        MetaResource(Provenance).delete(document_id)
        MetaResource(DocumentReference).delete(document_reference_id)
        return MetaResource(Binary).delete(binary_id)
