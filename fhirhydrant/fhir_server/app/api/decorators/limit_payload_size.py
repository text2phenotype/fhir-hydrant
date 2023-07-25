from functools import wraps
from flask import abort, request


def limit_payload_size(max_size):
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            size: int = request.content_length
            if (size or 0) > max_size:
                abort(413)
            return handler(*args, **kwargs)
        return wrapper
    return decorator
