import os

from fhir.resources.binary import Binary
from fhir.resources.documentreference import DocumentReference
from fhir.resources.patient import Patient
from fhir.resources.provenance import Provenance

from fhirhydrant.fhir_server.app.api.resources.clinical_text.demographics import DemographicsResource
from fhirhydrant.fhir_server.app.utils.document_reference_linker import (get_document_reference_by_provenance_id,
                                                                         get_binary_id_by_document_reference_id)
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv
from tests.intergration.test_case import IntegrationTestCase


class DemographicsTest(IntegrationTestCase):
    TEST_FILE = 'john_stevens/john-stevens.txt'

    def setUp(self) -> None:
        super(DemographicsTest, self).setUp()
        self.url = self.url_for(DemographicsResource)
        self.document_reference_resource = MetaResource(DocumentReference)
        self.patient_resource = MetaResource(Patient)
        self.binary_resource = MetaResource(Binary)
        self.provenance_resource = MetaResource(Provenance)
        self._references_to_cleanup = []

    def test_post(self) -> None:
        test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
        test_file_path = os.path.join(test_data_folder, self.TEST_FILE)

        with open(test_file_path, 'r') as fp:
            test_data = fp.read()

        response = self.client.post(self.url, data=test_data, headers={'tenantId': FhirServerEnv.TENANT_ID.value})
        self.check_test_client_response(response=response)

        provenance_id = response.json.get('provenance', {}).get('id', '')
        provenance = self.provenance_resource.get(provenance_id)
        self.assertIsNotNone(provenance)

        document_reference_id = response.json.get('document_reference', {}).get('id', '')
        document_reference = self.document_reference_resource.get(document_reference_id)
        self.assertIsNotNone(document_reference)

        _, patient_id = document_reference.get('subject', {}).get('reference', {}).split('/')
        self.assertIsNotNone(patient_id)
        patient = self.patient_resource.get(patient_id)
        self.assertIsNotNone(patient)

        binary_id = response.json.get('binary', {}).get('id', '')
        binary = self.binary_resource.get(binary_id)
        self.assertIsNotNone(binary)

        self._references_to_cleanup.append(provenance_id)

    def tearDown(self) -> None:
        for provenance_id in self._references_to_cleanup:
            document_reference_id = get_document_reference_by_provenance_id(provenance_id)
            binary_id = get_binary_id_by_document_reference_id(document_reference_id)

            document_reference = self.document_reference_resource.get(document_reference_id)
            _, patient_id = document_reference.get('subject', {}).get('reference', '/').split('/')

            self.patient_resource.delete(patient_id)
            self.binary_resource.delete(binary_id)
            self.document_reference_resource.delete(document_reference_id)
            self.provenance_resource.delete(provenance_id)
