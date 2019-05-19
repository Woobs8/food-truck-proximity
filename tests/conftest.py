import pytest
from application import create_app
from application.models import FoodTruck, db
from test_data import test_data

@pytest.fixture(scope='session', autouse=True)
def app():
    """
    A test fixture for automatically creating an instance of the flask application once for every test session
    """
    _app = create_app()
    return _app

@pytest.fixture(scope='class')
def class_db(app):
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
def populate_db(class_db):
    """
    A test fixture for populating the database with test data. 
    Will only run once per test class.
    """
    for e in test_data:
        truck=FoodTruck(
            name = e['name'],
            longitude = e['longitude'],
            latitude = e['latitude'],
            days_hours = e['days_hours'],
            food_items = e['food_items']
        )
        class_db.session.add(truck)
    class_db.session.commit()