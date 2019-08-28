import pytest
from application import create_app
from application.models import FoodTruck, User, db
from test_data import test_data, test_users
import json
from graphene.test import Client
from application.views.foodtrucks.api.GraphQL import schema


@pytest.fixture(scope='session', autouse=True)
def app():
    """
    A test fixture for automatically creating an instance of the flask application once for every test session
    """
    _app = create_app()
    return _app


@pytest.fixture(scope='class')
def create_db(app):
    """
    A test fixture for creating a database table, with the schema defined in model, 
    once per test class and deleted after exiting the scope of a test class.
    """
    db.app = app
    with app.app_context():
        db.create_all()
        yield db
        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    """
    A test fixture for creating a test client instance for every test case
    """
    return app.test_client()


@pytest.fixture(scope='class')
def populate_user_db(create_db):
    """
    A test fixture for populating the user database with test data. 
    Will only run once per test class.
    """
    for e in test_users:
        user = User(
            username = e['username'],
            password = e['password'],
            admin = e['admin']
        )
        create_db.session.add(user)
    create_db.session.commit()


@pytest.fixture(scope='class')
def populate_food_truck_db(create_db, populate_user_db):
    """
    A test fixture for populating the food truck database with test data. 
    Will only run once per test class.
    """
    for e in test_data:
        truck = FoodTruck(
            name = e['name'],
            longitude = e['longitude'],
            latitude = e['latitude'],
            days_hours = e['days_hours'],
            food_items = e['food_items'],
            user_id = 2
        )
        create_db.session.add(truck)
    create_db.session.commit()


@pytest.fixture()
def token(app, client):
    """
    A test fixture for logging in and acquiring token
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
    return data['auth_token']
    

@pytest.fixture()
def graphql_client():
    """
    A test fixture for creating a GraphQL test client
    """
    return Client(schema)