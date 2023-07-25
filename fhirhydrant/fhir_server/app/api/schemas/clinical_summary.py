from marshmallow import Schema
from marshmallow.fields import List, Float, Tuple, String, Field, Integer, Nested, Dict
from marshmallow.validate import Length


class NullableTupleList(Tuple):

    def __init__(self, *args, **kwargs):
        super(NullableTupleList, self).__init__(*args, **kwargs)
        self.validate_length = Length(max=len(self.tuple_fields))
        self.default = None

    def _serialize(self, value, attr, obj, **kwargs):
        result = super(NullableTupleList, self)._serialize(value, attr, obj, **kwargs)
        return list(result)

    def _deserialize(self, value, attr, data, **kwargs):
        result = super(NullableTupleList, self)._deserialize(value, attr, data, **kwargs)
        return list(result)

class Concept(Schema):
    code = String()
    cui = String()
    lstm_prob = Float()
    polarity = String()  # TODO: Enum or Dedicated Field (from bool)
    preferredText = String()
    range = Tuple((Integer(), Integer()))
    text = String()
    tui = String()
    vocab = String()  # TODO: Enum


class MedicationSchema(Schema):
    code = String(allow_none=True)
    cui = String(allow_none=True)

    medFrequencyNumber = NullableTupleList((String(), Integer(), Integer()))  # required=False, allow_none=True
    medFrequencyUnit = NullableTupleList((String(), Integer(), Integer()))
    medStrengthNum = NullableTupleList((String(), Integer(), Integer()))
    medStrengthUnit = NullableTupleList((String(), Integer(), Integer()))
    polarity = String(allow_none=True)
    preferredText = String(allow_none=True)
    prob = Dict()
    range = Tuple((Integer(), Integer()))
    text = String()
    tui = String(allow_none=True)
    vocab = String(allow_none=True)  # TODO: Enum


class DisorderSchema(Concept):
    attributes = Dict()
    umlsConcept = List(String())


class ClinicalSummarySchema(Schema):
    Allergy = List(Nested(Concept()))
    DiseaseDisorder = List(Nested(DisorderSchema()))
    Lab = List(Nested(Concept()))
    Medication = List(Nested(MedicationSchema()))

    # The rest of it is in the ClinicalSuumary, but never occures in the examples
    #
    # Diagnosis = List(Nested(Concept()))
    # Problem = List(Nested(Concept()))
    # AnatomicalSite = List(Nested(Concept()))
    # Procedure = List(Nested(Concept()))

    class Meta:
        strict = True
