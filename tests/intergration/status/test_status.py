from fhirhydrant.fhir_server.app.api.resources.status import StatusResource
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv
from tests.intergration.test_case import IntegrationTestCase


class StatusTest(IntegrationTestCase):

    def setUp(self) -> None:
        super(StatusTest, self).setUp()
        self.url = self.url_for(StatusResource)

    def test_get(self):
        response = self.client.get(self.url, headers={'tenantId': FhirServerEnv.TENANT_ID.value})
        self.assertIn(b'true', response.data)
