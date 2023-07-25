from functools import wraps
from flask import abort, request

from fhirhydrant.fhir_server.fhir_server_env import FhirServerEnv


def check_tenant_id(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        request_tenant_id = request.headers.get('tenantId')
        if FhirServerEnv.TENANT_ID.value != request_tenant_id:
            abort(403)
        return handler(*args, **kwargs)
    return wrapper
