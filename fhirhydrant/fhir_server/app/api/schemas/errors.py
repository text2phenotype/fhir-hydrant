from marshmallow import Schema, fields


class ValidationErrorSchema(Schema):
    errors = fields.List(
        fields.Dict()
    )
