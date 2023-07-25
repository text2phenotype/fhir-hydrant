from datetime import datetime

from fhir.resources.fhirdate import FHIRDate
from ..converter.base import BaseFHIRConverter


class Date(BaseFHIRConverter):
    @classmethod
    def from_fhir(cls, fhirDate: FHIRDate) -> datetime:
        """
        Convert FHIRDate to date with format 'MM/DD/YYYY'
        :param fhirDate: date in FHIR format
        :return: datetime
        """
        return fhirDate.date

    @classmethod
    def to_fhir(cls, date: datetime) -> FHIRDate:
        """
        Convert date in format to FHIRDate
        :type date: datetime
        :param date: datetime
        :return: date in FHIR format
        """
        fhirDate = FHIRDate()
        fhirDate.date = date
        return fhirDate
