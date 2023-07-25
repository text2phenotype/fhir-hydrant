from marshmallow import Schema, fields, validates_schema, ValidationError


class FHIRResourceSchema(Schema):
    _one_of_many: dict = None

    @validates_schema
    def one_of_many_validation(self, data, **kwargs):
        if self._one_of_many is None:
            return

        for key, field_names in self._one_of_many.items():
            if not any(map(lambda f: data.get(f, None), field_names)):
                raise ValidationError("You must provide one of the [{}]".format(", ".join(field_names)))


class ExtensionSchema(FHIRResourceSchema):
    extension = fields.Nested('self', required=False, many=True)
    id = fields.String(required=False)
    url = fields.String(required=True)
    valueAddress = fields.Nested('AddressSchema', required=False, many=False)
    valueAge = fields.Nested('AgeSchema', required=False, many=False)
    valueAnnotation = fields.Nested('AnnotationSchema', required=False, many=False)
    valueAttachment = fields.Nested('AttachmentSchema', required=False, many=False)
    valueBase64Binary = fields.String(required=False)
    valueBoolean = fields.Boolean(required=False)
    valueCanonical = fields.String(required=False)
    valueCode = fields.String(required=False)
    valueCodeableConcept = fields.Nested('CodeableConceptSchema', required=False, many=False)
    valueCoding = fields.Nested('CodingSchema', required=False, many=False)
    valueContactDetail = fields.Nested('ContactDetailSchema', required=False, many=False)
    valueContactPoint = fields.Nested('ContactPointSchema', required=False, many=False)
    valueContributor = fields.Nested('ContributorSchema', required=False, many=False)
    valueCount = fields.Nested('CountSchema', required=False, many=False)
    valueDataRequirement = fields.Nested('DataRequirementSchema', required=False, many=False)
    valueDate = fields.DateTime(required=False)
    valueDateTime = fields.DateTime(required=False)
    valueDecimal = fields.Float(required=False)
    valueDistance = fields.Nested('DistanceSchema', required=False, many=False)
    valueDosage = fields.Nested('DosageSchema', required=False, many=False)
    valueDuration = fields.Nested('DurationSchema', required=False, many=False)
    valueExpression = fields.Nested('ExpressionSchema', required=False, many=False)
    valueHumanName = fields.Nested('HumanNameSchema', required=False, many=False)
    valueId = fields.String(required=False)
    valueIdentifier = fields.Nested('IdentifierSchema', required=False, many=False)
    valueInstant = fields.DateTime(required=False)
    valueInteger = fields.Integer(required=False)
    valueMarkdown = fields.String(required=False)
    valueMoney = fields.Nested('MoneySchema', required=False, many=False)
    valueOid = fields.String(required=False)
    valueParameterDefinition = fields.Nested('ParameterDefinitionSchema', required=False, many=False)
    valuePeriod = fields.Nested('PeriodSchema', required=False, many=False)
    valuePositiveInt = fields.Integer(required=False)
    valueQuantity = fields.Nested('QuantitySchema', required=False, many=False)
    valueRange = fields.Nested('RangeSchema', required=False, many=False)
    valueRatio = fields.Nested('RatioSchema', required=False, many=False)
    valueReference = fields.Nested('FHIRReferenceSchema', required=False, many=False)
    valueRelatedArtifact = fields.Nested('RelatedArtifactSchema', required=False, many=False)
    valueSampledData = fields.Nested('SampledDataSchema', required=False, many=False)
    valueSignature = fields.Nested('SignatureSchema', required=False, many=False)
    valueString = fields.String(required=False)
    valueTime = fields.DateTime(required=False)
    valueTiming = fields.Nested('TimingSchema', required=False, many=False)
    valueTriggerDefinition = fields.Nested('TriggerDefinitionSchema', required=False, many=False)
    valueUnsignedInt = fields.Integer(required=False)
    valueUri = fields.String(required=False)
    valueUrl = fields.String(required=False)
    valueUsageContext = fields.Nested('UsageContextSchema', required=False, many=False)
    valueUuid = fields.String(required=False)


class IdentifierSchema(FHIRResourceSchema):
    assigner = fields.Nested('FHIRReferenceSchema', required=False, many=False)
    extension = fields.Nested('ExtensionSchema', required=False, many=True)
    id = fields.String(required=False)
    period = fields.Nested('PeriodSchema', required=False, many=False)
    system = fields.String(required=False)
    type = fields.Nested('CodeableConceptSchema', required=False, many=False)
    use = fields.String(required=False)
    value = fields.String(required=False)
