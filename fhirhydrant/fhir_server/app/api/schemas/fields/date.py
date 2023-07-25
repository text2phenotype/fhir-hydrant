from datetime import datetime
from marshmallow.fields import Date


def _date_serialize(value: datetime, localtime = None):
    result = datetime.strftime(value, "%-m/%-d/%Y")
    return result


def _date_deserialize(datestring: str):
    return datetime.strptime(datestring, "%m/%d/%Y")


class MDYDate(Date):
    DEFAULT_FORMAT = 'mdy'

    SERIALIZATION_FUNCS = {
        'mdy': _date_serialize
    }

    DESERIALIZATION_FUNCS = {
        'mdy': _date_deserialize,
    }
