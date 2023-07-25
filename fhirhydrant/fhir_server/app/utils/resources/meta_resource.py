from fhirhydrant.fhir_server.app.utils.resources.fhir_resource import FHIRResource


class MetaResource(FHIRResource):
    def __init__(self, resource_class: type):
        resource_type: str = resource_class.__name__
        super().__init__(resource_type)
