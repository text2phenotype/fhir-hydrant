from text2phenotype.common.demographics import Demographics

from fhirhydrant.fhir_client.utils.converter.practitioner import PractitionerConverter
from tests.unit.schemas.test_demographics import TestCase


class PractitionerConverterTest(TestCase):

    def assert_equal(self, actual, expected, msg=None):

        def get_value(attribute):
            if not isinstance(attribute, list):
                self.fail(msg + " is not a list")

            if len(attribute) < 1:
                self.fail("nothing to assert for " + msg)

            return max(attribute, key=lambda token: token[1])[0]

        self.assertEqual(get_value(actual), get_value(expected), msg=msg)

    def test_practitioner_converter(self):
        score = 0.98

        demographics = Demographics()
        demographics.dr_id = [("DR_ID", score)]
        demographics.dr_city = [("Los Alamos", score)]
        demographics.dr_email = [("moreau@example.com", score)]
        demographics.dr_fax = [("12345", score)]
        demographics.dr_first = [("Montgomery", score)]
        demographics.dr_id = [("013456", score)]
        demographics.dr_initials = [("M.M.", score)]
        demographics.dr_last = [("Moreau", score)]
        demographics.dr_middle = [("M.", score)]
        demographics.dr_phone = [("+1555789654", score)]
        demographics.dr_state = [("New Mexico", score)]
        demographics.dr_street = [("Windsor Garden", score)]
        demographics.dr_zip = [("895675", score)]

        # is not representable by Practitioner type
        demographics.dr_org = [("Insula inc.", score)]
        demographics.facility_name = [("The second", score)]

        fhir_repr = PractitionerConverter.to_fhir(demographics)
        restored = PractitionerConverter.from_fhir(fhir_repr)

        converted_fields = ('dr_id', 'dr_city', 'dr_email', 'dr_fax', 'dr_first', 'dr_id', 'dr_initials', 'dr_last',
                            'dr_middle', 'dr_phone', 'dr_state', 'dr_street', 'dr_zip')

        for field in converted_fields:
            self.assert_equal(getattr(demographics, field), getattr(restored, field), msg=field)
