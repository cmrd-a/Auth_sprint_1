from functools import wraps
from http import HTTPStatus

from apiflask import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from auth_app.extensions import redis_client, jwt


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token_in_redis = redis_client.get(jti)
    return token_in_redis is not None


def permissions_required(permisssions: [str]):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if set(permisssions) & set(claims["permissions"]):
                return fn(*args, **kwargs)
            else:
                return abort(HTTPStatus.FORBIDDEN, message="Not enough permissions")

        return decorator

    return wrapper
