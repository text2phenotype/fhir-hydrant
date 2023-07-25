import marshmallow
from fhir.resources.binary import Binary
from fhir.resources.documentreference import DocumentReference
from fhir.resources.provenance import Provenance

from fhirhydrant.fhir_server.app.utils.schemas.generator import resource_to_schema
from marshmallow import fields


class DocumentSchema(marshmallow.Schema):
    provenance = fields.Nested(resource_to_schema(Provenance), required=True, many=False)
    document_reference = fields.Nested(resource_to_schema(DocumentReference), required=True, many=False)
    binary = fields.Nested(resource_to_schema(Binary), required=True, many=False)
