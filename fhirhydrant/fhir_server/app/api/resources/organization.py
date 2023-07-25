from typing import Optional

from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id

from fhirhydrant.fhir_server.app.utils.schemas.generator import resource_to_schema

from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from requests.exceptions import HTTPError

from flask import abort, request
from flask_apispec import MethodResource, doc, marshal_with

from fhir.resources.fhirabstractbase import FHIRValidationError
from fhir.resources.organization import Organization


@doc(tags=['Organization'])
class OrganizationResource(MethodResource):

    organization_resource = MetaResource(Organization)
    organization_schema = resource_to_schema(Organization)

    @doc(
        description='Allows create Organization from json representation',
        parameters=[
            {
                'in': 'body',
                'name': 'organization',
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
    @marshal_with(organization_schema, 201)
    @marshal_with(None, code=422, description="Validation error occurred")
    def post(self):

        organization_json = request.get_json()

        try:
            new_organization = Organization(organization_json)
            created_organization = Organization(self.organization_resource.create(new_organization))
            return created_organization, 201

        except FHIRValidationError:
            abort(422)
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        params={
            'organization_id': {
                'description': 'Organization ID',
                'required': False
            }
        },
        description="Returns single instance or list of Organization object"
    )
    @check_tenant_id
    def get(self, organization_id: Optional[str] = None):
        try:
            if organization_id is None:
                return self.organization_resource.get_all().get('entry') or dict(), 200
            else:
                result = self.organization_resource.get(organization_id)
                return result, 200

        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        description="Update single instance of Organization object",
        parameters=[
            {
                'in': 'body',
                'name': 'organization',
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
    @marshal_with(organization_schema, 200)
    def patch(self):
        organization_dict = request.get_json()

        if 'id' not in organization_dict.keys():
            abort(400)

        try:
            patched_organization = Organization(request.get_json())
            organization_id = patched_organization.id
            updated_resource = Organization(self.organization_resource.update(organization_id, patched_organization))
            return updated_resource, 200

        except FHIRValidationError:
            abort(422)
        except HTTPError as e:
            abort(e.response.status_code)

    @doc(
        params={
            'organization_id': {
                'description': 'Organization ID ',
                'required': True
            }
        },
        description="Deletes instance of Organization object"
    )
    @check_tenant_id
    def delete(self, organization_id: str):
        deleted = self.organization_resource.delete(organization_id)
        if deleted:
            return None, 204
        else:
            abort(500)
