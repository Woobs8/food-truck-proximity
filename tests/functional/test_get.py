import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius


@pytest.mark.usefixtures('create_db')
class TestGetEmptyDB():
    """
    Test cases for validating the GET endpoints of the application with an 
    empty database to ensure every application endpoint can handle an empty database. 
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    """

    def test_get_root(self, client):
        """
        Test the GET request to the application root endpoint

        1. Send GET request to application root
        2. Verify the status code as successful
        3. Verify the metadata
        """
        ret = client.get('/')
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']
        assert data['entries'] == 0


    def test_get_all_empty_db(self, client):
        """
        Test the GET request to the foodtrucks root endpoint

        1. Send GET request to foodtrucks root
        2. Verify the status code as successful
        3. Verify that no elements are returned
        """
        ret = client.get('/foodtrucks')
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']
        assert len(data) == 0


    def test_get_truck_by_id_empty_db(self, client):
        """
        Test the GET request to foodtrucks with specific id

        1. Send GET request to foodtrucks/<id>
        2. Verify the status code as successful
        3. Verify that no elements are returned
        """
        ret = client.get('/foodtrucks/1')
        assert ret.status_code == 200
        data = ret.get_json()
        assert len(data) == 0


    def test_get_truck_by_name_empty_db(self, client):
        """
        Test the GET request to foodtrucks with foodtrucks searched by name

        1. Send GET request to foodtrucks/name/<needle>
        2. Verify the status code as successful
        3. Verify that no elements are returned
        """
        name = test_name[0]
        ret = client.get('/foodtrucks/name/{}'.format(name))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']
        assert len(data) == 0


    def test_get_truck_by_item_empty_db(self, client):
        """
        Test the GET request to foodtrucks with foodtrucks searched by item

        1. Send GET request to foodtrucks/items/<needle>
        2. Verify the status code as successful
        3. Verify that no elements are returned
        """
        item = test_item[0]
        ret = client.get('/foodtrucks/items/{}'.format(item))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']
        assert len(data) == 0


    def test_get_truck_by_location_empty_db(self, client):
        """
        Test the GET request to foodtrucks nearby location

        1. Send GET request to foodtrucks/location/<params> with a predefined test location
        2. Verify the status code as successful
        3. Verify that no elements are returned
        """
        lat = test_location[0]
        lon = test_location[1]

        ret = client.get('/foodtrucks/location?longitude={}&latitude={}'.format(lon,lat))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']
        assert len(data) == 0


