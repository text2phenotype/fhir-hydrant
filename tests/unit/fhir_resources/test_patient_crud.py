import json
import os
import requests

from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhir.resources.patient import Patient
from tests.unit.fhir_resources.base_fhir_resource_test import BaseFhirResourceTest


class PatientCrudTest(BaseFhirResourceTest):
    TEST_FAMILY = 'Vaughan'
    TEST_NAME = 'David'
    TEST_BOD = '1940-07-18'

    def test_crud_patient(self):
        patient_resource = MetaResource(Patient)

        test_file = 'fhir_resources/patient.json'
        file_name = os.path.join(getattr(self.config, 'TEST_DATA_FOLDER'), test_file)

        with open(file_name) as fp:
            data = fp.read()
            created_patient = patient_resource.create(Patient(json.loads(data)))

        identifier = created_patient['id']
        patient = patient_resource.get(identifier)

        self.assertEqual(created_patient, patient)
        patient.__delitem__('id')
        patient.__delitem__('meta')

        data = json.loads(data)

        # patch patient example https://www.hl7.org/fhir/patient-example.json.html
        contact_name_dict = data.get('contact')[0].get('name')
        del contact_name_dict['_family']
        del data['_birthDate']

        self.assertEqual(patient, data)

        created_patient['name'][0]['family'] = self.TEST_FAMILY
        created_patient['name'][0]['given'][0] = self.TEST_NAME
        created_patient['birthDate'] = self.TEST_BOD
        updated_patient = patient_resource.update(identifier, Patient(created_patient))

        self.assertEqual(updated_patient['name'][0]['family'], self.TEST_FAMILY)
        self.assertEqual(updated_patient['name'][0]['given'][0], self.TEST_NAME)
        self.assertEqual(updated_patient['birthDate'], self.TEST_BOD)

        patient_resource.delete(identifier)
        with self.assertRaises(requests.exceptions.HTTPError) as error:
            patient_resource.get(identifier)
        self.assertEqual(410, error.exception.response.status_code)
