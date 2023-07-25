import json
import os

from fhir.resources.documentreference import DocumentReference

from fhirhydrant.fhir_server.app.api.resources.document_reference import DocumentReferenceResource
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv
from tests.intergration.test_case import IntegrationTestCase


class DocumentReferenceTest(IntegrationTestCase):
    TEST_FILE = 'fhir_resources/document_reference.json'

    def setUp(self) -> None:
        super().setUp()
        self.url = self.url_for(DocumentReferenceResource)
        self.document_reference_resource = MetaResource(DocumentReference)

        self._test_document_references = []

        self.test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
        self.test_file_path = os.path.join(self.test_data_folder, self.TEST_FILE)

        self.headers = {
            'Content-Type': 'application/json',
            'tenantId': FhirServerEnv.TENANT_ID.value
        }

    def test_post_get(self):
        with open(self.test_file_path, 'r') as f:
            test_data = json.load(f)

        response = self.client.post(self.url, json=test_data, headers=self.headers)
        self.check_test_client_response(response=response)

        document_reference_id = response.json.get('id')
        document_reference = self.document_reference_resource.get(document_reference_id)

        self.assertIsNotNone(document_reference)
        self.assertEqual(document_reference_id, document_reference['id'])
        document_reference.pop('id', None)
        document_reference.pop('meta', None)

        self.assertEqual(test_data, document_reference)

        self._test_document_references.append(document_reference_id)

    def test_post_delete(self) -> None:
        with open(self.test_file_path, 'r') as f:
            test_data = json.load(f)

        response = self.client.post(self.url, json=test_data, headers=self.headers)

        self.assertEqual(response.status_code, 201)
        document_reference_id = response.json.get('id')
        response_before_delete = self.client.get(self.url + document_reference_id, headers=self.headers)

        self.assertEqual(response_before_delete.status_code, 200)

        response_deleted = self.client.delete(self.url + document_reference_id, headers=self.headers)
        self.assertEqual(response_deleted.status_code, 204)

        after_delete = self.client.get(self.url + document_reference_id, headers=self.headers)
        self.assertEqual(410, after_delete.status_code)

    def tearDown(self) -> None:
        for document_reference in self._test_document_references:
            self.document_reference_resource.delete(document_reference)
