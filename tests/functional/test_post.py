import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius
from haversine import haversine
import json

@pytest.mark.usefixtures('class_db')
class TestPost():
    """
    Test cases for validating the POST endpoints of the application.
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    """

    def test_post_root(self, client):
        """
        Test the POST request to the application root endpoint

        1. Send POST request to the application root
        2. Verify the status code as successful
        3. Verify the metadata against the predefined database elements
        """
        ret = client.post('/')
        assert ret.status_code == 200
        data = ret.get_json()
        assert data['entries'] == 0
    
    def test_post_truck(self, client):
        """
        Test the POST request to create a new FoodTruck resource element

        1. Send POST request to foodtrucks with valid parameters
        2. Verify the status code as entry created
        3. Verify the attributes of the object returned in the response
        4. Verify the element inserted into the database
        """
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}

        post_data = {'name': 'Food Truck 1',
                    'latitude': 37.7201,
                    'longitude': -122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}
        
        ret = client.post('/foodtrucks', data=json.dumps(post_data), headers=headers)
        ret_data = ret.get_json()['food_truck']

        # validate response
        assert ret.status_code == 201
        assert ret_data['name'] == post_data['name']
        assert ret_data['latitude'] == post_data['latitude']
        assert ret_data['longitude'] == post_data['longitude']
        assert ret_data['days_hours'] == post_data['days_hours']
        assert ret_data['food_items'] == post_data['food_items']

        # validate database
        truck_id = ret_data['uuid']
        truck = FoodTruck.query.filter_by(uuid=truck_id).first()
        assert truck.name == post_data['name']
        assert truck.latitude == post_data['latitude']
        assert truck.longitude == post_data['longitude']
        assert truck.days_hours == post_data['days_hours']
        assert truck.food_items == post_data['food_items']

    def test_post_truck_bad_request(self, client):
        """
        Test the POST request to create a new FoodTruck resource element with different
        invalid parameters.

        1. Send POST request to foodtrucks with missing longitude
        2. Verify the status code as bad request
        3. Send POST request to foodtrucks with wrong datatype for longitude
        4. Verify the status code as bad request
        5. Send POST request to foodtrucks with wrong mimetype in header
        6. Verify the status code as bad request
        """
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}

        # missing field in data
        post_data = {'name': 'Food Truck 1',
            'latitude': 37.7201,
            # longitude missing
            'days_hours':'Mon-Fri:8AM-2PM',
            'food_items':'sandwiches'}
        ret = client.post('/foodtrucks', data=json.dumps(post_data), headers=headers)
        assert ret.status_code == 400

        # wrong data type in field
        post_data['longitude'] = 'abc'
        ret = client.post('/foodtrucks', data=json.dumps(post_data), headers=headers)
        assert ret.status_code == 400        

        # wrong mimetype in header
        post_data['longitude'] = -122.3886
        mimetype = 'text/html'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}
        ret = client.post('/foodtrucks', data=json.dumps(post_data), headers=headers)
        assert ret.status_code == 400

