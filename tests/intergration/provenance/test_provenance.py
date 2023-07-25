import os
import json

from fhir.resources.provenance import Provenance

from fhirhydrant.fhir_server.app.api.resources.provenance import ProvenanceResource
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv
from tests.intergration.test_case import IntegrationTestCase


class ProvenanceTest(IntegrationTestCase):
    TEST_FILE = 'fhir_resources/provenance.json'

    def setUp(self) -> None:
        super().setUp()
        self.url = self.url_for(ProvenanceResource)
        self.provenance_resource = MetaResource(Provenance)
        self._provenances_to_cleanup = []

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

        provenance_id = response.json.get('id')
        provenance = self.provenance_resource.get(provenance_id)

        self.assertIsNotNone(provenance)
        provenance.pop('id', None)
        provenance.pop('meta', None)

        self.assertEqual(test_data, provenance)
        self._provenances_to_cleanup.append(provenance_id)

    def tearDown(self) -> None:
        for provenance in self._provenances_to_cleanup:
            self.provenance_resource.delete(provenance)
