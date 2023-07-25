from pathlib import Path

from text2phenotype.constants.environment import Environment, EnvironmentVariable


class FhirClientEnv(Environment):
    config_file_dir = Path(__file__).parent

    API_BASE = EnvironmentVariable(name='MDL_FHIR_API_BASE',
                                   legacy_name='FHIR_API_BASE',
                                   value='http://0.0.0.0:5000')
    TENANT_ID = EnvironmentVariable(name='MDL_FHIR_TENANT_ID',
                                    legacy_name='TENANT_ID',
                                    value='4a2074e8-3007-4341-b8eb-80f1448985de')
