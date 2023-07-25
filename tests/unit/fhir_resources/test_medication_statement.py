import json
import os

from fhir.resources.medicationstatement import MedicationStatement
from fhirhydrant.fhir_server.app.utils.resources.medication_statement import MedicationStatementResource
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from tests.unit.fhir_resources.base_fhir_resource_test import BaseFhirResourceTest


class MedicationStatementTest(BaseFhirResourceTest):

    def test_medication_statement(self):
        medication_statement_resource = MetaResource(MedicationStatement)

        test_file = 'fhir_resources/medication_statement.json'
        file_name = os.path.join(getattr(self.config, 'TEST_DATA_FOLDER'), test_file)

        with open(file_name) as fp:
            data = fp.read()
            medication_statement_dict = json.loads(data)

        medication_statement = MedicationStatement(medication_statement_dict)
        created_medication = medication_statement_resource.create(medication_statement)

        created_medication.__delitem__('id')
        created_medication.__delitem__('meta')

        self.assertEqual(created_medication, medication_statement_dict)
        id = created_medication.get('id')
        MedicationStatementResource().delete(id)
