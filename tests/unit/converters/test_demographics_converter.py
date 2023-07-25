import json
from datetime import datetime

from fhir.resources.patient import Patient

from text2phenotype.common.demographics import Demographics

from fhirhydrant.fhir_client.utils.converter.patient import PatientConverter
from tests.unit.schemas.test_demographics import TestCase
from tests.test_case import select_item


def get_demographics_data(fp) -> Demographics:
    data = json.load(fp)
    dob = datetime.strptime(select_item(data['dob']), "%m/%d/%Y")

    data["dob"] = [
        [dob, 1]
    ]
    return data


class DemographicsConverterTest(TestCase):
    def test_demographics_converter(self):

        for test_file in self.demographics_test_files.values():
            with open(test_file) as fp:
                data = get_demographics_data(fp)
                demographics = Demographics(**data)
                actual = PatientConverter.to_fhir(demographics)
                self.assert_demographics_object(actual, demographics)

    def assert_demographics_object(self, actual: Patient, demographics: Demographics):
        # if all parsed correct, it is able to convert to json
        jsonPatient = actual.as_json()

        self.assertEqual(select_item(demographics.dob), actual.birthDate.date)
        self.assertIn(demographics.first_name, (givenName for name in actual.name for givenName in name.given))
        self.assertIn(demographics.last_name, (name.family for name in actual.name))

        if actual.address is not None:
            self.assertIn(select_item(demographics.pat_city),
                          (address.city for address in actual.address))
            self.assertIn(select_item(demographics.pat_state),
                          (address.state for address in actual.address))
            self.assertIn(select_item(demographics.pat_zip),
                          (address.postalCode for address in actual.address))

        telecomPhones = list(telecom.value for telecom in actual.telecom if telecom.system == "phone")
        telecomEmails = list(telecom.value for telecom in actual.telecom if telecom.system == "email")

        if telecomPhones.__len__() > 0:
            self.assertIn(select_item(demographics.pat_phone), telecomPhones)

        if telecomEmails.__len__() > 0:
            self.assertIn(select_item(demographics.pat_email), telecomEmails)

    def test_patient_to_demographics_convert(self):
        patients = []
        for patient_name, test_file in self.demographics_test_files.items():
            with open(test_file, 'r') as fp:
                demographics = Demographics(**get_demographics_data(fp))
                patients.append(
                    (demographics, PatientConverter.to_fhir(demographics), patient_name)
                )

        for expected, patient, patient_name in patients:
            actual = PatientConverter.from_fhir(patient.as_json())
            self.assert_patients_are_equal(expected, actual, patient_name=patient_name)
