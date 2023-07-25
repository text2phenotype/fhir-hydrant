from tests.unit.fhir_hydrant_client.base_fhir_hydrant_client_test import FhirHydrantClientTest


class ClinicalTextTest(FhirHydrantClientTest):

    def test_clinical_summary(self):
        response = self.fhir_hydrant_client.post_clinical_summary(self.test_data)
        self.verify_response(response, 'clinical_summary')

    def test_clinical_identification(self):
        response = self.fhir_hydrant_client.post_de_identification(self.test_data)
        self.verify_response(response, 'de_identification')

    def test_demographics(self):
        response = self.fhir_hydrant_client.post_demographics(self.test_data)
        self.verify_response(response, 'demographics')

    def verify_response(self, response, endpoint: str):
        url = response.get('url')
        data = response.get('data')
        expected_url = f'{self.base_url}{endpoint}/'

        self.assertEqual(url, expected_url)
        self.assertEqual(data, self.test_data)
