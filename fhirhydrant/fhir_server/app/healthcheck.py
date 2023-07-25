import requests
from typing import Tuple, Optional
from urllib.parse import urlparse
from flask import Flask, current_app
from flask_apispec import doc, FlaskApiSpec
from requests.exceptions import RequestException

from text2phenotype.common.status import StatusReport, Component, Status

from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv


def try_dependency(url: str) -> Tuple[Status, Optional[str]]:
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.OK:
            return Status.healthy, None
        else:
            return Status.dead, response.reason
    except RequestException:
        return Status.dead, None


@doc(tags=['HealthCheck'])
def live():
    return None


@doc(tags=['HealthCheck'])
def ready():
    app_config = current_app.config

    status_report = StatusReport()
    fhir_status = Status.healthy

    biomed_url = urlparse(FhirServerEnv.BIOMED_API_BASE.value).geturl()
    biomed_healthcheck_url = f"{biomed_url}/health/ready"

    fhir_api_base_url = urlparse(app_config.get('API_URL')).geturl()
    fhir_azure_healthcheck_url = f'{fhir_api_base_url}/metadata'

    dependencies = (
        (Component.biomed, biomed_healthcheck_url),
        (Component.fhir_azure_api, fhir_azure_healthcheck_url)
    )

    for component, url in dependencies:
        status, reason = try_dependency(url)
        status_report.add_status(component, (status, reason))
        if status != Status.healthy:
            fhir_status = Status.conditional

    status_report.add_status(Component.fhir, (fhir_status, None))
    return status_report.as_json(), fhir_status.value


def init_app(app: Flask, doc: FlaskApiSpec = None):
    app.add_url_rule("/health/live", view_func=live, methods=["GET"], provide_automatic_options=False)
    app.add_url_rule("/health/ready", view_func=ready, methods=["GET"], provide_automatic_options=False)
    if doc is not None:
        doc.register(live)
        doc.register(ready)
