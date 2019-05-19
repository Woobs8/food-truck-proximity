import pytest
from application.models import FoodTruck
from test_data import test_location, test_radius
from haversine import haversine

# test values
name = 'Food Truck 1'
latitude = 37.7201
longitude = -122.3886
days_hours = 'Mon-Fri:8AM-2PM'
food_items = 'sandwiches'

@pytest.fixture(scope='module')
def new_food_truck():
    """
    A test fixture for creating a FoodTruck instance once per module
    """
    truck = FoodTruck(name=name,
            latitude=latitude,
            longitude=longitude,
            days_hours=days_hours,
            food_items=food_items)
    return truck

@pytest.mark.usefixtures('class_db', 'populate_db')
class TestModel():
    """
    Unit test the FoodTruck model class
    """

    def test_new_food_truck(self, new_food_truck):
        """
        Test the creation of a new FoodTruck instance

        1. Create FoodTruck instance with predefined values
        2. Verify the attributes of the created instance
        """
        assert new_food_truck.name == name
        assert new_food_truck.latitude == latitude
        assert new_food_truck.longitude == longitude
        assert new_food_truck.days_hours == days_hours
        assert new_food_truck.food_items == food_items

    def test_food_truck_serialize(self, new_food_truck):
        """
        Test the FoodTruck instance method serialize()
        
        1. Create FoodTruck instance with predefined values
        2. Serialize created instance
        3. Verify that returned object is type dict
        4. Verify key-value pairs in returned dict
        """
        truck = new_food_truck.serialize()
        assert type(truck) == dict
        assert truck['name'] == name
        assert truck['latitude'] == latitude
        assert truck['longitude'] == longitude
        assert truck['days_hours'] == days_hours
        assert truck['food_items'] == food_items

    def test_food_truck_radius_query(self, app):
        """
        Test the FoodTruck class method get_food_trucks_within_radius()
        
        1. Initialize application and database
        2. Populate database with predefined values from test_data.py
        3. Invoke method with predefined coordinates with known result
        4. Verify that the correct amount of elements are returned
        5. Verify that every returned element is within the radius
        """
        radius = app.config['DEFAULT_SEARCH_RADIUS']
        latitude = test_location[0]
        longitude = test_location[1]
        ret = FoodTruck.get_food_trucks_within_radius(longitude, latitude, radius)
        assert len(ret) == test_radius[radius]

        # every returned element should be within radius distance
        for e in ret:
            dist = haversine(latitude, longitude, e.latitude, e.longitude)
            assert dist <= radius