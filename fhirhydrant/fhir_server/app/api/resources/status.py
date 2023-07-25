import requests
from flask_apispec import MethodResource, doc

from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv


@doc(tags=['Status'])
class StatusResource(MethodResource):
    @doc(description="Check state of connection to FHIR API")
    def get(self):
        base_url = FhirServerEnv.API_URL.value
        response = requests.get('{}{}'.format(base_url, 'metadata'))
        if response.status_code == 200:
            return True
        else:
            return False
