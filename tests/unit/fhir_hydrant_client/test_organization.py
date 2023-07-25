import uuid
import requests
from fhir.resources.organization import Organization
from tests.unit.fhir_hydrant_client.base_fhir_hydrant_client_test import FhirHydrantClientTest


class OrganizationTest(FhirHydrantClientTest):
    def test_post_organization(self):
        response = self.fhir_hydrant_client.post_organization(self.test_data)
        url = response.get('url')
        expected_url = f'{self.base_url}organization/'

        self.assertEqual(url, expected_url)

    def test_get_organization(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.get_organization(id)
        url = response.get('url')
        expected_url = f'{self.base_url}organization/{id}'

        self.assertEqual(url, expected_url)

    def test_get_all_document(self):
        response = self.fhir_hydrant_client.get_organizations()
        url = response.get('url')
        expected_url = f'{self.base_url}organization/'

        self.assertEqual(url, expected_url)

    def test_patch_organization(self):
        response = self.fhir_hydrant_client.patch_organization(Organization())
        url = response.get('url')
        expected_url = f'{self.base_url}organization/'

        self.assertEqual(url, expected_url)

    def test_delete_organization(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.delete_organization(id)
        self.assertEqual(response[0], 'deleted')
        self.assertEqual(response[1], requests.codes.NO_CONTENT)
