import os

from fhir.resources.binary import Binary
from fhir.resources.documentreference import DocumentReference
from fhir.resources.provenance import Provenance

from fhirhydrant.fhir_server.app.api.resources.document import DocumentResource
from fhirhydrant.fhir_server.app.utils.document_reference_linker import (get_document_reference_by_provenance_id,
                                                                         get_binary_id_by_document_reference_id)
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_client.fhir_client_env import FhirClientEnv
from tests.intergration.test_case import IntegrationTestCase


class DocumentTest(IntegrationTestCase):
    TEST_FILE = 'john_stevens/john-stevens.txt'

    def setUp(self) -> None:
        super(DocumentTest, self).setUp()
        self.url = self.url_for(DocumentResource)
        self.document_reference_resource = MetaResource(DocumentReference)
        self.binary_resource = MetaResource(Binary)
        self.provenance_resource = MetaResource(Provenance)
        self._references_to_cleanup = []
        self.headers = {'tenantId': FhirClientEnv.TENANT_ID.value}

    def test_post(self):
        test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
        test_file_path = os.path.join(test_data_folder, self.TEST_FILE)

        with open(test_file_path, 'r') as fp:
            test_data = fp.read()

        response = self.client.post(self.url, data=test_data, headers=self.headers)
        self.check_test_client_response(response=response)

        provenance_id = response.json.get('provenance', {}).get('id', '')
        provenance = self.provenance_resource.get(provenance_id)
        self.assertIsNotNone(provenance)

        document_reference_id = response.json.get('document_reference', {}).get('id', '')
        document_reference = self.document_reference_resource.get(document_reference_id)
        self.assertIsNotNone(document_reference)

        binary_id = response.json.get('binary', {}).get('id', '')
        binary = self.binary_resource.get(binary_id)
        self.assertIsNotNone(binary)

        document = self.binary_resource.get(binary_id)
        self.assertIsNotNone(document)

        self._references_to_cleanup.append(provenance_id)

    def test_post_get(self):
        test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
        test_file_path = os.path.join(test_data_folder, self.TEST_FILE)

        with open(test_file_path, 'r') as fp:
            test_data = fp.read()

        response = self.client.post(self.url, data=test_data, headers=self.headers)
        self.assertEqual(201, response.status_code)

        document_id = response.json.get('document_reference', {}).get('id', '')
        provenance_id = response.json.get('provenance', {}).get('id', '')

        response = self.client.get('{}{}'.format(self.url, document_id), headers=self.headers)
        self.assertEqual(response.status_code, 200)

        content = response.json.get('content')

        self.assertEqual(content, test_data)
        self._references_to_cleanup.append(provenance_id)

    def test_post_delete(self):
        test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
        test_file_path = os.path.join(test_data_folder, self.TEST_FILE)

        with open(test_file_path, 'r') as fp:
            test_data = fp.read()

        response = self.client.post(self.url, data=test_data, headers=self.headers)
        self.assertEqual(201, response.status_code)

        provenance_id = response.json.get('provenance', {}).get('id', '')
        response = self.client.delete('{}{}'.format(self.url, provenance_id), headers=self.headers)
        self.assertEqual(response.status_code, 200)

        provenances = self.client.get(self.url, headers=self.headers).json

        for provenance in provenances:
            resource = provenance.get('resource')
            self.assertNotEqual(resource.get('id'), provenance_id)

    def tearDown(self) -> None:
        for provenance_id in self._references_to_cleanup:
            document_reference_id = get_document_reference_by_provenance_id(provenance_id)
            binary_id = get_binary_id_by_document_reference_id(document_reference_id)
            self.binary_resource.delete(binary_id)
            self.document_reference_resource.delete(document_reference_id)
            self.provenance_resource.delete(provenance_id)
