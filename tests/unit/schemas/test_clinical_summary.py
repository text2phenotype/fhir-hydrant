import json
from pathlib import Path

from marshmallow import ValidationError

from fhirhydrant.fhir_server.app.api.schemas.clinical_summary import ClinicalSummarySchema
from tests.test_case import TestCase


class ClinicalSummarySchemaTest(TestCase):

    def test_validation(self):
        test_data_folder = Path(getattr(self.config, 'TEST_DATA_FOLDER')).resolve()
        self.assertTrue(test_data_folder.exists())
        self.assertTrue(test_data_folder.is_dir())
        for test_file in test_data_folder.glob("**/*.summary.json"):
            with open(test_file) as fp:
                data = json.load(fp)
                ClinicalSummarySchema().load(data)

    def test_validation_invalid(self):
        with self.assertRaises(ValidationError):
            ClinicalSummarySchema().load({'invalid': 'field'})
