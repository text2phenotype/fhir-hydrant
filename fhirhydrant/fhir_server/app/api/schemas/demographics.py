from marshmallow import Schema
from marshmallow.fields import List, Float, Tuple, String, Field

from .fields.date import MDYDate


def _lot(a: Field = None, b: Field = None, **kwargs) -> Field:
    """
    Returns List of Tuples representation
    :param a: Instance of the first element of the tuple
    :param b: Instance of the Second element of the tuple
    :return:
    """
    a = a or String()
    b = b or Float()
    return List(Tuple((a, b)), **kwargs)


class DemographicsSchema(Schema):
    ssn = _lot(description="SSN")
    mrn = _lot(description="MRN")
    pat_first = _lot(description="PAT_FIRST")
    pat_middle = _lot(description="PAT_MIDDLE")
    pat_last = _lot(description="PAT_LAST")
    pat_initials = _lot(description="PAT_INITIALS")
    pat_age = _lot(description="PAT_AGE")
    pat_street = _lot(description="PAT_STREET")
    pat_zip = _lot(description="PAT_ZIP")
    pat_city = _lot(description="PAT_CITY")
    pat_state = _lot(description="PAT_STATE")
    pat_phone = _lot(description="PAT_PHONE")
    pat_email = _lot(description="PAT_EMAIL")
    insurance = _lot(description="INSURANCE")
    facility_name = _lot(description="FACILITY_NAME")
    sex = _lot(description="SEX")
    dob = _lot(MDYDate(), description="DOB")
    dr_first = _lot(description="DR_FIRST")
    dr_middle = _lot(description="DR_MIDDLE")
    dr_last = _lot(description="DR_LAST")
    dr_initials = _lot(description="DR_INITIALS")
    dr_age = _lot(description="DR_AGE")
    dr_street = _lot(description="DR_STREET")
    dr_zip = _lot(description="DR_ZIP")
    dr_city = _lot(description="DR_CITY")
    dr_state = _lot(description="DR_STATE")
    dr_phone = _lot(description="DR_PHONE")
    dr_fax = _lot(description="DR_FAX")
    dr_email = _lot(description="DR_EMAIL")
    dr_id = _lot(description="DR_ID")
    dr_org = _lot(description="DR_ORG")

    class Meta:
        strict = True
