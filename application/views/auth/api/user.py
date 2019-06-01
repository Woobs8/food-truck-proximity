from flask import request, jsonify, abort, make_response, current_app
from application.models import User, db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView

class UserAPI(MethodView):
    """
    User Resource
    """
    def get(self):
        # get auth token from request header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            # catch malformed bearer token errors
            except IndexError:
                abort(401, 'Malformed bearer token')
        else:
            auth_token = None
        
        # token must be present
        if auth_token:
            try:
                # get user id from token payload
                payload = User.decode_auth_token(auth_token)
                user_id = payload['sub']

                # get user details from database
                user = User.query.filter_by(id=user_id).first()
                response = {
                    'user': {
                        'user_id': user.id,
                        'username': user.username,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return make_response(jsonify(response), 200)
            except Exception as e:
                current_app.logger.error('Error getting user details: %s', e)
                abort(500, 'Error getting user details')
        # if no token is present, return unsuccessful response
        else:
            abort(401, 'A valid token must be included')