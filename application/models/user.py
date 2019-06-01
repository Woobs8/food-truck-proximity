from flask import current_app
from . import db, bcrypt
import datetime
import jwt


class User(db.Model):
    """
    A class used to encapsulate User database model

    Attributes
    ----------
    id (int)
        Unique identifer for user (primary key for DB)

    username (string)
        Unique name of the user
    
    password (string)
        Hashed password of the user
    
    admin (bool)
        Boolean denoting whether the user has admin permissions

    Methods
    -------
    serialize
        Returns a dictionary representation of a class instance

    encode_auth_token(user_id)
        Generates a JSON web token based on the user_id and encodes it
    
    decode_auth_token(token)
        Decodes the supplied token and returns the token payload
    """
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


    def serialize(self):
        """
        Returns a dictionary representation of a class instance
        """
        return {'user_id': self.id,
                'username': self.username,
                'admin': self.admin,
                'registered_on': self.registered_on}


    @classmethod
    def is_admin(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        return user.admin

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates and encodes a JSON web token with the user_id

        Parameters:
            user_id (int): unique user id

        Returns:
            Bytes: encoded JSON web token
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
        Decodes and returns the payload in a JSON web token 

        Parameters:
            token (Bytes): a JSON web token containing user info

        Returns:
            dict: token payload
        """
        try:
            return jwt.decode(token, 
                            current_app.config.get('SECRET_KEY'),
                            algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return 'Signature expired.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'