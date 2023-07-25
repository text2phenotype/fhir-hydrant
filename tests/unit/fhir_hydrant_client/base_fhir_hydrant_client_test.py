import json

import requests

from tests.test_case import TestCase
from unittest.mock import patch

from requests import Response

from fhirhydrant.fhir_client.utils.fhir_hydrant_client import FhirHydrantClient
from fhirhydrant.fhir_client.fhir_client_env import FhirClientEnv


class FhirHydrantClientTest(TestCase):
    fhir_hydrant_client = FhirHydrantClient()
    test_data = 'sample text'
    base_url = f'{FhirClientEnv.API_BASE.value}/api/v1/'

    def setUp(self):
        super().setUp()
        self.request_mock_patcher = patch('fhirhydrant.fhir_client.utils.fhir_hydrant_client.requests')
        self.request_mock = self.request_mock_patcher.start()
        self.request_mock.post.side_effect = self.post_mock_response
        self.request_mock.get.side_effect = self.get_mock_response
        self.request_mock.delete.side_effect = self.delete_mock_response
        self.request_mock.patch.side_effect = self.patch_mock_response

    def tearDown(self):
        super().tearDown()
        self.request_mock_patcher.stop()

    def post_mock_response(self, url, data=None, **kwargs):
        response = Response()

        response_data = {
            'url': url,
            'data': data
        }
        response._content = json.dumps(response_data).encode('utf-8')
        return response

    def get_mock_response(self, url, **kwargs):
        response = Response()

        response_data = {
            'url': url
        }
        response._content = json.dumps(response_data).encode('utf-8')
        return response

    def delete_mock_response(self, url, **kwargs):
        response = Response()
        response.status_code = requests.codes.NO_CONTENT
        return response

    def patch_mock_response(self, url, **kwargs):
        response = Response()

        response_data = {
            'url': url
        }
        response._content = json.dumps(response_data).encode('utf-8')
        return response
