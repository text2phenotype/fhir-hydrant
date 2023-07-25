import base64
from datetime import datetime

from fhir.resources import fhirdate, coding, attachment, codeableconcept
from fhir.resources.binary import Binary
from fhir.resources.documentreference import DocumentReference, DocumentReferenceContent
from fhir.resources.fhirreference import FHIRReference
from fhir.resources.provenance import Provenance, ProvenanceAgent

from ...utils.enums.document_reference_source import DocumentReferenceSource


def build_provenance(document_reference_id: str, document_reference_source: int) -> Provenance:
    provenance = Provenance()
    provenance.recorded = fhirdate.FHIRDate(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    who_reference = FHIRReference()
    who_reference.reference = "Organization/a4770810-0fbd-400a-a68b-78a6795bcc35"  # TODO: replace mock by real data

    provenance_agent = ProvenanceAgent()
    provenance_agent.who = who_reference
    provenance.agent = [provenance_agent]

    provenance_target = FHIRReference()
    provenance_target.reference = "DocumentReference/{}".format(document_reference_id)
    provenance.target = [provenance_target]

    activity_coding = codeableconcept.CodeableConcept()

    # TODO: set code type for each cases
    if document_reference_source == DocumentReferenceSource.de_id:
        activity_coding.system = "http://terminology.hl7.org/CodeSystem/v3-ActCode"
        activity_coding.code = "DEID"
        activity_coding.display = "deidentify"
    else:
        activity_coding.system = "http://terminology.hl7.org/CodeSystem/v3-DocumentCompletion"
        activity_coding.code = "LA"
        activity_coding.display = "legally authenticated"

    provenance.activity = activity_coding
    return provenance


def build_document_reference(subject: dict, binary_id: str) -> DocumentReference:
    reference = DocumentReference()
    reference.status = "current"
    reference.docStatus = "final"

    reference.type = codeableconcept.CodeableConcept()

    type_coding = coding.Coding()
    type_coding.system = "http://loinc.org"
    type_coding.code = "51899-3"
    type_coding.display = "Details Document"

    reference.type.coding = [type_coding]

    if subject:
        reference.subject = FHIRReference()
        reference.subject.reference = "{}/{}".format(subject.get("resourceType"), subject.get("id"))

    content = DocumentReferenceContent()
    content.attachment = attachment.Attachment()
    content.attachment.contentType = "text/plain"
    content.attachment.url = f"Binary/{binary_id}"
    reference.content = [content]
    return reference


def build_binary(document_content: str) -> Binary:
    binary = Binary()
    binary.data = base64.b64encode(document_content.encode('utf-8')).decode("utf-8")
    binary.contentType = 'text/plain'
    return binary
