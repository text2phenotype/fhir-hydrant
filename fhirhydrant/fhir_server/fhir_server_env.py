from pathlib import Path

from text2phenotype.constants.environment import Environment, EnvironmentVariable


class FhirServerEnv(Environment):
    config_file_dir = Path(__file__).parent

    APPLICATION_NAME = Environment.APPLICATION_NAME
    APPLICATION_NAME.value = 'FHIR Hydrant'

    FLASK_ENV = EnvironmentVariable(name='MDL_FHIR_FLASK_ENV', legacy_name='FLASK_ENV')
    REDIRECT_URI = EnvironmentVariable(name='MDL_FHIR_REDIRECT_URI', legacy_name='REDIRECT_URI', value='https://azurehealthcareapis.com')
    SCOPE = EnvironmentVariable(name='MDL_FHIR_SCOPE',
                                legacy_name='SCOPE',
                                value='https://azurehealthcareapis.com/user_impersonation offline_access')
    AUTH_BASE_URL = EnvironmentVariable(name='MDL_FHIR_AUTH_BASE_URL',
                                        legacy_name='AUTH_BASE_URL',
                                        value='https://login.microsoftonline.com/')

    # default is 500 MB
    MAX_CONTENT_LENGTH = EnvironmentVariable(name='MDL_FHIR_MAX_CONTENT_LENGTH',
                                             legacy_name='MAX_CONTENT_LENGTH',
                                             value=500 * 1024 * 1024)

    TENANT_ID = EnvironmentVariable(name='MDL_FHIR_TENANT_ID', legacy_name='TENANT_ID')
    CLIENT_ID = EnvironmentVariable(name='MDL_FHIR_CLIENT_ID', legacy_name='CLIENT_ID')
    CLIENT_SECRET = EnvironmentVariable(name='MDL_FHIR_CLIENT_SECRET', legacy_name='CLIENT_SECRET')
    AZURE_USERNAME = EnvironmentVariable(name='MDL_FHIR_AZURE_USERNAME', legacy_name='AZURE_USERNAME')
    PASSWORD = EnvironmentVariable(name='MDL_FHIR_PASSWORD', legacy_name='PASSWORD')
    API_URL = EnvironmentVariable(name='MDL_FHIR_API_URL', legacy_name='API_URL')

    APM_SERVICE_NAME = EnvironmentVariable(name='MDL_FHIR_APM_SERVICE_NAME',
                                           legacy_name='APM_SERVICE_NAME',
                                           value='Text2phenotype FHIR Hydrant')
