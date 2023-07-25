import json
import requests
import os
from os import path

from fhir.resources.patient import Patient

from text2phenotype.common.demographics import Demographics

from fhirhydrant.fhir_client.utils.converter.patient import PatientConverter
from fhirhydrant.fhir_server.app.api.resources.patient import PatientResource
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv
from tests.intergration.test_case import IntegrationTestCase


class PatientTest(IntegrationTestCase):

    def setUp(self):
        super(PatientTest, self).setUp()
        self.url = self.url_for(PatientResource)

        self.headers = {
            'Content-Type': 'application/json',
            'tenantId': FhirServerEnv.TENANT_ID.value
        }

    def test_demographics_post(self):
        for test_file in self.demographics_test_files.values():
            with open(test_file) as fp:
                data = json.load(fp)
                response = self.client.post(self.url, json=data, headers=self.headers)
                self.assertIn(response.status_code, [200, 201])

                created_patient = response.json
                identifier = created_patient['id']
                patient_resource = MetaResource(Patient)

                patient = patient_resource.get(identifier)
                self.assertEqual(patient, created_patient)

                patient_resource.delete(identifier)

                with self.assertRaises(requests.exceptions.HTTPError) as error:
                    patient_resource.get(identifier)
                self.assertEqual(410, error.exception.response.status_code)

    def test_patient_post(self):
        test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
        test_file_path = os.path.join(test_data_folder, 'fhir_resources/patient.json')
        with open(test_file_path) as fp:
            data = json.load(fp)
            response = self.client.post(self.url, json=data, headers=self.headers)
            self.assertIn(response.status_code, [200, 201])

            created_patient = response.json
            identifier = created_patient['id']
            patient_resource = MetaResource(Patient)

            patient = patient_resource.get(identifier)
            self.assertEqual(patient, created_patient)

            patient_resource.delete(identifier)

            with self.assertRaises(requests.exceptions.HTTPError) as error:
                patient_resource.get(identifier)
            self.assertEqual(410, error.exception.response.status_code)

    def test_post_get(self):
        for test_file in self.demographics_test_files.values():
            with open(test_file) as fp:
                data = json.load(fp)

                response = self.client.post(self.url, json=data, headers=self.headers)
                self.assertIn(response.status_code, [200, 201])

                created_patient = response.json
                identifier = created_patient['id']
                response = self.client.get('{}{}'.format(self.url, identifier), headers=self.headers)
                self.assertEqual(response.status_code, 200)

                patient_json = response.json

                init_demographics = Demographics(**data)
                demographics = PatientConverter.from_fhir(patient_json)

                demographics.dob = [[demographics.dob[0][0].strftime("%-m/%-d/%Y"), 1]]
                self.assert_patients_are_equal(init_demographics, demographics, path.basename(fp.name))

                patient_resource = MetaResource(Patient)
                patient_resource.delete(identifier)

                with self.assertRaises(requests.exceptions.HTTPError) as error:
                    patient_resource.get(identifier)
                self.assertEqual(410, error.exception.response.status_code)
