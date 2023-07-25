import dateutil.parser as date_parser

from fhir.resources.address import Address
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.patient import Patient

from text2phenotype.common.demographics import Demographics

from ..converter.base import BaseFHIRConverter
from ..converter.date import Date
from ..converter.helpers import first, make_codeable_concept


class PatientConverter(BaseFHIRConverter):
    DEFAULT_SCORE = 1.0

    class DemographicsWrapper:
        def __init__(self, demographics: Demographics):
            self._demographics = demographics

        def __getattribute__(self, item):

            demographics = super(PatientConverter.DemographicsWrapper, self).__getattribute__('_demographics')
            attribute = getattr(demographics, item)

            if not attribute:
                return None

            if isinstance(attribute, list):
                return max(attribute, key=lambda token: token[1])[0]
            else:
                return attribute

    @classmethod
    def to_fhir(cls, demographics: Demographics) -> Patient:

        demographics: cls.DemographicsWrapper = cls.DemographicsWrapper(demographics)

        patient = Patient()
        patient.active = False

        if type(demographics.dob) is str:
            patient.birthDate = Date.to_fhir(date_parser.parse(demographics.dob))
        else:
            patient.birthDate = Date.to_fhir(demographics.dob)

        humanName = HumanName()
        humanName.family = demographics.last_name
        humanName.given = [demographics.first_name]
        patient.name = [humanName]

        if demographics.pat_city and demographics.pat_state and demographics.pat_zip:
            address = Address()
            address.city = demographics.pat_city
            address.state = demographics.pat_state
            address.postalCode = demographics.pat_zip
            patient.address = [address]

        patient.telecom = []

        if demographics.pat_phone:
            homePhone = ContactPoint()
            homePhone.system = "phone"
            homePhone.use = "home"
            homePhone.value = demographics.pat_phone
            patient.telecom.append(homePhone)

        if demographics.pat_email:
            email = ContactPoint()
            email.system = "email"
            email.use = "home"
            email.value = demographics.pat_email
            patient.telecom.append(email)

        if demographics.sex is not None:
            patient.gender = str.lower(demographics.sex)

        if demographics.ssn:
            identifier = Identifier()
            identifier.use = 'usual'

            identifier.type = make_codeable_concept(None, 'SS', 'http://terminology.hl7.org/CodeSystem/v2-0203')
            identifier.system = 'http://hl7.org/fhir/sid/us-ssn'
            identifier.value = demographics.ssn
            patient.identifier = [identifier]

        return patient

    @classmethod
    def wrap(cls, value):
        return [[value, cls.DEFAULT_SCORE]]

    @classmethod
    def from_fhir(cls, data: dict()) -> Demographics:

        patient = Patient(data)
        demographics = Demographics()

        demographics.dob = cls.wrap(Date.from_fhir(patient.birthDate))

        name = first(patient.name)
        if name:
            demographics.pat_first = cls.wrap(first(name.given))
            demographics.pat_last = cls.wrap(name.family)

        address = first(patient.address)
        if address:
            demographics.pat_city = cls.wrap(address.city)
            demographics.pat_state = cls.wrap(address.state)
            demographics.pat_zip = cls.wrap(address.postalCode)

        for contact_point in patient.telecom:
            if contact_point.system == 'phone':
                demographics.pat_phone = cls.wrap(contact_point.value)
            elif contact_point.system == 'email':
                demographics.pat_email = cls.wrap(contact_point.value)

        if patient.gender:
            demographics.sex = cls.wrap(patient.gender)

        return demographics
