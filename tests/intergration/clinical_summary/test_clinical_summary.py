from pathlib import Path

from fhir.resources.bundle import Bundle
from fhir.resources.condition import Condition
from fhir.resources.patient import Patient

from fhirhydrant.fhir_server.app.api.resources.clinical_text.clinical_summary import ClinicalSummaryResource
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_client.fhir_client_env import FhirClientEnv
from tests.intergration.test_case import IntegrationTestCase


class ClinicalSummaryTest(IntegrationTestCase):

    def setUp(self) -> None:
        super(ClinicalSummaryTest, self).setUp()
        self.url = self.url_for(ClinicalSummaryResource)
        self.patient_resource = MetaResource(Patient)
        self.patient_ref = 'patient'
        self.bundles_to_cleanup = []
        self.patients_to_cleanup = []
        self.headers = {
            'Content-Type': 'application/json',
            'tenantId': FhirClientEnv.TENANT_ID.value
        }

    def test_post(self) -> None:
        test_data_folder = Path(getattr(self.config, 'TEST_DATA_FOLDER')).resolve()
        self.assertTrue(test_data_folder.exists())
        self.assertTrue(test_data_folder.is_dir())
        for file_name in test_data_folder.glob("**/*.txt"):
            self.assertTrue(file_name.is_file())
            with open(file_name, 'r') as fp:
                data = fp.read()

            response = self.client.post(self.url, data=data, headers=self.headers)
            self.check_test_client_response(response=response, additional_data=file_name)
            bundle_id = response.json.get('bundle_id', '')
            self.assertIsNotNone(bundle_id)

            condition = Condition(response.json.get('conditions', {})[0])
            _, patient_id = condition.subject.reference.split('/')
            self.assertIsNotNone(patient_id)
            patient = self.patient_resource.get(patient_id)
            self.assertIsNotNone(patient)

            for condition_dict in response.json.get('conditions', {}):
                condition = Condition(condition_dict)
                for extension in condition.extension:
                    for annotation_extension in extension.valueAnnotation.extension:
                        if annotation_extension.valueRange:
                            high = annotation_extension.valueRange.high.value
                            low = annotation_extension.valueRange.low.value
                            annotation_text = extension.valueAnnotation.text
                            self.assertEqual(len(annotation_text), high - low)
                        else:
                            self.assertEqual(extension.valueAnnotation.text, 'polarity')

            self.bundles_to_cleanup.append(bundle_id)
            self.patients_to_cleanup.append(patient_id)

    def tearDown(self) -> None:
        resource = MetaResource(Bundle)
        for bundle_id in self.bundles_to_cleanup:
            resource.delete(bundle_id)

        resource = MetaResource(Patient)
        for patient_id in self.patients_to_cleanup:
            resource.delete(patient_id)
