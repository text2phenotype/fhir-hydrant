from fhir.resources.provenance import Provenance
from fhir.resources.binary import Binary
from fhir.resources.documentreference import DocumentReference
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_client.utils.converter.resource_builder import build_provenance, build_binary, \
    build_document_reference


def create_document_reference(document_content: str, source: int, patient: dict = None) -> dict:
    binary = build_binary(document_content)

    created_binary = MetaResource(Binary).create(binary)

    reference = build_document_reference(patient, created_binary.get('id', ''))

    document_reference = MetaResource(DocumentReference).create(reference)
    document_reference_id = document_reference.get('id')

    provenance = build_provenance(document_reference_id, source)
    created_provenance = MetaResource(Provenance).create(provenance)

    return {'provenance': Provenance(created_provenance),
            'document_reference': DocumentReference(document_reference),
            'binary': Binary(created_binary)}


def get_source_binary_url_from_attachment(attachment_binary_url: str) -> str:
    # "binary/{id}" -> "{id}"
    return attachment_binary_url.split("/")[1]


def get_binary_id_by_document_reference_id(document_reference_id: str) -> str:
    document_reference = DocumentReference(MetaResource(DocumentReference).get(document_reference_id))
    content_list = list(document_reference.content)
    binary_id: str = ""

    if len(content_list) > 0:
        content = content_list[0]
        if content:
            attachment = content.attachment
            if attachment:
                binary_id = get_source_binary_url_from_attachment(attachment.url)
                return binary_id

    return binary_id


def get_document_reference_by_provenance_id(provenance_id: str) -> str:
    provenance = MetaResource(Provenance).get(provenance_id)
    target_dict = provenance.get('target')[0]
    reference = target_dict.get('reference')
    _, document_reference_id = reference.split('/')
    return document_reference_id
