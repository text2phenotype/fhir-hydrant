from collections import namedtuple, defaultdict
from functools import lru_cache
from typing import Type, TypeVar

from fhir.resources.extension import Extension
from fhir.resources.fhirabstractbase import FHIRAbstractBase
from fhir.resources.fhirdate import FHIRDate
from fhir.resources.identifier import Identifier
from fhirhydrant.fhir_server.app.api.schemas.fields.fhir_date_field import FHIRDateField
from marshmallow import fields

from .schemas import ExtensionSchema, IdentifierSchema, FHIRResourceSchema

__WARMED = False

TFHIRResource = TypeVar("TFHIRResource", bound=FHIRAbstractBase)
TSchema = TypeVar("TSchema", bound=FHIRResourceSchema)

__attribute_field_map = {
    FHIRDate: FHIRDateField,
    str: fields.String,
    float: fields.Float,
    bool: fields.Boolean,
    int: fields.Integer
}

__resource_schema_map = {
    Extension: ExtensionSchema,
    Identifier: IdentifierSchema
}

ResourceAttribute = namedtuple("ResourceAttribute",
                               ["name", "json_name", "type", "is_list", "of_many", "not_optional"])


@lru_cache(maxsize=128)
def resource_to_schema(resource_cls: Type[TFHIRResource]) -> Type[TSchema]:
    if not __WARMED:
        __warmup()
    assert hasattr(resource_cls, 'elementProperties')

    prepared = __resource_schema_map.get(resource_cls, None)
    if prepared is not None:
        return prepared

    resource = resource_cls()
    resource_attributes = resource.elementProperties()
    del resource

    schema_class_name = "{}Schema".format(resource_cls.__name__)

    schema_attributes = {}

    one_of_many = defaultdict(list)

    attribute: ResourceAttribute
    for attribute in map(ResourceAttribute._make, resource_attributes):
        field = _attribute_to_field(attribute)
        if attribute.of_many and attribute.not_optional:
            one_of_many[attribute.of_many].append(attribute.json_name)
            field.required = False
        schema_attributes[attribute.json_name] = field

    schema_attributes['resourceType'] = fields.String(required=False, many=False)
    if len(one_of_many):
        schema_attributes['_one_of_many'] = one_of_many

    schema = type(schema_class_name, (FHIRResourceSchema,), schema_attributes)
    return schema


def _attribute_to_field(attribute: ResourceAttribute) -> fields.Field:
    if hasattr(attribute.type, 'elementProperties'):
        return fields.Nested(resource_to_schema(attribute.type),
                             many=attribute.is_list,
                             required=attribute.not_optional)

    field_type = __attribute_field_map.get(attribute.type, fields.Raw)
    attributes = dict(
        required=attribute.not_optional
    )

    if attribute.is_list:
        return fields.List(field_type, **attributes)

    return field_type(**attributes)


def __warmup():
    """
    Warming up LRU cache of `resource_to_schema()` with schemas required for Extension Schema.
    Needs to be done this way because of recursive definition of Extension and Identifier resources.
    """

    global __WARMED

    if __WARMED:
        return

    from fhir.resources.extension import (
        address,
        age,
        annotation,
        attachment,
        codeableconcept,
        coding,
        contactdetail,
        contactpoint,
        contributor,
        count,
        datarequirement,
        distance,
        dosage,
        duration,
        expression,
        humanname,
        money,
        parameterdefinition,
        quantity,
        range,
        ratio,
        fhirreference,
        relatedartifact,
        sampleddata,
        signature,
        timing,
        triggerdefinition,
        usagecontext,
        period
    )

    __warmup = (
        period.Period,
        address.Address,
        age.Age,
        annotation.Annotation,
        attachment.Attachment,
        codeableconcept.CodeableConcept,
        coding.Coding,
        contactdetail.ContactDetail,
        contactpoint.ContactPoint,
        contributor.Contributor,
        count.Count,
        datarequirement.DataRequirement,
        distance.Distance,
        dosage.Dosage,
        duration.Duration,
        expression.Expression,
        humanname.HumanName,
        money.Money,
        parameterdefinition.ParameterDefinition,
        period.Period,
        quantity.Quantity,
        range.Range,
        ratio.Ratio,
        fhirreference.FHIRReference,
        relatedartifact.RelatedArtifact,
        sampleddata.SampledData,
        signature.Signature,
        timing.Timing,
        triggerdefinition.TriggerDefinition,
        usagecontext.UsageContext,
    )

    __WARMED = True

    for x in __warmup:
        resource_to_schema(x)
