import pytest
from application.models import FoodTruck
from test_data import test_data, test_name, test_item, test_location, test_radius


@pytest.mark.usefixtures('create_db')
class TestQueryEmptyDB():
    """
    Test cases for validating the GraphQL query endpoint of the application with an 
    empty database.
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    """

    def test_query_truck(self, graphql_client):
        """
        Test a query for all fields of a truck

        1. Send query to /graphql endpoint
        2. Verify the returned data
        """
        executed = graphql_client.execute('''{  
                                                allFoodTrucks {
                                                    edges {
                                                        node { id }
                                                    }   
                                                } 
                                            }''')
        assert executed == {
            'data': {'allFoodTrucks': {'edges': []}}
        }


@pytest.mark.usefixtures('create_db', 'populate_food_truck_db')
class TestQuery():
    """
    Test cases for validating the GraphQL query endpoint of the application with a populated database. 
    Prior to running the test cases, the following procedure is run:

    1. Initialize application
    2. Create database table
    3. Populate database with predefined elements
    """
    def test_query(self, graphql_client):
        executed = graphql_client.execute('''{  
                                                allFoodTrucks {
                                                    edges {
                                                        node { id }
                                                    }   
                                                } 
                                            }''')
        data = executed['data']['allFoodTrucks']['edges']
        assert len(data) == len(test_data)
