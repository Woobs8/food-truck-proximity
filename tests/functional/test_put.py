import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius
import json

@pytest.mark.usefixtures('class_db', 'populate_db')
class TestPut():
    """
    Test cases for validating the PUT endpoint of the application.
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    3. Populate database with predefined elements
    """

    def test_update_truck(self, client):
        """
        Test PUT request to update existing FoodTruck.

        1. Send PUT request to foodtrucks with valid parameters
        2. Verify the status code as successful
        3. Verify the attributes of the object returned in the response
        4. Verify the element in the database
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

    def test_create_truck(self, client):
        """
        Test PUT request to create new FoodTruck with specific id.

        1. Send PUT request to foodtrucks with valid parameters and specific id
        2. Verify the status code as successful
        3. Verify the attributes of the object returned in the response
        4. Verify the element in the database
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

    def test_update_truck_bad_request(self, client):
        """
        Test PUT request to create new FoodTruck with different invalid parameters.

        1. Send PUT request to foodtrucks with missing field in parameters
        2. Verify the status code as bad request
        3. Send PUT request to foodtrucks with wrong datatype for longitude
        4. Verify the status code as bad request
        5. Send PUT request to foodtrucks with wring mimetype in header
        6. Verify the status code as bad request
        """
        uuid = 1
        url = '/foodtrucks/{}'.format(uuid)
        mimetype = 'application/json'
        headers = {'Content-Type': mimetype,
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
        headers = {'Content-Type': mimetype,
                    'Accept': mimetype}
        ret = client.put(url, data=json.dumps(put_data), headers=headers)
        assert ret.status_code == 400

