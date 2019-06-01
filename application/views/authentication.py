from flask import request, abort
from application.models import User
import jwt

def get_token_from_header():
    """
    Extracts the authentication header from a Flask request

    Returns:
        bytes: token if present, othersise None
    """
    # get auth token from request header
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
        # catch malformed bearer token errors
        except IndexError:
            abort(401, 'Malformed bearer token')
    else:
        token = None
    
    return token


def get_user_id_from_token(token):
    """
    Decodes token and returns the user id in the payload

    Returns:
        int: unique id of the user
    """
    try:
        payload = User.decode_auth_token(token)
        return payload['sub']
    except IndexError:
        abort(401, 'could not authenticate token')
    