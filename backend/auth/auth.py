import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from exceptions import AuthError
from config import (
    AUTH0_DOMAIN,
    ALGORITHMS,
    API_AUDIENCE
)


def get_token_auth_header():
    auth = request.headers.get('Authorization')
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError("token is expired", 401)
        except jwt.JWTClaimsError:
            raise AuthError("invalid_claims", 401)
        except Exception as e:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

    raise AuthError("Unable to find appropriate key", 401)


def check_permissions(permission, payload):
    permissions = payload.get("permissions")
    if permissions is None:
        raise AuthError({
            "code": "invalid_payload",
            "description": "permission missing in payload"
            }, 401)

    if permission not in permissions:
        raise AuthError({
            "code": "invalid_payload",
            "description": "Permission not found."
            }, 401)

    return True


def requires_scope(required_scope):
    """
    Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False

def requires_auth(permission=""):

    def requires_auth_decorator(f):
        """ Determines if the Access Token is valid """
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        
        return wrapper

    return requires_auth_decorator
