import marshmallow


class OrganizationResponseSchema(marshmallow.Schema):
    organization_id = marshmallow.fields.String()
