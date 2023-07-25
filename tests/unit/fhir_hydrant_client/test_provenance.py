import uuid
import requests
from tests.unit.fhir_hydrant_client.base_fhir_hydrant_client_test import FhirHydrantClientTest


class ProvenanceTest(FhirHydrantClientTest):
    def test_post_provenance(self):
        response = self.fhir_hydrant_client.post_provenance({})
        url = response.get('url')
        expected_url = f'{self.base_url}provenance/'

        self.assertEqual(url, expected_url)

    def test_get_provenance(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.get_provenance(id)
        url = response.get('url')
        expected_url = f'{self.base_url}provenance/{id}'

        self.assertEqual(url, expected_url)

    def test_delete_provenance(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.delete_provenance(id)
        self.assertEqual(response[0], 'deleted')
        self.assertEqual(response[1], requests.codes.NO_CONTENT)
