import traceback

from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from requests import HTTPError

from fhirhydrant.fhir_client.utils.builders.bundle_from_clinical_summary \
    import build_bundle_from_clinical_summary, parse_bundle
from fhirhydrant.fhir_server.app.api.schemas.responses.clinical_summary_schema import ClinicalResponseSchema
from fhirhydrant.fhir_server.app.utils.resources.meta_resource import MetaResource
from fhirhydrant.fhir_server.app.api.schemas.errors import ValidationErrorSchema
from fhirhydrant.fhir_server.app.api.decorators.request_checker import check_tenant_id
from fhirhydrant.fhir_server.app.api.schemas.demographics import DemographicsSchema

from fhirhydrant.fhir_client.utils.converter.patient import PatientConverter
from flask import request
from flask_apispec import MethodResource, doc, marshal_with
from text2phenotype.apiclients.biomed import BioMedClient
from text2phenotype.common.demographics import Demographics

from text2phenotype.common.clinical_summary import ClinicalSummary


def text_to_demographics(clinical_text: str) -> Demographics:
    biomed_client = BioMedClient()
    demographics_data = biomed_client.get_demographics(clinical_text)
    schema = DemographicsSchema()

    return Demographics(**schema.load(demographics_data))


@doc(tags=['Clinical Summary'])
class ClinicalSummaryResource(MethodResource):
    @doc(
        description='Allows to pass Clinical text JSON to store it in the FHIR API',
        consumes='application/json',
        parameters=[
            {
                'in': 'body',
                'name': 'clinical_text',
                'required': True,
                'schema': {
                    'type': 'string'
                }
            }
        ],
        params={'tenantId': {
            'in': 'header',
            'type': 'string'
        }}
    )
    @check_tenant_id
    @marshal_with(ClinicalResponseSchema, code=201, description="Bundle successfully created")
    @marshal_with(ValidationErrorSchema, code=422, description="Validation Error")
    def post(self):
        try:
            clinical_text: str = request.get_data(as_text=True, cache=False)

            biomed_client = BioMedClient()
            demographics = text_to_demographics(clinical_text)
            patient = PatientConverter.to_fhir(demographics)

            patient = MetaResource(Patient).create(patient)

            summary_result = biomed_client.get_summary(clinical_text)
            summary = ClinicalSummary()
            summary.from_dict(summary_result)

            bundle = build_bundle_from_clinical_summary(summary, patient)

            bundle_response = MetaResource(Bundle).create(bundle)
            return parse_bundle(Bundle(bundle_response)), 201

        except HTTPError as e:
            return 'BIOMED internal error', e.response.status_code
        except:
            return f'FHIR Hydrant internal error: {traceback.format_exc()}', 500
