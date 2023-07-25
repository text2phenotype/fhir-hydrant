import uuid
import requests
from tests.unit.fhir_hydrant_client.base_fhir_hydrant_client_test import FhirHydrantClientTest


class DocumentReferenceTest(FhirHydrantClientTest):

    def test_post_document(self):
        response = self.fhir_hydrant_client.post_document_reference(self.test_data)
        url = response.get('url')
        expected_url = f'{self.base_url}document_reference/'

        self.assertEqual(url, expected_url)

    def test_get_document(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.get_document_reference(id)
        url = response.get('url')
        expected_url = f'{self.base_url}document_reference/{id}'

        self.assertEqual(url, expected_url)

    def test_delete_document(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.delete_document_reference(id)
        self.assertEqual(response[0], 'deleted')
        self.assertEqual(response[1], requests.codes.NO_CONTENT)
