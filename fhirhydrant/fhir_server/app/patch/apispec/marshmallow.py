import apispec.ext.marshmallow
import marshmallow
from fhirhydrant.fhir_server.app.utils.schemas.schemas import FHIRResourceSchema
from fhirhydrant.fhir_server.app.api.schemas.fields.file import FileField


class OpenAPIConverter(apispec.ext.marshmallow.OpenAPIConverter):

    def __init__(self, *args, skip_fhir_docs=False, **kwargs):
        super(OpenAPIConverter, self).__init__(*args, **kwargs)
        self.skip_fhir_docs = skip_fhir_docs
        self.field_mapping.update(
            {
                marshmallow.fields.Tuple: ("array", None)
            }
        )

    def set_skip_fhir_doc(self, value):
        self.skip_fhir_docs = value

    def init_attribute_functions(self):
        super().init_attribute_functions()
        self.attribute_functions.extend([
            self.tuple2properties,
            self.file2properties,
            self.fhir2properties
        ])

    def tuple2properties(self, field, ret):
        if isinstance(field, marshmallow.fields.Tuple):
            item_number = len(field.tuple_fields)
            field_props = [self.field2property(f) for f in field.tuple_fields]
            ret = dict(
                type="array",
                items=dict(oneOf=field_props),
                minItems=item_number,
                maxItems=item_number
            )
            ret["x-order"] = field_props

        return ret

    def file2properties(self, field, ret):
        if isinstance(field, FileField):
            ret = {
                'type': 'file',
                'in': 'formData'
            }
        return ret

    def fhir2properties(self, field, ret):
        if not (self.skip_fhir_docs
                and isinstance(field, marshmallow.fields.Nested)
                and isinstance(field.schema, FHIRResourceSchema)):
            return ret

        schema_dict = self.resolve_nested_schema(field.schema)
        if "items" in schema_dict:
            schema = schema_dict["items"]
        else:
            schema = schema_dict
        definition = schema["$ref"].split("/")[-1]

        del schema["$ref"]
        schema.update({
            "type": "object",
            "description": f"For reference see {definition} model"
        })

        return schema_dict


class MarshmallowPlugin(apispec.ext.marshmallow.MarshmallowPlugin):
    Converter = OpenAPIConverter
    SKIP_FHIR_DOC = True

    def init_spec(self, *args, **kwargs):
        super(MarshmallowPlugin, self).init_spec(*args, **kwargs)
        if hasattr(self.converter, 'set_skip_fhir_doc'):
            self.converter.set_skip_fhir_doc(self.SKIP_FHIR_DOC)
