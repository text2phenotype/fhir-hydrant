from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv

from tests.test_case import TestCase


class BaseFhirResourceTest(TestCase):
    def setUp(self) -> None:
        FhirServerEnv.refresh()
        return super().setUp()
