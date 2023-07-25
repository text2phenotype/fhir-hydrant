from typing import Union, Dict
import requests
import json
from urllib.parse import urlencode, urljoin

from text2phenotype.common.singleton import singleton

from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv


@singleton
class AzureFHIRClient:
    __ACCESS_TOKEN = ''
    __REFRESH_TOKEN = ''
    @property
    def access_token(self) -> str:
        return self.__class__.__ACCESS_TOKEN

    @access_token.setter
    def access_token(self, value: str) -> None:
        self.__class__.__ACCESS_TOKEN = value

    @property
    def refresh_token(self) -> str:
        return self.__class__.__REFRESH_TOKEN

    @refresh_token.setter
    def refresh_token(self, value: str) -> None:
        self.__class__.__REFRESH_TOKEN = value

    def make_request(self, method: str, path: str, data=None) -> Union[bool, Dict, int]:
        headers = {
            'Content-type': 'application/fhir+json',
            'Accept': 'application/fhir+json',
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

        method_handle = {
            'POST': requests.post,
            'GET': requests.get,
            'DELETE': requests.delete,
            'UPDATE': requests.put
        }[method]

        url: str = urljoin(FhirServerEnv.API_URL.value, path)
        response = method_handle(url, headers=headers, data=data)

        if response.status_code in [201, 200]:
            data = json.loads(response.text)
            return data
        elif response.status_code == 204:
            return True
        elif response.status_code == 401:
            if self.refresh_token:
                self.refresh_tokens()
            else:
                self.authorize()
            return self.make_request(method, path, data)
        else:
            response.raise_for_status()

    def authorize(self) -> None:
        data_dict = {
            "grant_type": "password",
            "client_id": FhirServerEnv.CLIENT_ID.value,
            "client_secret": FhirServerEnv.CLIENT_SECRET.value,
            'redirect_uri': FhirServerEnv.REDIRECT_URI.value,
            'username': FhirServerEnv.AZURE_USERNAME.value,
            'password': FhirServerEnv.PASSWORD.value,
            'scope': FhirServerEnv.SCOPE.value
        }
        self.send_authorization(data_dict)

    def refresh_tokens(self) -> None:
        data_dict = {
            'grant_type': 'refresh_token',
            'client_id': FhirServerEnv.CLIENT_ID.value,
            'client_secret': FhirServerEnv.CLIENT_SECRET.value,
            'refresh_token': self.refresh_token
        }

        self.send_authorization(data_dict)

    def send_authorization(self, data_dict) -> None:
        url = '{}{}/oauth2/v2.0/token'.format(FhirServerEnv.AUTH_BASE_URL.value, FhirServerEnv.TENANT_ID.value)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        body = urlencode(data_dict)

        response = requests.post(url, headers=headers, data=body)

        if response.status_code == 200:
            response_body = json.loads(response.text)
            self.access_token = response_body['access_token']
            self.refresh_token = response_body['refresh_token']
        else:
            response.raise_for_status()
