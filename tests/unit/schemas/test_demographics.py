import json
from marshmallow import ValidationError

from fhirhydrant.fhir_server.app.api.schemas.demographics import DemographicsSchema
from tests.test_case import TestCase


class DemographicsSchemaTest(TestCase):

    def test_validation(self):
        for test_file in self.demographics_test_files.values():
            with open(test_file) as fp:
                data = json.load(fp)
                DemographicsSchema().load(data)

    def test_validation_invalid(self):
        with self.assertRaises(ValidationError):
            DemographicsSchema().load({'invalid': 'field'})
