from flask import request, jsonify, abort, make_response, current_app
from application.models import User, db, bcrypt
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from jwt.exceptions import PyJWTError


class UserLoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        # get the POST data
        post_data = request.get_json()

        # validate JSON request
        if not post_data:
            abort(400, 'Request must be JSON mimetype')
        if not 'username' in post_data or type(post_data['username']) != str:
            abort(400, "invalid or missing 'username' field")
        if not 'password' in post_data or type(post_data['password']) != str:
            abort(400, "invalid or missing 'password' field")

        # extract values from request
        username = post_data['username']
        password = post_data['password']

        # verify user data, generate token and return token to user
        try:
            # fetch user data from database
            user = User.query.filter_by(username=username).first()

            # verify that user exists and that password is correct
            if user and bcrypt.check_password_hash(user.password, password):
                token = user.encode_auth_token(user.id)
                if token:
                    response = {
                        'message': 'Successfully logged in',
                        'auth_token': token.decode()
                    }
                    return make_response(jsonify(response), 200)
            else:
                abort(404, 'Invalid credentials or user does not exist')
        except (SQLAlchemyError, PyJWTError, ValueError, ImportError) as e:
            current_app.logger.error('Error logging in username %s: %s', username, e)
            abort(500, 'Error logging in')