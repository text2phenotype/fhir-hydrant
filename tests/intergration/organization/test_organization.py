import os
import json

from fhir.resources.organization import Organization

from fhirhydrant.fhir_server.app.api.resources.organization import OrganizationResource
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv
from tests.intergration.test_case import IntegrationTestCase


class OrganizationTest(IntegrationTestCase):
    TEST_FILE = 'fhir_resources/organization.json'

    def setUp(self) -> None:
        super().setUp()
        self.url = self.url_for(OrganizationResource)
        self.organization_resource = MetaResource(Organization)
        self._test_organizations = []

        self.test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
        self.test_file_path = os.path.join(self.test_data_folder, self.TEST_FILE)

        self.headers = {
            'Content-Type': 'application/json',
            'tenantId': FhirServerEnv.TENANT_ID.value
        }

    def test_post_get(self) -> None:

        with open(self.test_file_path, 'r') as f:
            test_data = json.load(f)

        response = self.client.post(self.url, json=test_data, headers=self.headers)
        self.check_test_client_response(response=response)

        organization_id = response.json.get('id')
        organization = self.organization_resource.get(organization_id)

        self.assertIsNotNone(organization)
        self.assertEqual(organization_id, organization['id'])
        organization.pop('id', None)
        organization.pop('meta', None)
        self.assertEqual(test_data, organization)

        self._test_organizations.append(organization_id)

    def test_post_delete(self) -> None:
        with open(self.test_file_path, 'r') as f:
            test_data = json.load(f)

        response = self.client.post(self.url, json=test_data, headers=self.headers)

        organization_id = response.json.get('id')
        response_before_delete = self.client.get(self.url+organization_id, headers=self.headers)

        self.assertEqual(response_before_delete.status_code, 200)

        response_deleted = self.client.delete(self.url+organization_id, headers=self.headers)
        self.assertEqual(response_deleted.status_code, 204)

        after_delete = self.client.get(self.url+organization_id, headers=self.headers)
        self.assertEqual(410, after_delete.status_code)

    def test_post_update(self) -> None:
        with open(self.test_file_path, 'r') as f:
            test_data = json.load(f)

        response = self.client.post(self.url, json=test_data, headers=self.headers)

        organization_id = response.json.get('id')
        organization = self.organization_resource.get(organization_id)

        new_name = 'New Organization Name'
        organization['name'] = new_name

        self.client.patch(self.url, json=organization, headers=self.headers)

        organization_after_update = self.organization_resource.get(organization_id)
        self.assertEqual(new_name, organization_after_update['name'])

        self._test_organizations.append(organization_id)

    def tearDown(self) -> None:
        for organization in self._test_organizations:
            self.organization_resource.delete(organization)
