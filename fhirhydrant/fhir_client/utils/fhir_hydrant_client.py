import requests
from enum import Enum
from fhir.resources.organization import Organization

from fhirhydrant.fhir_client.fhir_client_env import FhirClientEnv


class FHIREndpoint(Enum):
    clinical_summary = 0,
    de_identification = 1,
    demographics = 2,
    document = 3,
    document_reference = 4,
    organization = 5,
    patient = 6,
    provenance = 7,
    status = 8


class FhirHydrantClient:
    ENDPOINT = '/api/v1/{}/'

    def __init__(self):
        self.api_base = FhirClientEnv.API_BASE.value
        self.tenant_id = FhirClientEnv.TENANT_ID.value
        self.headers = {'tenantId': self.tenant_id}

    # Clinical Text endpoints
    def post_clinical_summary(self, clinical_text: str):
        response = self._send_text(clinical_text, FHIREndpoint.clinical_summary)
        return response.json()

    def post_de_identification(self, clinical_text: str):
        response = self._send_text(clinical_text, FHIREndpoint.de_identification)
        return response.json()

    def post_demographics(self, clinical_text: str):
        response = self._send_text(clinical_text, FHIREndpoint.demographics)
        return response.json()

    # Document endpoint
    def post_document(self, clinical_text: str):
        response = self._send_text(clinical_text, FHIREndpoint.document)
        return response.json()

    def get_documents(self):
        response = self._get_all_resources(FHIREndpoint.document)
        return response.json()

    def get_document(self, document_id: str):
        response = self._get_resource(document_id, FHIREndpoint.document)
        return response.json()

    def delete_document(self, document_id: str):
        response = self._delete_resource(document_id, FHIREndpoint.document)
        return 'deleted', response.status_code

    # Document Reference endpoint
    def post_document_reference(self, document_reference: dict):
        response = self._send_resource(document_reference, FHIREndpoint.document_reference)
        return response.json()

    def get_document_reference(self, document_reference_id: str):
        response = self._get_resource(document_reference_id, FHIREndpoint.document_reference)
        return response.json()

    def delete_document_reference(self, document_reference_id: str):
        response = self._delete_resource(document_reference_id, FHIREndpoint.document_reference)
        return 'deleted', response.status_code

    # Organization endpoint
    def post_organization(self, organization: dict):
        response = self._send_resource(organization, FHIREndpoint.organization)
        return response.json()

    def get_organizations(self):
        response = self._get_all_resources(FHIREndpoint.organization)
        return response.json()

    def get_organization(self, organization_id: str):
        response = self._get_resource(organization_id, FHIREndpoint.organization)
        return response.json()

    def patch_organization(self, organization: Organization):
        response = self._patch_resource(organization, FHIREndpoint.organization)
        return response.json()

    def delete_organization(self, organization_id: str):
        response = self._delete_resource(organization_id, FHIREndpoint.organization)
        return 'deleted', response.status_code

    # Patient endpoint
    def post_patient(self, patient: dict):
        response = self._send_resource(patient, FHIREndpoint.patient)
        return response.json()

    def get_patient(self, patient_id: str):
        response = self._get_resource(patient_id, FHIREndpoint.patient)
        return response.json()

    def delete_patient(self, patient_id: str):
        response = self._delete_resource(patient_id, FHIREndpoint.patient)
        return 'deleted', response.status_code

    # Provenance endpoint
    def post_provenance(self, provenance: dict):
        response = self._send_resource(provenance, FHIREndpoint.provenance)
        return response.json()

    def get_provenance(self, provenance_id: str):
        response = self._get_resource(provenance_id, FHIREndpoint.provenance)
        return response.json()

    def delete_provenance(self, provenance_id: str):
        response = self._delete_resource(provenance_id, FHIREndpoint.provenance)
        return 'deleted', response.status_code

    # Common methods
    def _send_text(self, resource_object, endpoint: FHIREndpoint):
        url = '{}{}'.format(self.api_base, self.ENDPOINT.format(endpoint.name))
        return requests.post(url, data=resource_object, headers=self.headers)

    def _send_resource(self, resource_object, endpoint: FHIREndpoint):
        url = '{}{}'.format(self.api_base, self.ENDPOINT.format(endpoint.name))
        return requests.post(url, json=resource_object, headers=self.headers)

    def _get_resource(self, identifier, endpoint: FHIREndpoint):
        url = '{}{}{}'.format(self.api_base, self.ENDPOINT.format(endpoint.name), identifier)
        return requests.get(url, headers=self.headers)

    def _get_all_resources(self, endpoint: FHIREndpoint):
        url = '{}{}'.format(self.api_base, self.ENDPOINT.format(endpoint.name))
        return requests.get(url, headers=self.headers)

    def _patch_resource(self, resource_object, endpoint: FHIREndpoint):
        url = '{}{}'.format(self.api_base, self.ENDPOINT.format(endpoint.name))
        return requests.patch(url, data=resource_object, headers=self.headers)

    def _delete_resource(self, identifier, endpoint: FHIREndpoint):
        url = '{}{}{}'.format(self.api_base, self.ENDPOINT.format(endpoint.name), identifier)
        return requests.delete(url, headers=self.headers)

    def check_connection(self) -> bool:
        try:
            requests.get(self.api_base)
            check_connection_url = '{}{}'.format(self.api_base, self.ENDPOINT.format(FHIREndpoint.status.name))
            response = requests.get(check_connection_url)

            return True if 'true' in response.text else False
        except:
            return False
