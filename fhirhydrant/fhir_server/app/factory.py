from flask import Flask

from text2phenotype.common.log import operations_logger
from text2phenotype.apm.flask import configure_apm

from fhirhydrant.fhir_server.app import healthcheck
from fhirhydrant.fhir_server.app.api import api
from fhirhydrant.fhir_server.app.patch.apispec.apispec import ApiSpec

from fhirhydrant.fhir_server.app.config import get_config
from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv


def create_app() -> Flask:

    config = get_config(FhirServerEnv.FLASK_ENV.value)

    app = Flask(__name__)
    app.config.from_object(config)

    docs = None

    if config.ENABLE_DOCS:
        docs = ApiSpec()
        docs.init_app(app)

    api.init_app(app, docs)
    healthcheck.init_app(app, docs)
    configure_apm(app, FhirServerEnv.APM_SERVICE_NAME.value, config.DEBUG)

    for handler in operations_logger.logger.handlers:
        app.logger.addHandler(handler)

    return app
