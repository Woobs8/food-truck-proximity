import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius
import json


@pytest.mark.usefixtures('create_db', 'populate_user_db')
class TestPost():
    """
    Test cases for validating the POST endpoints of the application.
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    4. Populate user database with predefined elements
    """
    
    def test_post_truck(self, client, token):
        """
        Test the POST request with authentication to create a new FoodTruck resource element

        1. Login to acquire token
        2. Send POST request to foodtrucks with valid parameters
        3. Verify the status code as entry created
        4. Verify the attributes of the object returned in the response
        5. Verify the element inserted into the database
        """
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}

        post_data = {'name': 'Food Truck 1',
                    'latitude': 37.7201,
                    'longitude': -122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}
        
        ret = client.post('/foodtrucks', data=json.dumps(post_data), headers=headers)
        ret_data = ret.get_json()

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
        assert truck.user_id == 2


    def test_post_truck_unauthorized(self, client):
        """
        Test the POST request without authentication to create a new FoodTruck resource element

        1. Send POST request without authentication to foodtrucks with valid parameters
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
        ret_data = ret.get_json()

        # verify unathorized access response
        assert ret.status_code == 401


    def test_post_truck_bad_request(self, client, token):
        """
        Test the POST request to create a new FoodTruck resource element with different
        invalid parameters.

        1. Login to acquire token
        2. Send POST request to foodtrucks with missing longitude
        3. Verify the status code as bad request
        4. Send POST request to foodtrucks with wrong datatype for longitude
        5. Verify the status code as bad request
        6. Send POST request to foodtrucks with wrong mimetype in header
        7. Verify the status code as bad request
        """
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
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
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}
        ret = client.post('/foodtrucks', data=json.dumps(post_data), headers=headers)
        assert ret.status_code == 400

