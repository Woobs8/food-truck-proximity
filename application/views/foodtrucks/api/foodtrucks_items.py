from flask import request, jsonify, abort, make_response, Blueprint, current_app
from application.models import FoodTruck, db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView


class FoodTrucksItemsAPI(MethodView):
    """
    A class used to encapsulate the API for the /foodtrucks/items resource

    Methods
    -------
    get(needle)
        implements the GET /foodtrucks/items/<string: needle> endpoint

    """

    def get(self, needle):
        """
        GET /foodtrucks/items/<needle> endpoint returns resources in /foodtrucks 
        filtered by content of food_items field

        Parameters:
            needle (str): substring that food_items field must contain (inferred from request URL)

        Returns:
            str: JSON representation of all resources in /foodtrucks filtered by those where the
                food_items field contains substring needle 
        """
        # search needle must be defined
        if not needle:
            abort(400, 'Missing parameter')
        
        # query by trucks where needle is a case-insensitive substring of food_items
        try:
            trucks = FoodTruck.query.filter(FoodTruck.food_items.ilike('%{}%'.format(needle)))
            return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
        except SQLAlchemyError as e:
            current_app.logger.error('error searching for needle %s: %s', needle, e)
            abort(500, 'Error retriving resources by items {}'.format(needle))