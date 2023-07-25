from fhir.resources.domainresource import DomainResource


class BaseFHIRConverter:

    @classmethod
    def to_fhir(cls, obj: object):
        raise NotImplementedError("to_fhir method is not implemented")

    @classmethod
    def from_fhir(cls, resource: DomainResource):
        raise NotImplementedError("from_fhir method is not implemented")
