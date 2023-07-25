from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id
from fhirhydrant.fhir_server.app.utils.schemas.generator import resource_to_schema

from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from flask import abort, request
from flask_apispec import MethodResource, doc, marshal_with
from requests.exceptions import HTTPError

from typing import Optional

from fhir.resources.fhirabstractbase import FHIRValidationError
from fhir.resources.provenance import Provenance


@doc(tags=['Provenance'])
class ProvenanceResource(MethodResource):
    provenance_resource = MetaResource(Provenance)
    provenance_schema = resource_to_schema(Provenance)

    @doc(
        description='Allows create Provenance from json representation',
        parameters=[
                     {
                         'in': 'body',
                         'name': 'provenance',
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
    @marshal_with(provenance_schema, 201)
    def post(self):
        provenance_json = request.get_json()
        try:
            provenance = Provenance(provenance_json)
            created_provenance = self.provenance_resource.create(provenance)
            response = Provenance(created_provenance)
            return response, 201
        except FHIRValidationError:
            abort(422)
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        params={
            'provenance_id': {
                'description': 'Provenance ID'
            }
        },
        description="Returns single instance of Provenance object as FHIR json"
    )
    @check_tenant_id
    @marshal_with(provenance_schema, 200)
    def get(self, provenance_id: Optional[str]):
        try:
            provenance = self.provenance_resource.get(provenance_id)
            return Provenance(provenance), 200
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        params={
            'provenance_id': {
                'description': 'Provenance ID',
            }
        },
        description="Deletes instance of Provenance object"
    )
    @check_tenant_id
    def delete(self, provenance_id: str):
        deleted = self.provenance_resource.delete(provenance_id)
        if deleted:
            return None, 204
        else:
            abort(500)
