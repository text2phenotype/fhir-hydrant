import json

from tests.unit.fhir_hydrant_client.base_fhir_hydrant_client_test import FhirHydrantClientTest
from requests import Response


class CheckConnectionClass(FhirHydrantClientTest):

    def get_mock_response_true(self, url, **kwargs):
        response = Response()

        response_data = True
        response._content = json.dumps(response_data).encode('utf-8')
        return response

    def get_mock_response_false(self, url, **kwargs):
        response = Response()
        response._content = False
        return response

    def get_mock_response_exception(self, url, **kwargs):
        response = Response()

        response._content = 'False'
        return response

    def test_check_connection_true(self):
        self.request_mock.get.side_effect = self.get_mock_response_true
        response = self.fhir_hydrant_client.check_connection()
        self.assertTrue(response)

    def test_check_connection_false(self):
        self.request_mock.get.side_effect = self.get_mock_response_false
        response = self.fhir_hydrant_client.check_connection()
        self.assertFalse(response)

    def test_check_connection_exception(self):
        self.request_mock.get.side_effect = self.get_mock_response_exception
        response = self.fhir_hydrant_client.check_connection()
        self.assertFalse(response)
