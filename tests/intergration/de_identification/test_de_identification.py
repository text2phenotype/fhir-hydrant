import json
import os

from fhir.resources.binary import Binary
from fhir.resources.documentreference import DocumentReference
from fhir.resources.provenance import Provenance

from fhirhydrant.fhir_server.app.api.resources.clinical_text.de_identification import DeIdentificationResource
from fhirhydrant.fhir_server.app.api.resources.document import DocumentResource
from fhirhydrant.fhir_server.app.utils.document_reference_linker import (get_document_reference_by_provenance_id,
                                                                         get_binary_id_by_document_reference_id)
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_client.fhir_client_env import FhirClientEnv
from tests.intergration.test_case import IntegrationTestCase


class DeIdentificationTest(IntegrationTestCase):
    TEST_FILE = 'john_stevens/john-stevens.txt'

    def setUp(self) -> None:
        super(DeIdentificationTest, self).setUp()
        self.url = self.url_for(DeIdentificationResource)
        self.document_url = self.url_for(DocumentResource)
        self.document_reference_resource = MetaResource(DocumentReference)
        self.provenance_resource = MetaResource(Provenance)
        self.binary_resource = MetaResource(Binary)
        self._references_to_cleanup = []
        self.headers = {'tenantId': FhirClientEnv.TENANT_ID.value}

    def test_post(self) -> None:
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

        self._references_to_cleanup.append(provenance_id)

    def test_simple_source_deid_comparison(self) -> None:
        source_text: str = "Patient John Smith was taken to hospital with suspected poisoning."
        expected_deid_text: str = "Patient **** ***** was taken to hospital with suspected poisoning."

        response = self.client.post(self.url, data=source_text, headers=self.headers)
        err_msg = "{}\n{}".format(response.json, json.dumps(response.status, indent=1))
        self.assertEqual(201, response.status_code, msg=err_msg)

        document_id = response.json.get('document_reference', {}).get('id', '')
        provenance_id = response.json.get('provenance', {}).get('id', '')

        document = self.document_reference_resource.get(document_id)
        self.assertIsNotNone(document)

        document_response = self.client.get(self.document_url + document_id, headers=self.headers)
        actual_deid_text = document_response.json.get('content')
        self.assertEqual(expected_deid_text, actual_deid_text)

        self._references_to_cleanup.append(provenance_id)

    def tearDown(self) -> None:
        for provenance_id in self._references_to_cleanup:
            document_reference_id = get_document_reference_by_provenance_id(provenance_id)
            binary_id = get_binary_id_by_document_reference_id(document_reference_id)

            self.binary_resource.delete(binary_id)
            self.document_reference_resource.delete(document_reference_id)
            self.provenance_resource.delete(provenance_id)