@pytest.mark.usefixtures('create_db', 'populate_db')
class TestGet():
    """
    Test cases for validating the GET endpoints of the application with a populated database. 
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    3. Populate database with predefined elements
    """

    def test_get_root(self, client):
        """
        Test the GET request to the application root endpoint

        1. Send GET request to application root
        2. Verify the status code as successful
        3. Verify the metadata against the predefined database elements
        """
        ret = client.get('/')
        assert ret.status_code == 200
        assert ret.get_json()['foodtrucks']['entries'] == len(test_data)


    def test_get_all(self, client):
        """
        Test the GET request to foodtrucks root endpoint

        1. Send GET request to foodtrucks root
        2. Verfiy the status code as successful
        3. Verify that the correct amount of elements is returned
        """
        ret = client.get('/foodtrucks')
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']
        assert len(data) == len(test_data)


    def test_get_truck_by_id(self, client):
        """
        Test the GET request to foodtrucks with specific id

        1. Send GET request to foodtrucks/<id>
        2. Verify the status code as successful
        3. Verify that the returned elements matches its predefined counterpart
        4. Repeat for every element
        """
        # fetch and validate every truck in test data individually
        for i, e in enumerate(test_data):
            ret = client.get('/foodtrucks/{}'.format(i+1))
            assert ret.status_code == 200
            data = ret.get_json()
            
            assert data['uuid'] == i+1
            assert data['name'] == e['name']
            assert data['latitude'] == e['latitude']
            assert data['longitude'] == e['longitude']
            assert data['days_hours'] == e['days_hours']
            assert data['food_items'] == e['food_items']


    def test_get_truck_by_id_not_found(self, client):
        """
        Test the GET request to foodtrucks with nonexisting id

        1. Send GET request to foodtrucks/<id> with nonexisting id
        2. Verify the status code as successful
        3. Verify that no elements are returned
        """
        uuid = len(test_data)+1
        ret = client.get('/foodtrucks/{}'.format(uuid))
        assert ret.status_code == 200
        data = ret.get_json()
        assert len(data) == 0


    def test_get_truck_by_name_lowercase(self, client):
        """
        Test the GET request to foodtrucks searched by lowercase name

        1. Send GET request to foodtrucks/name/<needle> with lowercase name
        2. Verify the status code as successful
        3. Verify that the correct amount of elements is returned
        4. Verify that the name attribute of every returned element contains needle substring
        """
        name = test_name[0].lower()
        ret = client.get('/foodtrucks/name/{}'.format(name))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']

        # number of returnes items should match expected
        assert len(data) == test_name[1]

        # every returned element should contain substring name
        for e in data:
            assert name in e['name'].lower()


    def test_get_truck_by_name_uppercase(self, client):
        """
        Test the GET request to foodtrucks searched by uppercase name

        1. Send GET request to foodtrucks/name/<needle> with uppercase needle
        2. Verify the status code as successful
        3. Verify that the correct amount of elements is returned
        4. Verify that the name attribute of every returned element contains needle substring
        """
        name = test_name[0].upper()
        ret = client.get('/foodtrucks/name/{}'.format(name))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']

        # number of returnes items should match expected
        assert len(data) == test_name[1]

        # every returned element should contain substring name
        for e in data:
            assert name in e['name'].upper()


    def test_get_truck_by_item_lowercase(self, client):
        """
        Test the GET request to foodtrucks searched by lowercase food items

        1. Send GET request to foodtrucks/items/<needle> with lowercase needle
        2. Verify the status code as successful
        3. Verify that the correct amount of elements is returned
        4. Verify that the food_items attribute of every returned element contains needle substring
        """
        item = test_item[0].lower()
        ret = client.get('/foodtrucks/items/{}'.format(item))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']

        # number of returnes items should match expected
        assert len(data) == test_item[1]

        # every returned element should contain substring item
        for e in data:
            assert item in e['food_items'].lower()


    def test_get_truck_by_item_uppercase(self, client):
        """
        Test the GET request to foodtrucks searched by uppercase food items

        1. Send GET request to foodtrucks/items/<needle> with uppercase needle
        2. Verify the status code as successful
        3. Verify that the correct amount of elements is returned
        4. Verify that the food_items attribute of every returned element contains needle substring
        """
        item = test_item[0].upper()
        ret = client.get('/foodtrucks/items/{}'.format(item))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']

        # number of returnes items should match expected
        assert len(data) == test_item[1]

        # every returned element should contain substring item
        for e in data:
            assert item in e['food_items'].upper()


    def test_get_truck_by_location(self, client):
        """
        Test the GET request to foodtrucks nearby location

        1. Send GET request to foodtrucks/location/<params> with a predefined test location
        2. Verify the status code as successful
        3. Verify that the correct amount of elements is returned
        4. Verify that every returned element is within the radius
        """
        lat = test_location[0]
        lon = test_location[1]

        # test with different radius
        for radius, (count, ids) in test_radius.items():
            ret = client.get('/foodtrucks/location?longitude={}&latitude={}&radius={}'.format(lon,lat, radius))
            assert ret.status_code == 200
            data = ret.get_json()['foodtrucks']

            # number of returnes items should match expected
            assert len(data) == count

            # verify that the correct trucks are returned, in the correct order
            for i, e in enumerate(data):
                assert test_radius[radius][1][i] == e['uuid']


    def test_get_truck_by_location_bad_request(self, client):
        """
        Test the GET request to foodtrucks nearby location with missing parameters

        1. Send GET request to foodtrucks/location/<params> with missing latitude
        2. Verify the status code as bad request
        3. Send GET request to foodtrucks/location/<params> with missing longitude
        4. Verify the status code as bad request
        """
        lat = test_location[0]
        lon = test_location[1]

        # omit latitude
        ret = client.get('/foodtrucks/location?longitude={}&latitude='.format(lon))
        assert ret.status_code == 400

        # omit longitude
        ret = client.get('/foodtrucks/location?longitude=&latitude={}'.format(lat))
        assert ret.status_code == 400


    def test_get_truck_by_location_and_name(self, app, client):
        """
        Test the GET request to foodtrucks nearby location filtered by a name search

        1. Send GET request to foodtrucks/location/<params> with a predefined test location
            and name search needle
        2. Verify the status code as successful
        3. Verify that the correct amount of elements is returned
        4. Verify that every returned element is within the radius
        5. Verify that the name attribute of every returned element contains substring needle
        """
        lat = test_location[0]
        lon = test_location[1]
        name = test_name[0]

        ret = client.get('/foodtrucks/location?longitude={}&latitude={}&name={}'.format(lon,lat,name))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']

        # number of returned entries should match expected
        assert len(data) == test_name[1]

        # verify that the correct trucks are returned, in the correct order
        for i, e in enumerate(data):
            assert test_name[2][i] == e['uuid']


    def test_get_truck_by_location_and_item(self, app, client):
        """
        Test the GET request to foodtrucks nearby location filtered by an item search

        1. Send GET request to foodtrucks/location/<params> with a predefined test location
            and item search needle
        2. Verify the status code as successful
        3. Verify that the correct amount of elements is returned
        4. Verify that every returned element is within the radius
        5. Verify that the food_items attribute of every returned element contains substring needle
        """
        lat = test_location[0]
        lon = test_location[1]
        item = test_item[0]

        ret = client.get('/foodtrucks/location?longitude={}&latitude={}&item={}'.format(lon,lat,item))
        assert ret.status_code == 200
        data = ret.get_json()['foodtrucks']

        # number of returned entries should match expected
        assert len(data) == test_item[1]

        # verify that the correct trucks are returned, in the correct order
        for i, e in enumerate(data):
            assert test_item[2][i] == e['uuid']