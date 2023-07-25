import json

from fhir.resources.fhirabstractresource import FHIRAbstractResource

from fhirhydrant.fhir_server.app.utils.fhir_client import AzureFHIRClient


class FHIRResource:

    def __init__(self, resource_type: str):
        self.resource_type = resource_type
        self.__fhir_client = AzureFHIRClient()

    def create(self, resource_object: FHIRAbstractResource):
        path = self.resource_type
        resource_data = json.dumps(resource_object.as_json())
        return self.__fhir_client.make_request('POST', path, data=resource_data)

    def get(self, identifier: str):
        path = '{}/{}'.format(self.resource_type, identifier)
        return self.__fhir_client.make_request('GET', path)

    def delete(self, identifier: str):
        path = '{}/{}'.format(self.resource_type, identifier)
        return self.__fhir_client.make_request('DELETE', path)

    def update(self, identifier: str, resource_object: FHIRAbstractResource):
        path = '{}/{}'.format(self.resource_type, identifier)
        resource_data = json.dumps(resource_object.as_json())
        return self.__fhir_client.make_request('UPDATE', path, data=resource_data)

    def get_all(self):
        path = self.resource_type
        return self.__fhir_client.make_request('GET', path)
