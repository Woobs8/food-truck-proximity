from flask import request, jsonify, abort, make_response, current_app
from application.models import User, db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from application.views.authentication import get_token_from_header

class UserAPI(MethodView):
    """
    A class used to encapsulate the API for the /auth/user resource

    Methods
    -------
    get()
        implements the GET /auth/user endpoint

    """
    def get(self):
        """
        GET /auth/user endpoint returns user details if authenticated

        Parameters:
        - 

        Returns:
            str: JSON representation of user details
        """
        # get authentication token from request header
        auth_token = get_token_from_header()

        # token must be present
        if auth_token:
            try:
                # get user id from token payload
                payload = User.decode_auth_token(auth_token)
                user_id = payload['sub']

                # get user details from database
                user = User.query.filter_by(id=user_id).first()

                return make_response(jsonify(user.serialize()), 200)
            except Exception as e:
                current_app.logger.error('Error getting user details: %s', e)
                abort(500, 'Error getting user details')
        # if no token is present, return unsuccessful response
        else:
            abort(401, 'A valid token must be included')