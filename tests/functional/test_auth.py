import pytest
from application.models import User
from test_data import test_users
import json


@pytest.mark.usefixtures('create_db', 'populate_user_db')
class TestAuthentication():
    """
    Test cases for validating the authentication endpoints of the application.
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database tables
    3. Populate user database with predefined elements
    """


    def test_registration(self, client):
        """
        Test POST request to register user

        1. Send POST request to register new user
        2. Verify the status code as successful
        3. Verify that the user is added to the database
        4. Send POST request to register existing user
        5. Verify the status code as successful
        6. Verify that the user exists in the database
        """
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}

        username = 'user2'
        password = 'test'
        post_data = {'username': username,
                    'password': password}
        
        ret = client.post('/auth/register', data=json.dumps(post_data), headers=headers)
        assert ret.status_code == 201
        user = User.query.filter_by(username=username).first()
        assert user

        ret = client.post('/auth/register', data=json.dumps(post_data), headers=headers)
        assert ret.status_code == 202
        user = User.query.filter_by(username=username).first()
        assert user


    def test_registered_user_login(self, client):
        """
        Test POST request to login registered user

        1. Send POST request to login as registered user
        2. Verify the status code as successful
        3. Verify the response message
        4. Verify that a token is returned
        """
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}
        login_cred = {
            'username': test_users[1]['username'],
            'password': test_users[1]['password']
        }
        ret = client.post('/auth/login', data=json.dumps(login_cred), headers=headers)
        assert ret.status_code == 200
        data = ret.get_json()
        assert data['message'] == 'Successfully logged in'
        assert data['auth_token']


    def test_invalid_credentials_user_login(self, client):
        """
        Test POST request to login registered user with invalid credentials

        1. Send POST request to login as registered user with invalid credentials
        2. Verify the status code as uinsuccessful
        """
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}
        login_cred = {
            'username': test_users[1]['username'],
            'password': test_users[1]['password']+'X'   # append X to make password invalid
        }
        ret = client.post('/auth/login', data=json.dumps(login_cred), headers=headers)
        assert ret.status_code == 404


    def test_non_registered_user_login(self, client):
        """
        Test POST request to login non-registered user

        1. Send POST request to login as non-registered user
        2. Verify the status code as unsuccessful
        """
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}
        login_cred = {
            'username': 'non-existing user',
            'password': 'test'
        }
        ret = client.post('/auth/login', data=json.dumps(login_cred), headers=headers)
        assert ret.status_code == 404