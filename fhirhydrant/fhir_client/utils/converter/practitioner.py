from itertools import chain

from fhir.resources.address import Address
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.humanname import HumanName
from fhir.resources.practitioner import Practitioner

from text2phenotype.common.demographics import Demographics
from ..converter.patient import PatientConverter
from ..converter.helpers import first


class PractitionerConverter(PatientConverter):
    TELECOM = {
        'email': 'dr_email',
        'fax': 'dr_fax',
        'phone': 'dr_phone'
    }

    @classmethod
    def to_fhir(cls, demographics: Demographics) -> Practitioner:
        demographics = cls.DemographicsWrapper(demographics)
        practitioner = Practitioner()

        practitioner.identifier = demographics.dr_id
        name = HumanName()
        name.family = demographics.dr_last
        name.given = [demographics.dr_first, demographics.dr_middle, demographics.dr_initials]
        practitioner.name = [name]

        address = Address()
        address.state = demographics.dr_state
        address.city = demographics.dr_city
        address.line = [demographics.dr_street]
        address.postalCode = demographics.dr_zip
        practitioner.address = [address]

        telecom = []
        for system, field_name in cls.TELECOM.items():
            value = getattr(demographics, field_name)
            if value is not None:
                telecom.append(
                    ContactPoint({
                        'system': system,
                        'value': value
                    })
                )

        practitioner.telecom = telecom

        return practitioner

    @classmethod
    def from_fhir(cls, obj: Practitioner) -> Demographics:
        demographics = Demographics()
        if obj.identifier:
            demographics.dr_id = cls.wrap(obj.identifier)

        name: HumanName = first(obj.name)
        if name:
            demographics.dr_last = cls.wrap(name.family)
            given_name = name.given
            if given_name is not None:
                dr_first, dr_middle, dr_initials, *_ = chain(given_name, [None, None, None])
                if dr_first:
                    demographics.dr_first = cls.wrap(dr_first)
                if dr_middle:
                    demographics.dr_middle = cls.wrap(dr_middle)
                if dr_initials:
                    demographics.dr_initials = cls.wrap(dr_initials)

        address: Address = first(obj.address)
        if address:
            demographics.dr_state = cls.wrap(address.state)
            demographics.dr_city = cls.wrap(address.city)
            demographics.dr_street = cls.wrap(first(address.line))
            demographics.dr_zip = cls.wrap(address.postalCode)

        for telecom in obj.telecom:
            if telecom.system not in cls.TELECOM.keys():
                continue
            field_name = cls.TELECOM.get(telecom.system)
            setattr(demographics, field_name, cls.wrap(telecom.value))

        demographics.dr_org = [("", cls.DEFAULT_SCORE)]
        demographics.facility_name = [("", cls.DEFAULT_SCORE)]

        return demographics
