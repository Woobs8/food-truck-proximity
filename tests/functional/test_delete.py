import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius
import json


@pytest.mark.usefixtures('create_db', 'populate_user_db', 'populate_food_truck_db')
class TestDelete():
    """
    Test cases for validating the DELETE endpoint of the application.
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    4. Populate user database with predefined elements
    3. Populate food truck database with predefined elements
    """

    def test_delete_existing_truck(self, client, token):
        """
        Test DELETE request to delete existing FoodTruck.

        1. Login to acquire token
        2. Send DELETE request to foodtruck with specific id
        3. Verify the status code as successful
        4. Verify that the id does not exist in the database
        """
        uuid = 1
        headers = {'Authorization': 'Bearer ' + token}
        ret = client.delete('/foodtrucks/{}'.format(uuid), headers=headers)
        assert ret.status_code == 200

        # validate database
        truck = FoodTruck.query.filter_by(uuid=uuid).first()
        assert not truck


    def test_delete_nonexisting_truck_(self, client, token):
        """
        Test DELETE request to delete nonexisting FoodTruck.

        1. Login to acquire token
        2. Send DELETE request to foodtruck with nonexisting id
        3. Verify the status code as successful
        """
        uuid = len(test_data)+1
        headers = {'Authorization': 'Bearer ' + token}
        ret = client.delete('/foodtrucks/{}'.format(uuid), headers=headers)
        assert ret.status_code == 200