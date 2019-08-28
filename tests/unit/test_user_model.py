import pytest
from application.models import User, bcrypt

@pytest.mark.usefixtures('create_db')
class TestUser():

    """
    Unit test the User model class
    """

    def test_new_user(self):
        """
        Test the creation of a new User instance

        1. Create a non-admin User instance with predefined values
        2. Verify the attributes of the created instance
        3. Create an admin User instance with predefined values
        4. Verify the attributes of the created instance
        """
        username = 'admin'
        password = "1234321"

        # non-admin user
        user = User(username, password)
        assert user.username == username
        assert bcrypt.check_password_hash(user.password, password)
        assert user.admin == False

        # adnin user
        user = User(username, password, admin=True)
        assert user.username == username
        assert bcrypt.check_password_hash(user.password, password)
        assert user.admin == True


    def test_encode_auth_token(self):
        user_id = 1
        token = User.encode_auth_token(user_id)
        assert isinstance(token, bytes)


    def test_decode_auth_token(self):
        user_id = 1
        token = User.encode_auth_token(user_id)
        assert isinstance(token, bytes)
        payload = User.decode_auth_token(token)
        assert payload['sub'] == user_id