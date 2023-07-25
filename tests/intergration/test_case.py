import json

from flask import Flask, url_for
from flask_apispec import MethodResource

from fhirhydrant.fhir_server.app.factory import create_app

from tests.intergration.test_client import JSONTestClient
from tests.test_case import TestCase


class IntegrationTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(IntegrationTestCase, self).__init__(*args, **kwargs)

        self.application: Flask = create_app()

        self.app_context = self.application.app_context()
        self.app_context.push()

        self.application.test_client_class = JSONTestClient
        self.client: JSONTestClient = self.application.test_client()

        self.maxDiff = None

    @staticmethod
    def url_for(resource_cls: MethodResource, **kwargs):
        """
        Returns url for the resource
        :param resource_cls: Resource which url we generate for
        :param kwargs: query params
        :return:
        """

        endpoint = resource_cls.__module__.replace('fhirhydrant.fhir_server.app.api.resources.', '').replace('clinical_text.', '').replace('_', '')
        endpoint = "fhir-api-v1.{endpoint}resource".format(endpoint=endpoint)

        return url_for(endpoint, **kwargs)

    def check_test_client_response(self, response, additional_data: str = ''):
        error_text = response.json if response.is_json else ''
        err_msg = "{}\n{}\n{}".format(error_text, additional_data, json.dumps(response.status, indent=1))
        self.assertEqual(response.status_code, 201, msg=err_msg)
