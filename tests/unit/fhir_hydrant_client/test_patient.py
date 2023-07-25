import uuid
import requests
from tests.unit.fhir_hydrant_client.base_fhir_hydrant_client_test import FhirHydrantClientTest


class PatientTest(FhirHydrantClientTest):
    def test_post_patient(self):
        response = self.fhir_hydrant_client.post_patient({})
        url = response.get('url')
        expected_url = f'{self.base_url}patient/'

        self.assertEqual(url, expected_url)

    def test_get_patient(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.get_patient(id)
        url = response.get('url')
        expected_url = f'{self.base_url}patient/{id}'

        self.assertEqual(url, expected_url)

    def test_delete_patient(self):
        id = uuid.uuid4()
        response = self.fhir_hydrant_client.delete_patient(id)
        self.assertEqual(response[0], 'deleted')
        self.assertEqual(response[1], requests.codes.NO_CONTENT)
