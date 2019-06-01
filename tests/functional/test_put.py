import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius
import json


@pytest.mark.usefixtures('create_db', 'populate_user_db', 'populate_food_truck_db')
class TestPut():
    """
    Test cases for validating the PUT endpoint of the application.
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    4. Populate user database with predefined elements
    3. Populate food truck database with predefined elements
    """

    def test_update_truck(self, client, token):
        """
        Test PUT request to update existing FoodTruck with valid authentication.

        1. Login to acquire token
        2. Send PUT request to foodtrucks with valid parameters
        3. Verify the status code as successful
        4. Verify the attributes of the object returned in the response
        5. Verify the element in the database
        """
        uuid = 1
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}

        put_data = {'name':'Food Truck 1',
                    'latitude':37.7201,
                    'longitude':-122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}
        
        ret = client.put('/foodtrucks/{}'.format(uuid), data=json.dumps(put_data), headers=headers)
        ret_data = ret.get_json()
        
        # validate response
        assert ret.status_code == 200
        assert ret_data['uuid'] == uuid
        assert ret_data['name'] == put_data['name']
        assert ret_data['latitude'] == put_data['latitude']
        assert ret_data['longitude'] == put_data['longitude']
        assert ret_data['days_hours'] == put_data['days_hours']
        assert ret_data['food_items'] == put_data['food_items']

        # validate database
        truck = FoodTruck.query.filter_by(uuid=uuid).first()
        assert truck.name == put_data['name']
        assert truck.latitude == put_data['latitude']
        assert truck.longitude == put_data['longitude']
        assert truck.days_hours == put_data['days_hours']
        assert truck.food_items == put_data['food_items']
        assert truck.user_id == 2


    def test_update_truck_unauthorized(self, client):
        """
        Test PUT request to update existing FoodTruck without authnetication.

        1. Send PUT request to foodtrucks without authentication
        2. Verify the status code as unauthorized
        """
        uuid = 1
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}

        put_data = {'name':'Food Truck 1',
                    'latitude':37.7201,
                    'longitude':-122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}
        
        ret = client.put('/foodtrucks/{}'.format(uuid), data=json.dumps(put_data), headers=headers)
        ret_data = ret.get_json()
        
        # validate response
        assert ret.status_code == 401


    def test_create_truck(self, client, token):
        """
        Test authenticated PUT request to create new FoodTruck with specific.

        1. Login to acquire token
        2. Send authenticated PUT request to foodtrucks with valid parameters and specific id
        3. Verify the status code as successful
        4. Verify the attributes of the object returned in the response
        5. Verify the element in the database
        """
        uuid = len(test_data)+1
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}

        put_data = {'name':'Food Truck 2',
                    'latitude':37.7201,
                    'longitude':-122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}
        
        ret = client.put('/foodtrucks/{}'.format(uuid), data=json.dumps(put_data), headers=headers)
        ret_data = ret.get_json()
        
        # validate response
        assert ret.status_code == 200
        assert ret_data['uuid'] == uuid
        assert ret_data['name'] == put_data['name']
        assert ret_data['latitude'] == put_data['latitude']
        assert ret_data['longitude'] == put_data['longitude']
        assert ret_data['days_hours'] == put_data['days_hours']
        assert ret_data['food_items'] == put_data['food_items']

        # validate database
        truck = FoodTruck.query.filter_by(uuid=uuid).first()
        assert truck.name == put_data['name']
        assert truck.latitude == put_data['latitude']
        assert truck.longitude == put_data['longitude']
        assert truck.days_hours == put_data['days_hours']
        assert truck.food_items == put_data['food_items']
        assert truck.user_id == 2


    def test_create_truck_unauthorized(self, client):
        """
        Test PUT request without authentication to create new FoodTruck with specific id.

        1. Send PUT request without authentication to foodtrucks with valid parameters and specific id
        2. Verify the status code as unauthorized
        """
        uuid = len(test_data)+1
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}

        put_data = {'name':'Food Truck 2',
                    'latitude':37.7201,
                    'longitude':-122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}
        
        ret = client.put('/foodtrucks/{}'.format(uuid), data=json.dumps(put_data), headers=headers)
        ret_data = ret.get_json()
        
        # validate response
        assert ret.status_code == 401


    def test_update_truck_bad_request(self, client, token):
        """
        Test PUT request to create new FoodTruck with different invalid parameters.

        1. Login to acquire token
        2. Send PUT request to foodtrucks with missing field in parameters
        3. Verify the status code as bad request
        4. Send PUT request to foodtrucks with wrong datatype for longitude
        5. Verify the status code as bad request
        6. Send PUT request to foodtrucks with wring mimetype in header
        7. Verify the status code as bad request
        """
        uuid = 1
        url = '/foodtrucks/{}'.format(uuid)
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}

        # missing field in data
        put_data = {'name':'Food Truck 1',
                    'latitude':37.7201,
                    #longitude missing
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}
        ret = client.put(url, data=json.dumps(put_data), headers=headers)
        assert ret.status_code == 400

        # wrong data type in field
        put_data['longitude'] = 'abc'
        ret = client.put(url, data=json.dumps(put_data), headers=headers)
        assert ret.status_code == 400        

        # wrong mimetype in header
        put_data['longitude'] = -122.3886
        mimetype = 'text/html'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}
        ret = client.put(url, data=json.dumps(put_data), headers=headers)
        assert ret.status_code == 400
