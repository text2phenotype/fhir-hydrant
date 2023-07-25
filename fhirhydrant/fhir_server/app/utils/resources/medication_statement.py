from fhirhydrant.fhir_server.app.utils.resources.fhir_resource import FHIRResource


class MedicationStatementResource(FHIRResource):
    def __init__(self):
        self.resource_name = 'MedicationStatement'
        super(MedicationStatementResource, self).__init__(self.resource_name)

