import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius
from flask import Request, current_app


@pytest.mark.usefixtures('create_db', 'populate_food_truck_db')
class TestMutation():
    """
    Test cases for validating the GraphQL mutation endpoint createFoodTruck.

    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    4. Populate user database with predefined elements
    """


    def test_create_food_truck(self, graphql_client, token):
        """
        Test the GraphQL mutation createFoodTruck with authentication and valid parameters.

        1. Login to acquire token
        2. Send query to /graphql endpoint
        3. Verify the attributes of the object returned in the response
        4. Verify the element inserted into the database
        """
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}

        truck_data = {'name': 'Food Truck 1',
                    'latitude': 37.7201,
                    'longitude': -122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}

        with current_app.test_request_context('/graphql', headers=headers) as request: 
            executed = graphql_client.execute(''' mutation {
                                                    createFoodTruck(name: "Food Truck 1", 
                                                    latitude: 37.7201, 
                                                    longitude: -122.3886, 
                                                    daysHours: "Mon-Fri:8AM-2PM", 
                                                    foodItems: "sandwiches") {
                                                        foodTruck {
                                                        uuid,
                                                        name,
                                                        latitude,
                                                        longitude,
                                                        daysHours,
                                                        foodItems}
                                                    } } ''', context=request)

        # validate response
        data = executed['data']['createFoodTruck']['foodTruck']
        assert data['name'] == truck_data['name']
        assert data['latitude'] == truck_data['latitude']
        assert data['longitude'] == truck_data['longitude']
        assert data['daysHours'] == truck_data['days_hours']
        assert data['foodItems'] == truck_data['food_items']

        # validate database
        truck_id = data['uuid']
        truck = FoodTruck.query.filter_by(uuid=truck_id).first()
        assert truck.name == truck_data['name']
        assert truck.latitude == truck_data['latitude']
        assert truck.longitude == truck_data['longitude']
        assert truck.days_hours == truck_data['days_hours']
        assert truck.food_items == truck_data['food_items']
        assert truck.user_id == 2


    def test_update_food_truck(self, graphql_client, token):
        """
        Test the GraphQL mutation updateFoodTruck with authentication and valid parameters.

        1. Login to acquire token
        2. Send query to /graphql endpoint
        3. Verify the attributes of the object returned in the response
        4. Verify the element inserted into the database
        """
        uuid = 1
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}

        truck_data = {'name': 'Food Truck 1',
                    'latitude': 37.7201,
                    'longitude': -122.3886,
                    'days_hours':'Mon-Fri:8AM-2PM',
                    'food_items':'sandwiches'}

        with current_app.test_request_context('/graphql', headers=headers) as request: 
            executed = graphql_client.execute(''' mutation {
                                                    updateFoodTruck( truckId: 1,
                                                    name: "Food Truck 1", 
                                                    latitude: 37.7201, 
                                                    longitude: -122.3886, 
                                                    daysHours: "Mon-Fri:8AM-2PM", 
                                                    foodItems: "sandwiches") {
                                                        foodTruck {
                                                        uuid,
                                                        name,
                                                        latitude,
                                                        longitude,
                                                        daysHours,
                                                        foodItems}
                                                    } } ''', context=request)

        # validate response
        data = executed['data']['updateFoodTruck']['foodTruck']
        assert data['uuid'] == str(uuid)
        assert data['name'] == truck_data['name']
        assert data['latitude'] == truck_data['latitude']
        assert data['longitude'] == truck_data['longitude']
        assert data['daysHours'] == truck_data['days_hours']
        assert data['foodItems'] == truck_data['food_items']

        # validate database
        truck = FoodTruck.query.filter_by(uuid=uuid).first()
        assert truck.name == truck_data['name']
        assert truck.latitude == truck_data['latitude']
        assert truck.longitude == truck_data['longitude']
        assert truck.days_hours == truck_data['days_hours']
        assert truck.food_items == truck_data['food_items']
        assert truck.user_id == 2


    def test_delete_food_truck(self, graphql_client, token):
        """
        Test the GraphQL mutation deleteFoodTruck with authentication and valid parameters.

        1. Login to acquire token
        2. Send query to /graphql endpoint
        3. Verify the attributes of the object returned in the response
        4. Verify the element inserted into the database
        """
        uuid = 1
        mimetype = 'application/json'
        headers = {'Authorization': 'Bearer ' + token,
                    'Content-Type': mimetype,
                    'Accept': mimetype}

        with current_app.test_request_context('/graphql', headers=headers) as request: 
            executed = graphql_client.execute(''' mutation {
                                                    deleteFoodTruck( truckId: 1) {
                                                        foodTruck {
                                                        uuid,
                                                        name,
                                                        latitude,
                                                        longitude,
                                                        daysHours,
                                                        foodItems}
                                                    } } ''', context=request)

        # validate response
        data = executed['data']['deleteFoodTruck']['foodTruck']
        assert data['uuid'] == str(uuid)

        # validate database
        truck = FoodTruck.query.filter_by(uuid=uuid).first()
        assert not truck