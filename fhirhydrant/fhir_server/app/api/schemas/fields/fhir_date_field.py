from fhir.resources.fhirdate import FHIRDate
from marshmallow import fields


def _fhir_serialize(date: FHIRDate, localtime=False) -> str:
    return date.isostring


def _fhir_deserialize(date: str) -> FHIRDate:
    return FHIRDate(date)


class FHIRDateField(fields.DateTime):
    DEFAULT_FORMAT = 'fhir'

    SERIALIZATION_FUNCS = {
        'fhir': _fhir_serialize
    }

    DESERIALIZATION_FUNCS = {
        'fhir': _fhir_deserialize
    }