from fhirhydrant.fhir_server.app.api.resources.status import StatusResource
from fhirhydrant.fhir_server.app.api.resources.provenance import ProvenanceResource
from fhirhydrant.fhir_server.app.api.resources.patient import PatientResource
from fhirhydrant.fhir_server.app.api.resources.organization import OrganizationResource
from fhirhydrant.fhir_server.app.api.resources.document import DocumentResource
from fhirhydrant.fhir_server.app.api.resources.document_reference import DocumentReferenceResource
from fhirhydrant.fhir_server.app.api.resources.clinical_text.demographics import DemographicsResource
from fhirhydrant.fhir_server.app.api.resources.clinical_text.de_identification import DeIdentificationResource
from fhirhydrant.fhir_server.app.api.resources.clinical_text.clinical_summary import ClinicalSummaryResource
from flask import blueprints, Flask
from flask_apispec import FlaskApiSpec


BLUEPRINT_NAME = 'fhir-api-v1'

"""
_resources tuple describes resources to be added to current blueprint:
(Resource class, Resource path, Options)

Options:
    - get_list: indicates whether Resource can return a list of the objects or not
    - get_item: indicates whether Resource can return a single objects by PK or not
    - pk: PK name, name of the kwarg in the GET method of the Resource. Required if get_item is True
    - pk_type: PK type. Required if get_item is True
"""

_resources = (
    (
        ClinicalSummaryResource,
        '/clinical_summary',
        dict(
            pk=None,
            pk_type=None,
            get_list=False,
            get_item=False
        )
    ),
    (
        DeIdentificationResource,
        '/de_identification',
        dict(
            pk=None,
            pk_type=None,
            get_list=False,
            get_item=False
        )
    ),
    (
        DemographicsResource,
        '/demographics',
        dict(
            pk=None,
            pk_type=None,
            get_list=False,
            get_item=False
        )
    ),
    (
        DocumentReferenceResource,
        '/document_reference',
        dict(
            pk='document_reference_id',
            pk_type='string',
            get_list=False,
            get_item=True
        )
    ),
    (
        DocumentResource,
        '/document',
        dict(
            pk='document_id',
            pk_type='string',
            get_list=True,
            get_item=True
        )
    ),
    (
        OrganizationResource,
        '/organization',
        dict(
            pk='organization_id',
            pk_type='string',
            get_list=True,
            get_item=True
        )
    ),
    (
        PatientResource,
        '/patient',
        dict(
            pk="patient_id",
            pk_type="string",
            get_list=False,
            get_item=True
        )
    ),
    (
        ProvenanceResource,
        '/provenance',
        dict(
            pk='provenance_id',
            pk_type='string',
            get_list=True,
            get_item=True
        )
    ),
    (
        StatusResource,
        '/status',
        dict(
            pk=None,
            pk_type=None,
            get_list=True,
            get_item=False
        )
    )
)


def _get_rules(resource, path, pk=None, pk_type=None, get_list=False, get_item=True) -> list:
    """
    Builds URL rules for the resource
    :param resource: Resource class
    :param path: Resource path
    :param pk: PK name, if needed
    :param pk_type: PK type, if needed
    :param get_list: Indicates if rule for list of items should be added (/resource/)
    :param get_item: Indicates if rule for getting item by PK should be added (/resource/{PK})
    :return: list
    """
    methods = set(resource.methods)

    if not get_list:
        methods = set(resource.methods) - {'GET'}

    rules = []

    if 'DELETE' in methods:
        methods.remove('DELETE')

    if methods:
        rules = [(f"{path}/", methods)]

    if 'GET' in resource.methods:
        if get_item:
            if pk is None:
                raise RuntimeError('pk is not specified for {}'.format(resource.__qualname__))
            if pk_type is None:
                raise RuntimeError('pk_type is not specified for {}'.format(resource.__qualname__))

            rules.append(("{path}/<{pk_type}:{pk}>".format(path=path, pk=pk, pk_type=pk_type), ['GET']))

    if 'DELETE' in resource.methods:
        if pk is None:
            raise RuntimeError('pk is not specified for {}'.format(resource.__qualname__))
        if pk_type is None:
            raise RuntimeError('pk_type is not specified for {}'.format(resource.__qualname__))
        rules.append(("{path}/<{pk_type}:{pk}>".format(path=path, pk=pk, pk_type=pk_type), ['DELETE']))

    return rules


def _register_views(bp: blueprints.Blueprint):
    """
    Register resource's views from _resource list in the blueprint
    :param bp: Api Blueprint
    :return:
    """
    for resource, path, options in _resources:
        view_name = resource.__name__.lower()
        view = resource.as_view(view_name)

        for rule, methods in _get_rules(resource, path, **options):
            bp.add_url_rule(rule, view_func=view, methods=methods)


def _register_doc(bp: blueprints.Blueprint, docs: FlaskApiSpec):
    """
    Register resources in the ApiSpec
    :param bp: Api blueprint
    :param docs: FlaskApiSpec instance
    :return:
    """
    for resource, *_ in _resources:
        docs.register(resource, blueprint=bp.name)


def init_app(app: Flask, doc: FlaskApiSpec = None):
    """
    Register API blueprint as well as documentation (optionally)
    :param app: Flask application
    :param doc: FlaskApiSpec instance. If None, no docs would be attached
    :return: None
    """
    bp = blueprints.Blueprint(BLUEPRINT_NAME, __name__)
    _register_views(bp)
    app.register_blueprint(bp, url_prefix='/api/v1')
    if doc is not None:
        _register_doc(bp, doc)
