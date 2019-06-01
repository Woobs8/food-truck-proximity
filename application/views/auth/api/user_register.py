from flask import request, jsonify, abort, make_response, current_app
from application.models import User, db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView

class UserRegisterAPI(MethodView):
    """
    User Registration Resource
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

        # add user if no user with same username exists
        user = User.query.filter_by(username=username).first()
        if not user:
            try:
                user = User(
                    username=username,
                    password=password
                )

                # add the user to the database
                db.session.add(user)
                db.session.commit()

                return make_response(jsonify({'message': 'User successfully registered'}), 201)
            except SQLAlchemyError as e:
                db.session.rollback()
                current_app.logger.error('error registering username %s: %s', 
                                        username, e)
                abort(500, 'Error registering user')
        else:
            return make_response(jsonify({'message': 'User is already registered'}), 202)