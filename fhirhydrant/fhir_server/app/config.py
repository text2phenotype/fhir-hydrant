import os
from apispec import APISpec
from webargs.flaskparser import FlaskParser

from fhirhydrant.fhir_server.app.api.error_handler import error_handler
from fhirhydrant.fhir_server.app.patch.apispec.marshmallow import MarshmallowPlugin


class Config:
    DEBUG = False
    ENABLE_DOCS = False

    APISPEC_SWAGGER_URL = '/spec'
    APISPEC_SWAGGER_UI_URL = '/docs'

    APISPEC_SPEC = APISpec(
        title='Text2phenotype FHIR documentation',
        version='v0.1',
        openapi_version='2.0.0',
        plugins=[MarshmallowPlugin()],
    )

    APISPEC_WEBARGS_PARSER = FlaskParser(
        error_handler=error_handler
    )

    ROOT_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../'
        )
    )


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ENABLE_DOCS = True


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ENABLE_DOCS = True


class TestConfig(Config):
    DEBUG = True
    ENABLE_DOCS = False

    SERVER_NAME = 'test_server'
    TESTING = True

    TEST_DATA_FOLDER = os.path.abspath(os.path.join(Config.ROOT_DIR, '../..', 'test_data'))


def get_config(environment: str) -> Config:
    conf_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'test': TestConfig
    }

    cfg_class = conf_map.get(environment)

    if cfg_class is None:
        raise RuntimeError("Environment is not set")

    return cfg_class()
