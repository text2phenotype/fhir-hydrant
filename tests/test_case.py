import glob
import unittest
from os import path
from typing import Dict

from fhirhydrant.fhir_server.app.config import get_config


def select_item(items: list):
    if len(items) != 0:
        return max(items, key=lambda token: token[1])[0]
    else:
        return None


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self._demographics_test_files = None
        self.config = get_config('test')

    @property
    def demographics_test_files(self) -> Dict:
        if self._demographics_test_files is None:
            test_data_folder = getattr(self.config, 'TEST_DATA_FOLDER')
            self._demographics_test_files = glob.iglob("{}/**/*.txt.json".format(test_data_folder), recursive=True)
            self._demographics_test_files = {
                path.basename(f).replace(".txt.json", ""): f
                for f in self._demographics_test_files
            }

        return self._demographics_test_files

    def assert_patients_are_equal(self, expected, actual, patient_name=None):
        attributes = (
            'dob', 'pat_first', 'pat_last', 'pat_city', 'pat_state', 'pat_zip', 'pat_phone', 'pat_email', 'sex'
        )

        for attribute in attributes:
            message = "{attribute} for {patient_name}".format(attribute=attribute, patient_name=patient_name)
            actual_attr = getattr(actual, attribute)
            expected_attr = getattr(expected, attribute)

            self.assertEqual(type(actual_attr), type(expected_attr))

            self.assertEqual(
                select_item(actual_attr),
                select_item(expected_attr),
                msg=message
            )
