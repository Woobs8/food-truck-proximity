from flask import current_app
from . import db, bcrypt
import datetime
import jwt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)


    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = bcrypt.generate_password_hash(password, 
                        current_app.config['BCRYPT_LOG_ROUNDS']).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        now = datetime.datetime.utcnow()
        try:
            payload = {
                'sub': user_id,
                'exp': now + datetime.timedelta(days=0, seconds=current_app.config['AUTH_TOKEN_EXP_TIME_SEC']),
                'iat': now
            }

            return jwt.encode(payload,
                            current_app.config.get('SECRET_KEY'),
                            algorithm='HS256')
        except jwt.exceptions.PyJWTError as e:
            return e


    @staticmethod
    def decode_auth_token(token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            return jwt.decode(token, 
                            current_app.config.get('SECRET_KEY'),
                            algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return 'Signature expired.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'