from functools import wraps

from flask import abort
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(*roles: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in roles:
                abort(403, description="Forbidden")
            return fn(*args, **kwargs)

        return wrapper

    return decorator
